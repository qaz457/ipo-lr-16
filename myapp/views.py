from django.contrib.auth import login
from io import BytesIO
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages

from .forms import CustomUserCreationForm
from .models import Product, ProductCategory, Manufacturer, Cart, CartItem,Order,OrderItem
from openpyxl import Workbook
from django.core.mail import EmailMessage

def base(request):
    return render(request,'base.html')

def author(request):
    return render(request,'author.html')

def shop(request):
    return render(request,'shop.html')

def product_list(request):
    products = Product.objects.all()
    categories = ProductCategory.objects.all()
    manufacturers = Manufacturer.objects.all()

    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id = category_id)

    manufacturer_id = request.GET.get('manufacturer')
    if manufacturer_id:
        products = products.filter(manufacturer_id = manufacturer_id)

    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    context = {
        'products': products,
        'categories': categories,
        'manufacturers': manufacturers,
        'selected_category': category_id,
        'selected_manufacturer': manufacturer_id,
        'search_query': search_query,

    }
    return render(request, 'product_list.html', context)

def item(request,pk):
    actual_id = pk + 34
    product = get_object_or_404(Product, pk=actual_id)
    return render(request, 'product_info.html', {
            'product': product,
            'item_pk': pk
    })

@login_required
def cart_add(request, item_id):
    actual_id = item_id + 34
    product = get_object_or_404(Product, pk=actual_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': 1}
    )

    if not created:
        cart_item.quantity += 1
    else:
        cart_item.quantity = 1

    cart_item.save()
    messages.success(request, f'{product.name} в корзине.')

    return redirect('cart_view')

def cart_update(request, item_id):
    if request.method == "POST":
        quantity = int(request.POST.get("quantity",1))
        actual_id = item_id + 34

        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item = get_object_or_404(CartItem, cart=cart, product_id=actual_id)

        if quantity > cart_item.product.stock:
            messages.error(request, f"Максимальное количество для {cart_item.product.name} — {cart_item.product.stock}")
            quantity = cart_item.product.stock

        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, f"Количество {cart_item.product.name} обновлено до {cart_item.quantity}")

    return redirect('cart_view')
def cart_remove(request, item_id):
    actual_id = item_id + 34
    cart = get_object_or_404(Cart,user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, product_id=actual_id)
    cart_item.delete()
    messages.success(request, f"{cart_item.product.name} удалён из корзины")
    return redirect('cart_view')

@login_required
def cart_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = CartItem.objects.filter(cart=cart)

    for item in items:
        item.total = item.product.price * item.quantity

    total_price = sum(item.total for item in items)

    context = {
        'cart_items': items,
        'total_price': total_price
    }
    return render(request, 'cart.html', context)

@login_required
def checkout(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = CartItem.objects.filter(cart=cart)

    if not items:
        messages.error(request, "Корзина пуста")
        return redirect('cart_view')

    if request.method == 'POST':
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        comment = request.POST.get('comment')

        if not address or not phone:
            messages.error(request,"Заполните все обязательные поля")
            return render(request,'checkout.html',{'items':items})

        total_price = sum(item.item_price() for item in items)

        order = Order.objects.create(
            user = request.user,
            address = address,
            phone = phone,
            comment = comment,
            total_price = total_price
        )

        for item in items:
            OrderItem.objects.create(
                order = order,
                product = item.product,
                quantity = item.quantity,
                price = item.product.price
            )

        wb = Workbook()
        ws = wb.active
        ws.title = order.__str__()
        ws.append(["Товар","Количество","Цена за ед.","Сумма"])
        for item in items:
            ws.append([
                item.product.name,
                item.quantity,
                item.product.price,
                item.item_price()
            ])
            product = item.product
            product.stock -= item.quantity
            product.save()
        ws.append([])
        ws.append(["Итого","","",total_price])

        excel_file = BytesIO()
        wb.save(excel_file)
        excel_file.seek(0)

        if not request.user.email:
            messages.error(request, 'У вашего аккаунта не указан email. Заполните его в профиле, чтобы получать чеки.')
            return redirect('base')
        subject = order.__str__()

        message = f'''
            Спасибо за заказ {request.user.username}!
            Ваш заказ №{order.id}.
            Сумма: {total_price} BYN.
            Чек прикреплен.
            '''

        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [request.user.email]

        email = EmailMessage(
            subject,
            message,
            from_email,
            recipient_list
        )
        email.attach(f"check_{order.id}.xlsx",excel_file.getvalue(),'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        email.send()
        items.delete()
        messages.success(request,f"Заказ №{order.id} успешно оформлен! Чек отправлен на {request.user.email}")
        return redirect('cart_view')

    context = {
        'items':items,
        'total_price':sum(item.item_price() for item in items)
    }

    return render(request,'checkout.html', context)

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('base')
    else:
        form = CustomUserCreationForm()
    return render(request,'registration/register.html', {'form': form})

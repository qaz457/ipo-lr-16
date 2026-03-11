from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User

class ProductCategory(models.Model):
    name = models.CharField(max_length=100,verbose_name="Название")
    description = models.TextField(null=False,blank=False,verbose_name="Описание")

    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=200,verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    image = models.ImageField(upload_to='photos/' , verbose_name="Фото_товара")
    price = models.DecimalField(max_digits=10,decimal_places=2,verbose_name="Цена",validators=[MinValueValidator(0)])
    stock = models.IntegerField(verbose_name="Количество_на_складе ",validators=[MinValueValidator(0)])
    category = models.ForeignKey(ProductCategory,on_delete = models.CASCADE,verbose_name="Категория")
    manufacturer = models.ForeignKey('Manufacturer',on_delete=models.CASCADE,verbose_name="Производитель")

    def __str__(self):
        return self.name

class Manufacturer(models.Model):
    name = models.CharField(max_length=100,verbose_name="Название")
    country = models.CharField(max_length=100,verbose_name="Страна")
    description = models.TextField(blank=True,null=True,verbose_name="Описание")

    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,verbose_name="Пользователь")
    date_creation = models.DateTimeField(auto_now_add=True,verbose_name="Дата_создания")

    def __str__(self):
        return f"Корзина пользователя {self.user.username}"
    def total_price(self):
        return sum(item.item_price() for item in self.items.all())
class CartItem(models.Model):
    cart = models.ForeignKey('Cart',on_delete=models.CASCADE,related_name="items",verbose_name='Корзина')
    product = models.ForeignKey('Product',on_delete=models.CASCADE,verbose_name="Товар")
    quantity = models.PositiveIntegerField(verbose_name="Количсетво")

    def __str__(self):
        return f"{self.product.name} ({self.quantity} шт.)"
    def item_price(self):
        return self.product.price * self.quantity
    def clean(self):
        if self.quantity > self.product.stock:
            raise ValidationError("Нету такого количества в наличии")

class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="Пользователь")
    date_creation = models.DateTimeField(auto_now_add=True,verbose_name="Дата_создания")
    address = models.CharField(max_length=500,verbose_name="Адрес_доставки")
    phone = models.CharField(max_length=20,verbose_name="Телефон")
    comment = models.TextField(blank=True,verbose_name="Комментарий")
    total_price = models.DecimalField(max_digits=10,decimal_places=2,verbose_name="Общая стоимость")

    def __str__(self):
        return  f"Заказ №{self.id} от {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='items',verbose_name='Заказ')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name="Товары")
    quantity = models.PositiveIntegerField(verbose_name="Количество")
    price = models.DecimalField(max_digits=10,decimal_places=2,verbose_name="Цена")























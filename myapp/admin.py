from django.contrib import admin
from .models import Product,ProductCategory,CartItem,Cart,Manufacturer

class CartItemInLine(admin.TabularInline):
    model = CartItem
    extra = 1

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("user","date_creation")
    inlines = [CartItemInLine]

admin.site.register(CartItem)
admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(Manufacturer)



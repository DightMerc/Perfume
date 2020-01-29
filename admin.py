from django.contrib import admin
from .models import Product, Category, Photo, Brand, FreeOption, FreeOptionGroup, PriceForOption, Cart, TempProduct       
from .models import GroupCategory, BannerPhoto, FavouriteProducts, FavouriteBrands, TempOrder, Order
# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'active')
    ordering = ('id', 'active')
    search_fields = ('id', 'title', "active")


@admin.register(Category)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    ordering = ('id',)
    search_fields = ('id', 'title')


admin.site.register(Photo)
admin.site.register(FavouriteProducts)

admin.site.register(Brand)
admin.site.register(Cart)
admin.site.register(TempProduct)
admin.site.register(GroupCategory)
admin.site.register(BannerPhoto)
admin.site.register(FavouriteBrands)
admin.site.register(TempOrder)
admin.site.register(Order)



@admin.register(FreeOption)
class FreeOptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    ordering = ('id',)
    search_fields = ('id', 'title')

@admin.register(FreeOptionGroup)
class FreeOptionGroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    ordering = ('id',)
    search_fields = ('id', 'title')

@admin.register(PriceForOption)
class PriceForOptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'product','option', 'price')
    ordering = ('id', 'product', 'option')
    search_fields = ('id', 'product', 'option', 'price')

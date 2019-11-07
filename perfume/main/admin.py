from django.contrib import admin
from .models import Product, Category, ProductVolume, PriceForVolume, Photo

# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'titleRU','titleUZ', 'active')
    ordering = ('id', 'active')
    search_fields = ('id', 'titleRU', 'titleUZ', "active")


@admin.register(Category)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'titleRU','titleUZ')
    ordering = ('id',)
    search_fields = ('id', 'titleRU', 'titleUZ')


admin.site.register(Photo)
admin.site.register(ProductVolume)


@admin.register(PriceForVolume)
class PriceForVolumeAdmin(admin.ModelAdmin):
    list_display = ('id', 'product','volume', 'price')
    ordering = ('id', 'product', 'volume')
    search_fields = ('id', 'product', 'volume', 'price')

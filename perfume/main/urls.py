"""perfume URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.conf import settings
from django.views.static import serve

from .views import MainView, SingleProductView, ShopView, AddToCartView, CartView, BuyView, KickProductView, CheckoutView, BrandView, ChoosenBrandView


urlpatterns = [
    path('', MainView, name="MainView"),
    path('products/<int:pk>', SingleProductView, name="SingleProductView"),
    path('shop/<int:pk>', ShopView, name="ShopView"),
    path('addToCart/', AddToCartView, name="AddToCartView"),
    path('cart/', CartView, name="CartView"),
    path('buy/', BuyView, name="BuyView"),
    path('kickProduct/', KickProductView, name="KickProductView"),
    path('checkout/', CheckoutView, name="CheckoutView"),
    path('brands/', BrandView, name="BrandView"),
    path('brands/<int:brand>/', ChoosenBrandView, name="ChoosenBrandView"),






]

urlpatterns += [url(r'^media/(?P<path>.*)$', serve, {'document_root': "media/" + settings.MEDIA_ROOT, }),]

from django.shortcuts import render
from .models import Product, Category, Brand, PriceForOption, Cart, TempProduct, PriceForOption, TempOrder, Order, GroupCategory, BannerPhoto
from .models import FavouriteProducts
from django.http import JsonResponse, HttpResponse, response, HttpResponsePermanentRedirect
import requests

from django.core.paginator import Paginator

import logging



logger = logging.getLogger(__name__)

# Create your views here.
def MainView(request):
    user_num = request.session.get('user')
    if user_num is None:
        user_num = int(Cart.objects.latest("id").userId) + 1
        request.session['user'] = user_num
        cart = Cart()
        cart.userId = user_num
        cart.save()
    else:
        cart = Cart.objects.get(userId=int(user_num))

    return render(request, "main/index.html", {
        'banners': BannerPhoto.objects.all(),
        'products': FavouriteProducts.objects.all().first().products.all().filter(active=True),
        'user': user_num,
        'cart': cart,
        'categories': GroupCategory.objects.get(title="Главная страница").categories.all(),
        'brands': Brand.objects.all(),
        
    })


def BrandView(request):
    user_num = request.session.get('user')
    if user_num is None:
        user_num = int(Cart.objects.latest("id").userId) + 1
        request.session['user'] = user_num
        cart = Cart()
        cart.userId = user_num
        cart.save()
    else:
        cart = Cart.objects.get(userId=int(user_num))

    return render(request, "main/brands.html", {
        'brands': Brand.objects.all(),
        'user': user_num,
        'cart': cart,
    })


def ChoosenBrandView(request, brand):
    categories = GroupCategory.objects.all()
    currentBrand = Brand.objects.get(pk=brand)

    products = Product.objects.filter(brand=currentBrand)

    paginator = Paginator(products, 15) # Show 25 contacts per page

    page = request.GET.get('page')
    products = paginator.get_page(page)

    currentPage = page if page else 1

    return render(request, "main/shop.html", {
        'currentPage': currentPage,
        'currentBrand': currentBrand,
        'products': products,
        'categories': categories.get(title="Магазин стандарт")
    })


def SingleProductView(request, pk):
    product = Product.objects.all().filter(active=True).get(pk=pk)
    
    user_num = request.session.get('user')
    if user_num is None:
        user_num = int(Cart.objects.latest("id").userId) + 1
        request.session['user'] = user_num
        cart = Cart()
        cart.userId = user_num
        cart.save()
    else:
        cart = Cart.objects.get(userId=int(user_num))

    return render(request, "main/product-details.html", {
        'product': product,
        'mainPhoto': product.photo.all().first().photo.url,
        'photoes': product.photo.all(),
        'optionMain': product.options.first(),
        'options': product.options.all()[1:],
        'prices': PriceForOption.objects.filter(product=product),

        'user': user_num,
        'cart': cart
    })


def CartView(request):
    user_num = request.session.get('user')
    if user_num is None:
        user_num = int(Cart.objects.latest("id").userId) + 1
        request.session['user'] = user_num
        cart = Cart()
        cart.userId = user_num
        cart.save()
    else:
        cart = Cart.objects.get(userId=int(user_num))
    price = 0

    for a in cart.products.all():
        price += int(a.price)

    return render(request, "main/cart.html", {
        'user': user_num,
        'cart': cart,
        'total': price
    })


def KickProductView(request):
    user_num = request.session.get('user')
    
    cart = Cart.objects.get(userId=int(user_num))

    cart.products.remove(TempProduct.objects.get(pk=request.POST.get("product")))


    return HttpResponse("ok")


def CheckoutView(request):
    user_num = request.session.get('user')
    
    cart = Cart.objects.get(userId=int(user_num))

    tempOrder = TempOrder()
    tempOrder.firstName = request.POST.get("firstName")
    tempOrder.lastName = request.POST.get("lastName")
    tempOrder.address = request.POST.get("address")
    tempOrder.comment = request.POST.get("comment")
    tempOrder.phone = int(str(request.POST.get("phone")).replace("+", ""))
    tempOrder.save()

    order = Order()
    order.tempOrder = tempOrder
    order.save()

    text = "Новый заказ\n"

    for product in cart.products.all():
        tempOrder.products.add(product)
        cart.products.remove(product)

        try:
            text = text + f"\n{product.product.titleRU} - {product.option.title}"
        except Exception as e:
            text = text + f"\n{product.product.titleRU} - {product.optionGroup.title}"


    text = text + f"\n\n{tempOrder.firstName} {tempOrder.lastName}\n\nАдрес: {tempOrder.address}\nКомментарий: {tempOrder.comment}\n\nНомер телефона: +{tempOrder.phone}"
    

    url = f"https://api.telegram.org/bot796303915:AAF4MJs2lqEYxUWtK-7VSjYVWGjeLhNEXnU/sendMessage?chat_id=-1001262840203&text={text}"
    requests.get(url = url)

    

    

    return HttpResponse("ok")

def BuyView(request):
    user_num = request.session.get('user')
    if user_num is None:
        user_num = int(Cart.objects.latest("id").userId) + 1
        request.session['user'] = user_num
        cart = Cart()
        cart.userId = user_num
        cart.save()
    else:
        cart = Cart.objects.get(userId=int(user_num))

    price = 0

    for a in cart.products.all():
        price += int(a.price)

    return render(request, "main/checkout.html", {
        'user': user_num,
        'cart': cart,
        'total': price

    })

def AddToCartView(request):
    user_num = request.session.get('user')
    option = request.POST.get("option")
    
    if option[0].isdigit():
        if not " л" in option:
            option = option.replace(" л", "") + " л"

    tempProduct = TempProduct()
    tempProduct.product = Product.objects.get(pk=int(request.POST.get("product")))
    try:
        tempProduct.option = tempProduct.product.options.first().options.all().get(title=option)
    except Exception as e:
        logger.error(option)

        tempProduct.optionGroup = tempProduct.product.options.all().get(title=option)


    try:
        tempProduct.price = PriceForOption.objects.get(product=tempProduct.product, option=tempProduct.optionGroup).price
    except Exception as e:
        tempProduct.price = PriceForOption.objects.filter(product=tempProduct.product).first().price


    tempProduct.save()



    if user_num is None:
        user_num = int(Cart.objects.latest("id").userId) + 1
        request.session['user'] = user_num
        cart = Cart()
        cart.userId = user_num
        cart.save()
    else:
        cart = Cart.objects.get(userId=int(user_num))

    cart.products.add(tempProduct)
    return HttpResponse("ok")
    

    

def ShopView(request, pk):
    categories = GroupCategory.objects.all()
    currentCategory = Category.objects.get(pk=pk)

    products = Product.objects.filter(category=currentCategory)

    paginator = Paginator(products, 15) # Show 25 contacts per page

    page = request.GET.get('page')
    products = paginator.get_page(page)

    currentPage = page if page else 1

    return render(request, "main/shop.html", {
        'currentPage': currentPage,
        'currentCategory': currentCategory,
        'products': products,
        'categories': categories.get(title="Магазин стандарт")


    })
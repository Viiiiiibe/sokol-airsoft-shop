from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from products.models import Product
from .cart import Cart
import datetime
from .forms import MakingAnOrderForm, MakingAnDeliveryOrderForm
from django.contrib.auth import get_user_model
from django.db.models import F

User = get_user_model()


def cart_view(request):
    cart = Cart(request)
    context = {
        'cart': cart,
    }

    return render(request, 'cart/cart-view.html', context)


def cart_add(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        product = get_object_or_404(Product, pk=product_id)

        cart.add(product=product, quantity=product_qty)

        cart_qty = cart.__len__()

        response = JsonResponse({'qty': cart_qty, "product": product.name})

        return response


def cart_delete(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))

        cart.delete(product=product_id)

        cart_qty = cart.__len__()

        cart_total = cart.get_total_price()

        response = JsonResponse({'qty': cart_qty, 'total': cart_total})

        return response


def cart_update(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))

        if Product.objects.get(pk=product_id).items_left is None:
            prod_items_left = 10000
        else:
            prod_items_left = Product.objects.get(pk=product_id).items_left

        if (int(request.POST.get('product_qty')) < prod_items_left) and (int(request.POST.get('product_qty')) > 1):
            product_qty = int(request.POST.get('product_qty'))
        elif int(request.POST.get('product_qty')) <= 1:
            product_qty = 1
        else:
            product_qty = prod_items_left

        cart.update(product=product_id, quantity=product_qty)

        cart_qty = cart.__len__()
        cart_total = cart.get_total_price()

        response = JsonResponse({'qty': cart_qty, 'total': cart_total})

        return response


def order_view(request):
    cart = Cart(request)
    if request.method == "POST":
        form = MakingAnOrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.price = float(cart.get_total_price())
            order.created = datetime.datetime.now()
            order.delivery_method = request.POST.get("shipping", '')
            if order.delivery_method == 'Забрать в пункте выдачи СДЭК':
                order.delivery_region = request.POST.get("pickup-point-region", )
                order.delivery_city = request.POST.get("pickup-point-city", )
                order.delivery_street = request.POST.get("pickup-point-street", )
                order.delivery_house = request.POST.get("pickup-point-house", )
            elif order.delivery_method == 'Курьерская доставка СДЭК':
                order.delivery_region = request.POST.get("courier-delivery-region", )
                order.delivery_city = request.POST.get("courier-delivery-city", )
                order.delivery_street = request.POST.get("courier-delivery-street", )
                order.delivery_house = request.POST.get("courier-delivery-house", )
                order.delivery_flat = request.POST.get("courier-delivery-flat", )
                order.delivery_entrance = request.POST.get("courier-delivery-entrance", )
                order.delivery_floor = request.POST.get("courier-delivery-floor", )
                order.delivery_intercom = request.POST.get("courier-delivery-intercom", )
            elif order.delivery_method == 'Самовывоз':
                order.delivery_region = "Ленинградская"
                order.delivery_city = "Санкт-Петербург"
                order.delivery_street = "Лидии Зверевой"
                order.delivery_house = "5к1"
            for item in cart:
                order.ordered_products = order.ordered_products + str(item.get('product')) + " x" + str(
                    item.get('qty')) + "; "
                product = item.get('product')
                product_id = int(product.pk)
                Product.objects.filter(id=product_id).update(items_left=F("items_left") - item.get('qty'))
                cart.delete(product=product_id)
            if request.user.is_authenticated:
                order.customer = request.user
            order.customer_comment = request.POST.get("comment", )
            order.save()
            return redirect('cart:order-completed', order.number)
    else:
        if request.user.is_authenticated:
            form = MakingAnOrderForm(
                initial={
                    'customer_last_name': request.user.last_name,
                    'customer_first_name': request.user.first_name,
                    'customer_patronymic': request.user.patronymic,
                    'customer_email': request.user.email,
                    'customer_phone': request.user.phone_number,
                    'customer_vk': request.user.vk,
                    'customer_telegram': request.user.telegram
                }
            )
        else:
            form = MakingAnOrderForm()

    context = {
        'cart': cart,
        'form': form,
    }

    return render(request, 'cart/order.html', context)


def order_completed(request, number):
    context = {
        'number': number,
    }
    return render(request, 'cart/order_completed.html', context)


def delivery_order_view(request):
    if request.method == "POST":
        form = MakingAnDeliveryOrderForm(request.POST)
        if form.is_valid():
            delivery_order = form.save(commit=False)
            delivery_order.created = datetime.datetime.now()
            delivery_order.description = str(request.POST.getlist("description", ''))
            delivery_order.delivery_method = request.POST.get("shipping", '')
            if delivery_order.delivery_method == 'Забрать в пункте выдачи СДЭК':
                delivery_order.delivery_region = request.POST.get("pickup-point-region", )
                delivery_order.delivery_city = request.POST.get("pickup-point-city", )
                delivery_order.delivery_street = request.POST.get("pickup-point-street", )
                delivery_order.delivery_house = request.POST.get("pickup-point-house", )
            elif delivery_order.delivery_method == 'Курьерская доставка СДЭК':
                delivery_order.delivery_region = request.POST.get("courier-delivery-region", )
                delivery_order.delivery_city = request.POST.get("courier-delivery-city", )
                delivery_order.delivery_street = request.POST.get("courier-delivery-street", )
                delivery_order.delivery_house = request.POST.get("courier-delivery-house", )
                delivery_order.delivery_flat = request.POST.get("courier-delivery-flat", )
                delivery_order.delivery_entrance = request.POST.get("courier-delivery-entrance", )
                delivery_order.delivery_floor = request.POST.get("courier-delivery-floor", )
                delivery_order.delivery_intercom = request.POST.get("courier-delivery-intercom", )
            elif delivery_order.delivery_method == 'Самовывоз':
                delivery_order.delivery_region = "Ленинградская"
                delivery_order.delivery_city = "Санкт-Петербург"
                delivery_order.delivery_street = "Лидии Зверевой"
                delivery_order.delivery_house = "5к1"
            if request.user.is_authenticated:
                delivery_order.customer = request.user
            delivery_order.customer_comment = request.POST.get("comment", )
            delivery_order.save()
            return redirect('cart:delivery-order-completed', delivery_order.number)
    else:
        if request.user.is_authenticated:
            form = MakingAnOrderForm(
                initial={
                    'customer_last_name': request.user.last_name,
                    'customer_first_name': request.user.first_name,
                    'customer_patronymic': request.user.patronymic,
                    'customer_email': request.user.email,
                    'customer_phone': request.user.phone_number,
                    'customer_vk': request.user.vk,
                    'customer_telegram': request.user.telegram
                }
            )
        else:
            form = MakingAnOrderForm()

    context = {
        'form': form,
    }

    return render(request, 'cart/delivery_order.html', context)


def delivery_order_completed(request, number):
    context = {
        'number': number,
    }
    return render(request, 'cart/delivery_order_completed.html', context)

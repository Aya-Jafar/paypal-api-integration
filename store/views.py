import json
from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import datetime
from .utils import cookieCheckout, cookieData



def store(request):
    products = Product.objects.all()

    if request.user.is_authenticated:
        customer = request.user.customer
        current_order,created = Order.objects.get_or_create(
            customer=customer,completed=False)
        total_items_count = current_order.count_order_items

    else:
        # print(request.COOKIES)
        if 'cart' in request.COOKIES.keys():
            total_items_count = len(list(json.loads(request.COOKIES['cart'])))
        else:
            total_items_count = 0
    
    context = {
        'products': products,
        'total_items_count': total_items_count
    }
    return render(request, 'store/store.html', context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, completed=False)
        items = order.orderitem_set.all()
        total_items_count = order.count_order_items
    else: # for not authenticated useres
        items = cookieData(request)['items']
        order = cookieData(request)['order']
        total_items_count = cookieData(request)['total_items_count']

    context = {'items': items,
                'order': order,
                'total_items_count': total_items_count
                }

    return render(request, 'store/cart.html', context)



def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, completed=False)
        items = order.orderitem_set.all()
        total_items_count = order.count_order_items

    else:
        items = cookieData(request)['items']
        total_items_count = cookieData(request)['total_items_count']
        order = cookieData(request)['order']
    context = {'items': items,
                'order': order,
                'total_items_count': total_items_count}

    return render(request, 'store/checkout.html', context)


def update_item(request):
    data = json.loads(request.body) # convert string response to dict
    
    # print(type(data))

    customer = request.user.customer

    product = Product.objects.get(id=data['productID'])

    order, created = Order.objects.get_or_create(
        customer=customer, completed=False)

    item, created = OrderItem.objects.get_or_create(
        order=order, product=product)

    if data['action'] == 'add':
        item.qnt += 1
    elif data['action'] == 'remove':
        item.qnt -= 1

    item.save()

    if item.qnt <= 0 and data['action'] == 'remove':
        item.delete()

    return JsonResponse('item updated successfully', safe=False)


def process_order(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)  # data comming from js response
    print(data)
    # data 
    #      {'userInfo': {'name': 'Aya Jafar', 'email': 'ayajafar991@gmail.com', 'total': '40.00'},
    #     'shippingInfo': {'address': 'ff', 'city': 'Baghdad', 'state': 'f', 'zipcode': 'f'}}

    if request.user.is_authenticated :
        if int(float(data['userInfo']['total'])) > 0:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(
                customer=customer,
                completed=False
            )
    else:
        customer , order = cookieCheckout(request,data)

    # the next code will excute regarding of the user type
    total = float(data['userInfo']['total'])

    order.translation_id = transaction_id

    # to ensure that data have'nt been manipulated in the front-end
    if total == float(order.order_total_price):
        order.completed = True  # order is closed and we can't add more items

    order.save()

    ShippingAddress.objects.create(
        customer=customer,
        order=order,
        address=data['shippingInfo']['address'],
        city=data['shippingInfo']['city'],
        state=data['shippingInfo']['state'],
        zipcode=data['shippingInfo']['zipcode'],
    )
    # print(ShippingAddress.objects.all())
        
    return JsonResponse('Payment processed successfully', safe=False)

import json
from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import datetime


def store(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'store/store.html', context)


def cart(request):

    # print(request.user.customer)
    # print(type(request.user.customer))
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, completed=False)
        items = order.orderitem_set.all()

    else:
        items = []
        order = {
            'order_total_price': 0,
            'order_total_qnt': 0
        }
    context = {'items': items,
                'order': order}
    return render(request, 'store/cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, completed=False)
        items = order.orderitem_set.all()

    else:
        items = []
        order = {
            'order_total_price': 0,
            'order_total_qnt': 0,
            'shipping': False
        }
    context = {'items': items,
                'order': order}

    return render(request, 'store/checkout.html', context)


def update_item(request):
    data = json.loads(request.body)

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

    if item.qnt <=0 and data['action'] == 'remove':
        item.delete()

    return JsonResponse('item updated successfully', safe=False)



def process_order(request):
    transaction_id = datetime.datetime().now().timestamp()
    print(transaction_id)
    return JsonResponse('Payment processed successfully', safe=False)

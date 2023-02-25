import json
from .models import * 


def cookieData(request):
    try:
        # get the value of cart cookie and convert it from string to a dictionary
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    items = []
    order = {
        'order_total_price': 0,
        'order_total_qnt': 0,
        'shipping':False,
        'total_items_count':0
    }
    # print(cart)
    for i in cart:
        try:
            # get the product of each item
            product = Product.objects.get(id=int(i))
            # update the order total price
            total = product.price * cart[i]['quantity']
            
            order['order_total_price'] += total
            order['order_total_qnt'] += cart[i]['quantity']
            
            item = {
                'product': {
                    'id':product.id,
                    'name':product.name,
                    'price':product.price,
                    'image':product.image
                },
                'qnt':cart[i]['quantity'],
                'total':total
            }
            items.append(item)
        except ProductDoesNotExist:
            del cart[i]
        except:
            pass
    total_items_count = len(items)
    
    return {'items': items,
                'order': order,
                'total_items_count': total_items_count
                }


def cookieCheckout(request , data):
    # data
    #      {'userInfo': {'name': 'Aya Jafar', 'email': 'ayajafar991@gmail.com', 'total': '40.00'},
    #     'shippingInfo': {'address': 'ff', 'city': 'Baghdad', 'state': 'f', 'zipcode': 'f'}}

    # Cookie data
    #   {'items': [{'product': {'id': 4, 'name': 'Jackit', 'price': 20.0, 'image': < ImageFieldFile: None >}, 'qnt': 1, 'total': 20.0}],
    #   'order': {'order_total_price': 20.0,
    #   'order_total_qnt': 1,
    #   'shipping': False,
    #   'total_items_count': 0},
    #   'total_items_count': 1}
    if int(float(data['userInfo']['total'])) > 0:
        # handle checkout for unauthenticated users
        name = data['userInfo']['name']
        email = data['userInfo']['email']

        items = cookieData(request)['items']

        customer, created = Customer.objects.get_or_create(
            email=email
        )
        customer.name = name
        customer.save()
        order = Order.objects.create(
            customer=customer,
            completed=False
        )

        # Create an actual items from the guest user cookie
        for item in items:
            # {'product': {'id': 4, 'name': 'Jackit', 'price': 20.0, 'image': <ImageFieldFile: None>}, 'qnt': 1, 'total': 20.0}
            product = Product.objects.get(id=item['product']['id'])
            orderItem = OrderItem.objects.create(
                product=product,
                order=order,
                qnt=item['qnt'],
            )
    return customer, order

from django.db import models
from django.contrib.auth.models import User
import PIL


class Customer(models.Model):
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    price = models.FloatField()
    digital = models.BooleanField(default=False)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    # if false,order is an open card and we can add more to it
    completed = models.BooleanField(default=False)
    translation_id = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'{self.id} - {self.customer.name}'

    @property
    def order_total_price(self):
        return sum([item.total for item in self.orderitem_set.all()])

    @property
    def order_total_qnt(self):
        return sum([item.qnt for item in self.orderitem_set.all()])



class OrderItem(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(
        Order, on_delete=models.SET_NULL, null=True, blank=True)
    qnt = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.id} - {self.product.name}'
    
    @property
    def total(self) -> int:
        return self.product.price * self.qnt

    @property
    def shipping(self) -> bool:
        shipping = False
        items = self.orderitem_set.all()
        for item in items:
            if item.product.digital == False:
                shipping=True
        return shipping 



class ShippingAddress(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address

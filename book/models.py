from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from datetime import datetime
from django.db.models import Sum
# Create your models here.


class Book(models.Model):
    book_no = models.CharField(max_length=10, blank=True, null=True)
    book_title = models.CharField(max_length=100, blank=True, null=True)
    book_type = models.CharField(max_length=20, default='Secondary')    
    book_board = models.CharField(max_length=20, blank=True, null=True)
    book_image1 = models.ImageField(upload_to='media', blank=True, null=True)
    book_image2 = models.ImageField(upload_to='media', blank=True, null=True)
    book_image3 = models.ImageField(upload_to='media', blank=True, null=True)
    book_image4 = models.ImageField(upload_to='media', blank=True, null=True)
    book_mrp = models.IntegerField(default=1)
    book_price = models.IntegerField(default=1)
    book_discount_price = models.IntegerField(blank=True, null=True)
    book_category = models.CharField(max_length=30, blank=True, null=True)
    book_stock = models.IntegerField(default=1)
    standard = models.CharField(max_length=30, blank=True, null=True)
    ideal_course = models.CharField(max_length=500, blank=True, null=True)
    ideal_sem = models.CharField(max_length=150, blank=True, null=True)
    publication_name = models.CharField(max_length=50, blank=True, null=True)
    authors = models.CharField(max_length=200, blank=True, null=True)
    edition = models.CharField(max_length=60, blank=True, null=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.book_title

    def get_pro_amount_saved(self):
        return self.book_mrp - self.book_price

    class Meta:
        verbose_name_plural = 'Books'
        ordering = ('book_stock',)

    def get_absolute_url(self):
        return reverse("book:book_product", kwargs={
            'slug': self.slug
        })

    def add_to_cart_url(self):
        return reverse("book:add-to-cart", kwargs={
            'slug': self.slug
        })

    def buy_now_url(self):
        return reverse("book:od-summary")


class OrderProduct(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    # Product is refered to Book table
    product = models.ForeignKey(Book, on_delete=models.CASCADE)
    product_quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.product.book_title} - {self.product_quantity}"

    def get_pro_price(self):
        return self.product_quantity * self.product.book_price

    def get_pro_discount_price(self):
        return self.product_quantity * self.product.book_discount_price

    def get_pro_total_price(self):
        return self.get_delievery_charges() + self.get_pro_price()

    def get_total_cart_price(self):
        return self.product_quantity * self.product.book_price

    def get_total_cart_discount_price(self):
        return self.product_quantity * self.product.book_discount_price

    def get_amount_saved(self):
        return self.get_total_cart_price() - self.get_total_cart_discount_price()

    def get_final_price(self):
        if self.product.book_discount_price:
            return self.get_total_cart_discount_price()
        return self.get_total_cart_price()

    def get_total_quantity(self):
        return self.product_quantity


class Order(models.Model):
    order_id = models.CharField(
        null=True, blank=True, max_length=15)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    products = models.ManyToManyField(OrderProduct)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    delievery_date = models.DateTimeField(null=True, blank=True)
    delivery_chages = models.FloatField(default=0.0)
    ordered = models.BooleanField(default=False)
    being_delieverd = models.BooleanField(default=False)
    recieved = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)
    delievery_address = models.ForeignKey(
        'Address', on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.first_name

    # def get_absolute_od_url(self):
        # return reverse("products:request-refund", kwargs={'slug': self.order_id})

    def get_product(self):
        return ", ".join([str(p) for p in self.products.all()])

    def get_total_quantity(self):
        total = 0
        for order_product in self.products.all():
            total += order_product.get_total_quantity()
        return total

    # Delievery charges set karnya sathi
    def get_total_delievery_charges(self):
        if self.get_total() >= 10:
            return 50
        else:
            return 0

    def get_total(self):
        total = 0
        for order_product in self.products.all():
            total += order_product.get_final_price()
        return total

    def total_od_price(self):
        a = self.get_total() + self.get_total_delievery_charges()
        return a


class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField(default=0.0)
    timestamp = models.DateTimeField(auto_now_add=True)
    payment_option = models.CharField(blank=True, null=True, max_length=20)
    payment_sender_name = models.CharField(blank=True, max_length=50)

    def __str__(self):
        return self.payment_option


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    address = models.CharField(max_length=150, blank=True, null=True)
    pin_code = models.CharField(max_length=10, blank=True, null=True)
    contact_no = models.CharField(max_length=14, blank=True, null=True)
    refer_code = models.CharField(max_length=14, blank=True, null=True)   
    default = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Adresses'
    def __str__(self):
        return self.refer_code

class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    email = models.EmailField()
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.order}"


class BookRequests(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)
    address = models.TextField(max_length=150, blank=True, null=True)
    contact_number = models.CharField(max_length=120, blank=True, null=True)
    book_title = models.CharField(max_length=150, blank=True, null=True)
    book_mrp = models.IntegerField(default=1)
    book_category = models.CharField(max_length=50, blank=True, null=True)
    book_board = models.CharField(max_length=20, blank=True, null=True)
    standard = models.CharField(max_length=30, blank=True, null=True)
    ideal_course = models.CharField(max_length=500, blank=True, null=True)
    ideal_sem = models.CharField(max_length=150, blank=True, null=True)
    publication_name = models.CharField(max_length=50, blank=True, null=True)
    authors = models.CharField(max_length=200, blank=True, null=True)
    edition = models.CharField(max_length=60, blank=True, null=True)
    request_date = models.DateTimeField(blank=True, null=True)
    book_status = models.BooleanField(default=False)

    def __str__(self):
        return self.book_title

    class Meta:
        verbose_name_plural = 'Book requests'


class Messages(models.Model):
    contact_no = models.CharField(max_length=20, blank=True, null=True)
    message = models.TextField(max_length=500, blank=True, null=True)
    message_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.contact_no

    class Meta:
        verbose_name_plural = 'Messages'
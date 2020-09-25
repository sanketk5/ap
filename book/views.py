from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.views.generic.edit import FormView
from django.views.generic import ListView, DetailView, View
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponse
from datetime import datetime
from django.utils import timezone
from django.db.utils import DataError
from .models import Book, OrderProduct, Order, Address, Refund, Payment, BookRequests
from accounts.models import Profile
from .forms import CheckoutForm, PaymentForm, RefundForm
from itertools import zip_longest
from collections import OrderedDict
import random

# Create your views here.


def home(request):
    book = Book.objects.all()
    return render(request, 'base.html', {'books': book})


def product(request):
    book = Book.objects.all()
    return render(request, "product.html", {'books': book})


def about(request):
    return render(request, "about.html")


def t_and_c(request):
    return render(request, "terms_&_conditions.html")


def search(request):
    query = request.GET['query']
    if len(query) > 55:
        search_products = Book.objects.none()
    else:
        bk_title = Book.objects.filter(
            book_title__icontains=query)
        print(type(bk_title))
        bk_category = Book.objects.filter(
            book_category__icontains=query)
        id_course = Book.objects.filter(
            ideal_course__icontains=query)
        id_sem = Book.objects.filter(
            ideal_sem__icontains=query)
        pub_name = Book.objects.filter(
            publication_name__icontains=query)
        search_products = bk_category.union(
            bk_title, bk_category, id_course, id_sem, pub_name)

    if len(search_products) == 0:
        messages.warning(
            request, 'No search results. Please try different book.')
    context = {
        'query': query,    # key : value
        'products': search_products,
    }
    return render(request, "search.html", context)
    # return HttpResponse('Search is working')

class Myprofile(View):
    def get(self, *args, **kwargs):
        try:
            user = self.request.user
            pro = Profile.objects.get(user=user)
            context = {
                'user':user,
                'pro': pro,
            }
            return render(self.request,"my_profile.html", context)
        except ObjectDoesNotExist:
            messages.info(
                    self.request, "Your profile is not ready.")
            return redirect("/home")
    

def get_id(self):
    n = random.randint(0, 9)
    o = random.randint(11, 99)
    now = datetime.now()
    date = now.strftime("%d%m%Y")
    a = "OD" + date + str(n) + str(o)
    return a


class SellBook(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'sell_book.html')

    def post(self, *args, **kwargs):
        try:
            if self.request.user.is_authenticated:
                print(self.request)
                user = self.request.user
                bk_title = self.request.POST['bk_title']
                bk_pub = self.request.POST['bk_pub']
                bk_auth = self.request.POST['bk_auth']
                bk_edition = self.request.POST['bk_edition']
                bk_mrp = self.request.POST['bk_mrp']
                bk_stream = self.request.POST.get('bk_stream', False)
                id_course = self.request.POST['id_course']
                id_sem = self.request.POST['id_sem']
                usr_adr = self.request.POST['usr_adrs']
                usr_num = self.request.POST['usr_num']
                time = timezone.now()

                br = BookRequests.objects.create(user=user, address=usr_adr, contact_number=usr_num ,book_title=bk_title, book_mrp=bk_mrp, book_category=bk_stream, publication_name=bk_pub,
                                                 ideal_course=id_course, ideal_sem=id_sem, authors=bk_auth, edition=bk_edition, request_date=time)
                br.save()
                messages.info(
                    self.request, "Your request for selling a book is in process. Thank you")
                return redirect("/home")
            else:
                messages.info(
                    self.request, "Please login first.")
                return redirect("/profile/login")
        except ValueError:
            messages.warning(
                self.request, "Please fill all values correctly.")
            return redirect("/sell-book")
        except DataError:
            messages.warning(
                self.request, "Please fill all values correctly.")
            return redirect("/sell-book")


class BookDetailView(DetailView):    
    try:
        model = Book
        template_name = "plp.html"
    except MultipleObjectsReturned:
        messages.info(request, "Book is invalid.")
        template_name = "plp.html"


@csrf_protect
def add_to_cart(request, slug):
    if request.user.is_authenticated:
        product = get_object_or_404(Book, slug=slug)
        pro_quantity = int(request.POST.get('qnt', False))
        if product.book_stock >= pro_quantity:
            print('qnt is ok')
            order_product, created = OrderProduct.objects.get_or_create(
                product=product,
                user=request.user,
                ordered=False,
                product_quantity=pro_quantity
            )
            order_qs = Order.objects.filter(user=request.user, ordered=False)
            if order_qs.exists():
                order = order_qs[0]
                # Check if the order item is in the order
                if order.products.filter(product__slug=product.slug).exists():
                    order_product.product_quantity += pro_quantity
                    order_product.save()
                    messages.info(request, "The product quantity is updated.")
                else:
                    order.products.add(order_product)
                    messages.info(
                        request, "This product is added to your cart succesfully.")

            else:
                ordered_date = timezone.now()
                product_quantity = pro_quantity
                order = Order.objects.create(
                    user=request.user, ordered_date=ordered_date)
                order.products.add(order_product)
                messages.info(
                    request, "This product is added to your cart succesfully.")
            # "products:product" is saying products is the name of main url of app
            # product is the name of url who is calling the function (add_to_cart)
            return redirect("book:book_product", slug=slug)
        else:
            print('not ok')
            messages.info(
                request, f'There are only {product.book_stock} {product.book_title} left.')
            return redirect("book:book_product", slug=slug)
    else:
        messages.info(
            request, "Login first.")
        return redirect("book:home")

@login_required
def remove_from_cart(request, slug):
    product = get_object_or_404(Book, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # Check if the order item is in the order
        if order.products.filter(product__slug=product.slug).exists():
            order_product = OrderProduct.objects.filter(
                product=product,
                user=request.user,
                ordered=False
            )[0]            
            order.products.remove(order_product)           
            messages.info(
                request, "This book is removed from your cart succesfully.")
            return redirect("book:od-summary")
        else:
            # Add a message saying the order does not contain the item
            messages.info(request, "This book is not in your cart .")
            return redirect("book:od-summary")
    else:
        # Add a message saying the user doesn't have an order
        messages.info(request, "Your cart is empty.")
        return redirect("book:product", slug=slug)

class OrderSummaryView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(
                user=self.request.user, ordered=False)
            print(order)
            context = {
                'object': order,
            }
            print(order)
            return render(self.request, 'order_summary.html', context)
            # return HttpResponse('Hello')
        except ObjectDoesNotExist:
            messages.warning(self.request, "Your cart is empty.")
            return redirect("/home")


class Checkoutview(View):
    def get(self, *args, **kwargs):
        # form
        try:
            form = CheckoutForm()
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'form': form,
                'order': order
            }
            return render(self.request, "checkout.html", context)

        except ObjectDoesNotExist:
            return redirect("/home")

    def post(self, *args, **kwargs):
        # form
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            # payment = Payment.objects.get(user = self.request.user)
            if form.is_valid():
                address = form.cleaned_data.get('address')
                pin_code = form.cleaned_data.get('pin_code')
                phone_no = form.cleaned_data.get('contact_no')
                save_info = form.cleaned_data.get('save-info')
                refer_code = str(form.cleaned_data.get('refer_code')).upper()
                #refer_code2 = str(refer_code).upper()
                print(refer_code)
                print(form.cleaned_data)
                delievery_address = Address(
                    user=self.request.user,
                    address=address,
                    pin_code=pin_code,
                    contact_no=phone_no,
                    refer_code=refer_code
                )
                
                    
                delievery_address.save()
                order.delievery_address = delievery_address
                order.save()
                # return redirect('book:payment', payment_option='UPI')
                return redirect('book:payment', payment_option='UPI')
            else:
                messages.warning(
                    self.request, "Invalid option is selected.")
                return redirect("products:checkout")

        except ObjectDoesNotExist:
            messages.warning(self.request, "Your cart is empty.")
            return redirect("book:od-summary")


class PaymentView(View):
    def get(self, *args, **kwargs):
        try:
            # Form
            form = PaymentForm()
            # Order
            order = Order.objects.get(user=self.request.user, ordered=False)
            pro = Book.objects.all()
            for od in order.products.all():
                print(od.product.slug)
            context = {
                'form': form,
                'order': order,
                'pro': pro
            }
            return render(self.request, 'payment.html', context)
        except ObjectDoesNotExist:
            return redirect("/home")

    def post(self, *args, **kwargs):
        form = PaymentForm(self.request.POST)
        order = Order.objects.get(user=self.request.user, ordered=False)
        try:
            if form.is_valid():
                payment_option = form.cleaned_data.get('payment_option')
                payment_sender_name = form.cleaned_data.get(
                    'payment_sender_name')
                print(f"Payment Sender Name :- {payment_sender_name}")
                print(f"Payment option :- {payment_option}")
                payment = Payment(
                    user=self.request.user,
                    amount=order.total_od_price(),
                    payment_option=payment_option,
                    payment_sender_name=payment_sender_name
                )
                # Order zhali asel tar product chi quantity kami karayla.
                for od in order.products.all():
                    od.product.book_stock -= od.product_quantity
                    od.product.save()
                # Create payment here.
                payment.save()
                # Assign the payment to the order.
                order.payment = payment

                order.order_id = get_id(self)
                # pro.total_orders += order.products.product_quantity
                # order.i += 1
                order_products = order.products.all()
                order_products.update(ordered=True)
                #order.delievery_address.refer_code

                if order.delievery_address.refer_code:
                    a = Profile.objects.filter(refer_code = order.delievery_address.refer_code)
                    for i in a:
                        if self.request.user != i.user:
                            i.refer_order+=1
                            i.total_order+=1
                            i.save()

                order.ordered = True
                order.save()
                messages.info(
                    self.request, "Your order is succesfully placed.")
                return redirect("book:home")
            else:
                messages.warning(self.request, "Form is not filled properly.")
                return redirect("/")

        except ObjectDoesNotExist:
            messages.warning(self.request, "Invalid Credentials.")
            return redirect("book:checkout")


class MyorderView(View):

    def get(self, *args, **kwargs):
        try:
            c = list()
            order = Order.objects.filter(
                user_id=self.request.user.id, ordered=True, recieved=False).order_by('-start_date')
            for i in range(0, len(order)):
                b = order[i]
                print(b.get_total())
                c += b.products.all()
            print(f'Diff : {c}')

            mylist = list(zip(c, order))

            context = {
                'mylist': mylist,  # LIst of c and order
            }
            return render(self.request, 'my_ord1.html', context)
        except len(order) == 0:
            messages.warning(self.request, "Your cart is empty.")
            return redirect("/")

def cancel_order(request):
    form = RefundForm()
    od_id = request.POST['order_id']
    context = {
        'od_id': od_id,
        'form': form,
    }
    return render(request, "request_refund.html", context)

class RefundRequestView(View):
    def post(self, request, *args, **kwargs):
        form = RefundForm(self.request.POST)

        if form.is_valid():
            order_id = request.POST['order_id']
            message = form.cleaned_data.get('message')
            email = form.cleaned_data.get('email')
            # Edit the order
            try:
                order = Order.objects.get(order_id=order_id)
                order.refund_requested = True
                order.save()
                # Store the refund
                # refund = Refund()
                refund = Refund()
                refund.order = order
                refund.reason = message
                refund.email = email
                refund.save()
                messages.info(
                    self.request, "Your request is succesfully recieved.")
                return redirect("/my-orders/")

            except ObjectDoesNotExist:
                messages.info(self.request, "This order is not exist.")
                return redirect("/request-refund/")
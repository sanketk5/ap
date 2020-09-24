from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'book'

urlpatterns = [
    #path('', views.product, name='one'),
    path('', views.product, name='home'),
    path('home/', views.product, name='home'),
    path('about/', views.about, name='about'),
    path('my-profile/', views.Myprofile.as_view(), name='profile'),
    path('sell-book/', views.SellBook.as_view(), name='sell-book'),
    path('terms_and_conditions/', views.t_and_c, name='t_and_c'),
    path('search/', views.search, name='search'),
    path('book/<slug>/', views.BookDetailView.as_view(), name='book_product'),
    path('add-to-cart/<slug>', views.add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>',
         views.remove_from_cart, name='remove-from-cart'),
    path('order-summary/', views.OrderSummaryView.as_view(), name='od-summary'),
    path('checkout/', views.Checkoutview.as_view(), name='checkout'),
    path('payment/<payment_option>/', views.PaymentView.as_view(), name='payment'),
    path('cancel-order/', views.cancel_order, name='cancel-order'),
    path('request-refund/', views.RefundRequestView.as_view(), name='request-refund'),
    path('my-orders/', views.MyorderView.as_view(), name='my-orders'),
]
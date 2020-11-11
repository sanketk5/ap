from django.contrib import admin
from .models import Book, OrderProduct, Order, Address, Refund, Payment, BookRequests, Messages
# Register your models here.

def make_refund_accepted(modeladmin, request, quesryset):
    quesryset.update(refund_requested=False, refund_granted=True)


make_refund_accepted.short_description = "Update orders to refund granted"

class BookAdmin(admin.ModelAdmin):
    list_display = ('book_title', 'book_mrp',
                    'book_price', 'book_discount_price', 'book_stock',)
    list_display_links = ('book_title', )
    list_editable = ('book_mrp', 'book_price',
                     'book_discount_price', 'book_stock',)


class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('user', 'ordered', 'product')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_product', 'start_date', 'ordered', 'recieved', 'refund_requested', 'refund_granted',
                    'payment', 'delievery_address',)
    list_display_links = ('user', 'get_product', 'start_date')
    list_editable = ('ordered', 'recieved',)
    list_filter = ('ordered',)

    search_fields = ('user__username',)
    actions = [make_refund_accepted]


class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'pin_code', 'refer_code')
    list_filter = ('user', 'default',)
    search_fields = ['user', ]


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'timestamp',
                    'payment_option', 'payment_sender_name')

class BookRequestAdmin(admin.ModelAdmin):
    list_display = ('user','book_title', 'book_mrp','book_category','ideal_course', 'ideal_sem', 'publication_name', 'authors' ,'edition', 'book_status')
    list_editable = ('book_status',)

class RefundAdmin(admin.ModelAdmin):
    list_display = ('order', 'reason', 'email', 'accepted')
    list_editable = ('accepted',)

class MessagesAdmin(admin.ModelAdmin):
    list_display = ('contact_no', 'message', 'message_time')    

admin.site.site_header = "Aplepustak admin panel"
admin.site.site_title = "Log in to Aplepustak"
admin.site.index_title = "Welcome to the Aplepustak admin panel"
admin.site.register(Book, BookAdmin)
admin.site.register(BookRequests, BookRequestAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Refund, RefundAdmin)
admin.site.register(Messages, MessagesAdmin)

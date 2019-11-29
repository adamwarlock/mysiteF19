from django.contrib import admin
from .models import Publisher, Book, Member, Order, Review


# Register your models here.
class BookAdmin(admin.ModelAdmin):
    fields = [('title', 'category', 'publisher'), ('num_pages', 'price', 'num_reviews')]
    list_display = ('title', 'category', 'price')


class OrderAdmin(admin.ModelAdmin):
    fields = ['books', ('member', 'order_type', 'order_date')]
    list_display = ('id', 'member', 'order_type', 'order_date', 'total_items')


class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name', 'website', 'city', 'country')


admin.site.register(Publisher, PublisherAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Member)
admin.site.register(Order, OrderAdmin)
admin.site.register(Review)

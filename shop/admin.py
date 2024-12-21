from django.contrib import admin
from .models import Product, Cart, CartItem, Order, Rating, Address

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'average_rating']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer', 'product', 'quantity', 'status', 'created_at']
    list_filter = ['status']
    actions = ['mark_as_approved', 'mark_as_shipped', 'mark_as_delivered']

    def mark_as_approved(self, request, queryset):
        queryset.update(status='Approved')
    mark_as_approved.short_description = "Mark selected orders as Approved"

    def mark_as_shipped(self, request, queryset):
        queryset.update(status='Shipped')
    mark_as_shipped.short_description = "Mark selected orders as Shipped"

    def mark_as_delivered(self, request, queryset):
        queryset.update(status='Delivered')
    mark_as_delivered.short_description = "Mark selected orders as Delivered"

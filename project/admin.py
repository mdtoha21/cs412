"""Admin registrations for the FoodFlow project app."""
from django.contrib import admin
from .models import Customer, Restaurant, MenuItem, Order, OrderItem


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
	list_display = ('first_name', 'last_name', 'email', 'phone')
	search_fields = ('first_name', 'last_name', 'email')


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
	list_display = ('name', 'cuisine_type', 'phone_number')
	search_fields = ('name', 'cuisine_type')


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
	list_display = ('name', 'restaurant', 'price')
	list_filter = ('restaurant',)
	search_fields = ('name', 'description')


class OrderItemInline(admin.TabularInline):
	model = OrderItem
	extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_display = ('id', 'customer', 'restaurant', 'total_price', 'is_completed', 'order_date')
	list_filter = ('is_completed', 'restaurant')
	search_fields = ('customer__first_name', 'customer__last_name', 'restaurant__name')
	inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
	list_display = ('order', 'menu_item', 'quantity', 'item_subtotal')
	list_filter = ('menu_item__restaurant',)

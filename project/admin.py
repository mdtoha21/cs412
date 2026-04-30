"""Admin registrations for the FoodFlow project app."""
from django.contrib import admin
from .models import Customer, Restaurant, MenuItem, Order, OrderItem


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
	"""Admin configuration for browsing/searching customer profiles."""

	list_display = ('first_name', 'last_name', 'email', 'phone')
	search_fields = ('first_name', 'last_name', 'email')


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
	"""Admin configuration for restaurant records."""

	list_display = ('name', 'cuisine_type', 'phone_number')
	search_fields = ('name', 'cuisine_type')


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
	"""Admin configuration for menu items, grouped by restaurant."""

	list_display = ('name', 'restaurant', 'price')
	list_filter = ('restaurant',)
	search_fields = ('name', 'description')


class OrderItemInline(admin.TabularInline):
	"""Inline editor for order items within the parent order admin page."""

	model = OrderItem
	extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	"""Admin configuration for orders, including inline order items."""

	list_display = ('id', 'customer', 'restaurant', 'total_price', 'is_completed', 'order_date')
	list_filter = ('is_completed', 'restaurant')
	search_fields = ('customer__first_name', 'customer__last_name', 'restaurant__name')
	inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
	"""Admin configuration for order line-items and their subtotals."""

	list_display = ('order', 'menu_item', 'quantity', 'item_subtotal')
	list_filter = ('menu_item__restaurant',)

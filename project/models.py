"""Database models for FoodFlow customers, restaurants, menu items, and orders."""
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse


class Customer(models.Model):
	"""A delivery customer profile optionally linked to a Django `User`."""

	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	email = models.EmailField(unique=True)
	phone = models.CharField(max_length=30)
	address = models.TextField()

	def __str__(self):
		"""Return a human-friendly label for admin screens and logs."""
		return f'{self.first_name} {self.last_name}'


class Restaurant(models.Model):
	"""A restaurant that can receive orders and provides menu items."""

	name = models.CharField(max_length=200)
	address = models.TextField()
	phone_number = models.CharField(max_length=30)
	cuisine_type = models.CharField(max_length=100)
	image = models.ImageField(upload_to='project/restaurants/', blank=True)

	def __str__(self):
		"""Return the restaurant name for display purposes."""
		return self.name


class MenuItem(models.Model):
	"""A purchasable item belonging to exactly one restaurant."""

	restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menu_items')
	name = models.CharField(max_length=200)
	description = models.TextField()
	price = models.DecimalField(max_digits=10, decimal_places=2)
	image = models.ImageField(upload_to='project/menu_items/', blank=True)

	def __str__(self):
		"""Include restaurant name to disambiguate items across restaurants."""
		return f'{self.name} ({self.restaurant.name})'


class Order(models.Model):
	"""An order "cart" that becomes a completed purchase when finalized."""

	customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
	restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='orders', null=True, blank=True)
	order_date = models.DateTimeField(null=True, blank=True)
	total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
	delivery_address = models.TextField(null=True, blank=True)
	is_completed = models.BooleanField(default=False)

	def recalculate_total(self):
		"""Recompute `total_price` from associated `OrderItem` subtotals."""
		self.total_price = sum(item.item_subtotal for item in self.items.all())

	def get_absolute_url(self):
		"""Return the canonical URL for viewing this order."""
		return reverse('project:order_detail', kwargs={'pk': self.pk})

	def __str__(self):
		"""Return a label including the primary key and customer."""
		return f'Order #{self.pk} - {self.customer}'


class OrderItem(models.Model):
	"""A line item in an order with quantity and computed subtotal."""

	order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
	menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='order_items')
	quantity = models.PositiveIntegerField(default=1)
	item_subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)

	def clean(self):
		"""Validate cross-model consistency between the order and menu item."""
		if self.menu_item and self.order and self.menu_item.restaurant_id != self.order.restaurant_id:
			raise ValidationError('Menu item must belong to the same restaurant as the order.')

	def save(self, *args, **kwargs):
		"""
		Validate and persist the line item.

		We call `full_clean()` to enforce `clean()` constraints even when the model
		is created outside of a Django form. Subtotal is derived data and is stored
		so templates/admin can display it without recalculating each time.
		"""
		self.full_clean()
		self.item_subtotal = self.menu_item.price * self.quantity
		super().save(*args, **kwargs)

	def __str__(self):
		"""Return a compact label like 'Burger x2'."""
		return f'{self.menu_item.name} x{self.quantity}'

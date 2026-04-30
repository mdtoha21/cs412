"""Database models for FoodFlow customers, restaurants, menu items, and orders."""
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse


class Customer(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	email = models.EmailField(unique=True)
	phone = models.CharField(max_length=30)
	address = models.TextField()

	def __str__(self):
		return f'{self.first_name} {self.last_name}'


class Restaurant(models.Model):
	name = models.CharField(max_length=200)
	address = models.TextField()
	phone_number = models.CharField(max_length=30)
	cuisine_type = models.CharField(max_length=100)
	image = models.ImageField(upload_to='project/restaurants/', blank=True)

	def __str__(self):
		return self.name


class MenuItem(models.Model):
	restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menu_items')
	name = models.CharField(max_length=200)
	description = models.TextField()
	price = models.DecimalField(max_digits=10, decimal_places=2)
	image = models.ImageField(upload_to='project/menu_items/', blank=True)

	def __str__(self):
		return f'{self.name} ({self.restaurant.name})'


class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
	restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='orders', null=True, blank=True)
	order_date = models.DateTimeField(null=True, blank=True)
	total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
	delivery_address = models.TextField(null=True, blank=True)
	is_completed = models.BooleanField(default=False)

	def recalculate_total(self):
		self.total_price = sum(item.item_subtotal for item in self.items.all())

	def get_absolute_url(self):
		return reverse('project:order_detail', kwargs={'pk': self.pk})

	def __str__(self):
		return f'Order #{self.pk} - {self.customer}'


class OrderItem(models.Model):
	order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
	menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='order_items')
	quantity = models.PositiveIntegerField(default=1)
	item_subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)

	def clean(self):
		if self.menu_item and self.order and self.menu_item.restaurant_id != self.order.restaurant_id:
			raise ValidationError('Menu item must belong to the same restaurant as the order.')

	def save(self, *args, **kwargs):
		self.full_clean()
		self.item_subtotal = self.menu_item.price * self.quantity
		super().save(*args, **kwargs)

	def __str__(self):
		return f'{self.menu_item.name} x{self.quantity}'

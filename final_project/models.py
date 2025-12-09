from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    '''Represents a customer who can place orders.'''
    
    # Define the data attributes
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    address = models.TextField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_all_orders(self):
        '''Retrieve all orders made by this customer, ordered by most recent first.'''
        return self.orders.all().order_by('-order_date')
    
    def get_num_orders(self):
        """Return the number of orders made by this customer."""
        return self.orders.count()


class Restaurant(models.Model):
    '''Represents a restaurant that serves food.'''
    
    # Define the data attributes
    name = models.CharField(max_length=200)
    address = models.TextField()
    phone_number = models.CharField(max_length=20)
    cuisine_type = models.CharField(max_length=100)
    image = models.ImageField(upload_to='restaurant_images/', blank=True, null=True)

    def __str__(self):
        return self.name
    
    def get_all_menu_items(self):
        """Retrieve all menu items for this restaurant."""
        return self.menu_items.all()
    
    def get_num_menu_items(self):
        """Return the number of menu items for this restaurant."""
        return self.menu_items.count()
    
    def get_absolute_url(self):
        # Redirect back to the restaurant page
        return reverse('final_project:show_restaurant', args=[self.pk])


class MenuItem(models.Model):
    '''Represents a menu item offered by a restaurant.'''
    
    # Define the data attributes
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menu_items')
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='menu_images/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.restaurant.name}"
    
    def get_absolute_url(self):
        # Redirect back to the menu item page
        return reverse('final_project:show_menu_item', args=[self.pk])


class Order(models.Model):
    '''Represents an order placed by a customer at a restaurant.'''
    
    # Define the data attributes
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='orders')
    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    delivery_address = models.TextField(blank=True)

    def __str__(self):
        return f"Order #{self.id} by {self.customer}"
    
    def get_absolute_url(self):
        # Redirect back to the order page
        return reverse('final_project:show_order', args=[self.pk])
    
    def get_all_order_items(self):
        """Retrieve all order items for this order."""
        return self.order_items.all()
    
    def get_num_items(self):
        """Return the total number of items in this order."""
        return sum(item.quantity for item in self.order_items.all())
    
    def calculate_total(self):
        """Calculate the total price of all items in this order."""
        return sum(item.item_subtotal for item in self.order_items.all())


class OrderItem(models.Model):
    '''Represents an item in an order, linking a menu item with a quantity.'''
    
    # Define the data attributes
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    item_subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity}x {self.menu_item.name} (Order {self.order.id})"

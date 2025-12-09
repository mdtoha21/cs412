from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import Restaurant, MenuItem, Order, OrderItem, Customer
from .forms import AddToOrderForm, CompleteOrderForm, CreateCustomerForm, UpdateOrderItemForm, SearchRestaurantForm, CustomUserCreationForm

# ---------------- Mixins ----------------

class CustomerAccessMixin(LoginRequiredMixin):
    """Mixin to get the Customer object of the logged-in user."""
    login_url = '/final_project/login/'

    def get_customer(self):
        """Return the Customer object of the logged-in user."""
        customer = Customer.objects.filter(user=self.request.user).first()
        if not customer:
            # Create customer if it doesn't exist
            customer = Customer.objects.create(
                user=self.request.user,
                first_name=self.request.user.first_name or '',
                last_name=self.request.user.last_name or '',
                email=self.request.user.email or '',
                phone='',
                address=''
            )
        return customer


# ---------------- Restaurant Views ----------------

class RestaurantListView(ListView):
    """Show all restaurants."""
    model = Restaurant
    template_name = "final_project/show_all_restaurants.html"
    context_object_name = "restaurants"


class RestaurantDetailView(DetailView):
    """Show a restaurant and its menu items."""
    model = Restaurant
    template_name = "final_project/show_restaurant.html"
    context_object_name = "restaurant"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add menu items to context
        context['menu_items'] = self.object.menu_items.all()
        return context


class MenuItemDetailView(DetailView):
    """Show a single menu item."""
    model = MenuItem
    template_name = "final_project/show_menu_item.html"
    context_object_name = "menu_item"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add form to context for adding item to order
        context['form'] = AddToOrderForm()
        return context


# ---------------- Order Views ----------------

class AddToOrderView(CustomerAccessMixin, CreateView):
    """Add a menu item to the order."""
    model = OrderItem
    form_class = AddToOrderForm
    template_name = "final_project/add_to_order_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the menu item being added
        menu_item = get_object_or_404(MenuItem, pk=self.kwargs['pk'])
        context['menu_item'] = menu_item
        return context

    def form_valid(self, form):
        menu_item = get_object_or_404(MenuItem, pk=self.kwargs['pk'])
        restaurant = menu_item.restaurant
        customer = self.get_customer()
        
        # Get order_id from URL if provided (for continuing an existing order)
        order_id = self.kwargs.get('order_id')
        if order_id:
            order = get_object_or_404(Order, pk=order_id, customer=customer)
            # Make sure this order is still pending (not completed)
            if order.delivery_address:
                # Order was completed, create a new one
                order = None
        else:
            order = None
        
        # Check for pending order for this customer and restaurant
        # Only if not completed (has no delivery_address)
        if not order:
            order = Order.objects.filter(
                customer=customer,
                restaurant=restaurant,
                delivery_address=''  # Only pending orders (not completed)
            ).order_by('-order_date').first()
        
        # If no pending order exists, create a completely new order
        if not order:
            # Create new order for this customer
            order = Order.objects.create(
                customer=customer,
                restaurant=restaurant,
                total_price=0,
                delivery_address=''
            )
        
        # Create order item
        quantity = form.cleaned_data['quantity']
        item_subtotal = menu_item.price * quantity
        order_item = form.save(commit=False)
        order_item.order = order
        order_item.menu_item = menu_item
        order_item.item_subtotal = item_subtotal
        order_item.save()
        
        # Update order total
        order.total_price = sum(item.item_subtotal for item in order.order_items.all())
        order.save()
        
        self.object = order_item
        return redirect('final_project:show_order', pk=order.pk)


class OrderDetailView(CustomerAccessMixin, DetailView):
    """Show the current order."""
    model = Order
    template_name = "final_project/show_order.html"
    context_object_name = "order"

    def get_object(self):
        order = get_object_or_404(Order, pk=self.kwargs['pk'])
        customer = self.get_customer()
        # Make sure the order belongs to this customer
        if order.customer != customer:
            from django.http import Http404
            raise Http404("Order not found")
        return order

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add order items to context
        context['order_items'] = self.object.order_items.all()
        return context


class CompleteOrderView(CustomerAccessMixin, CreateView):
    """Complete the order by updating customer info and delivery address."""
    model = Customer
    form_class = CreateCustomerForm
    template_name = "final_project/complete_order_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = self.get_customer()
        order = get_object_or_404(Order, pk=self.kwargs['pk'], customer=customer)
        context['order'] = order
        # Add form for completing order
        context['order_form'] = CompleteOrderForm(instance=order)
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        customer = self.get_customer()
        order = get_object_or_404(Order, pk=self.kwargs['pk'], customer=customer)
        # Pre-populate form with existing customer data
        kwargs['instance'] = order.customer
        return kwargs

    def form_valid(self, form):
        customer = self.get_customer()
        order = get_object_or_404(Order, pk=self.kwargs['pk'], customer=customer)
        
        # Update customer info
        customer_obj = form.save()
        order.customer = customer_obj
        order.save()
        
        # Update order delivery address
        order_form = CompleteOrderForm(self.request.POST, instance=order)
        if order_form.is_valid():
            order_form.save()
        
        self.object = customer_obj
        return redirect('final_project:order_confirmation', pk=order.pk)


class OrderConfirmationView(CustomerAccessMixin, DetailView):
    """Show order confirmation after purchase."""
    model = Order
    template_name = "final_project/order_confirmation.html"
    context_object_name = "order"

    def get_object(self):
        order = get_object_or_404(Order, pk=self.kwargs['pk'])
        customer = self.get_customer()
        # Make sure the order belongs to this customer
        if order.customer != customer:
            from django.http import Http404
            raise Http404("Order not found")
        return order

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add order items to context
        context['order_items'] = self.object.order_items.all()
        return context


class UpdateOrderItemView(CustomerAccessMixin, UpdateView):
    """Update an order item (quantity)."""
    model = OrderItem
    form_class = UpdateOrderItemForm
    template_name = "final_project/update_order_item_form.html"

    def get_object(self):
        order_item = get_object_or_404(OrderItem, pk=self.kwargs['pk'])
        customer = self.get_customer()
        # Make sure the order belongs to this customer
        if order_item.order.customer != customer:
            from django.http import Http404
            raise Http404("Order item not found")
        return order_item

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add order to context
        context['order'] = self.object.order
        return context

    def form_valid(self, form):
        order_item = form.save(commit=False)
        # Recalculate subtotal based on new quantity
        quantity = form.cleaned_data['quantity']
        order_item.item_subtotal = order_item.menu_item.price * quantity
        order_item.save()
        
        # Update order total
        order = order_item.order
        order.total_price = sum(item.item_subtotal for item in order.order_items.all())
        order.save()
        
        return redirect('final_project:show_order', pk=order.pk)


class DeleteOrderItemView(CustomerAccessMixin, DeleteView):
    """Delete an order item from an order."""
    model = OrderItem
    template_name = "final_project/delete_order_item_form.html"
    context_object_name = "order_item"

    def get_object(self):
        order_item = get_object_or_404(OrderItem, pk=self.kwargs['pk'])
        customer = self.get_customer()
        # Make sure the order belongs to this customer
        if order_item.order.customer != customer:
            from django.http import Http404
            raise Http404("Order item not found")
        return order_item

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add order to context
        context['order'] = self.object.order
        return context

    def get_success_url(self):
        order = self.object.order
        # Update order total after deletion
        order.total_price = sum(item.item_subtotal for item in order.order_items.all())
        order.save()
        return reverse('final_project:show_order', args=[order.pk])


# ---------------- Search Views ----------------

class SearchRestaurantView(ListView):
    """Search and filter restaurants."""
    model = Restaurant
    template_name = "final_project/search_restaurants.html"
    context_object_name = "restaurants"

    def get_queryset(self):
        queryset = Restaurant.objects.all()
        query = self.request.GET.get('query', '')
        cuisine_type = self.request.GET.get('cuisine_type', '')
        
        # Filter by name or address if query provided
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | Q(address__icontains=query)
            )
        
        # Filter by cuisine type if provided
        if cuisine_type:
            queryset = queryset.filter(cuisine_type__icontains=cuisine_type)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add search form and query parameters to context
        context['form'] = SearchRestaurantForm(self.request.GET)
        context['query'] = self.request.GET.get('query', '')
        context['cuisine_type'] = self.request.GET.get('cuisine_type', '')
        return context


# ---------------- Customer Registration Views ----------------

class CreateCustomerView(CreateView):
    """Create a new customer account (registration)."""
    model = Customer
    form_class = CreateCustomerForm
    template_name = "final_project/create_customer_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add user creation form to context
        if self.request.method == 'POST':
            context['user_form'] = CustomUserCreationForm(self.request.POST)
        else:
            context['user_form'] = CustomUserCreationForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        user_form = CustomUserCreationForm(self.request.POST)
        
        # Validate both forms
        if form.is_valid() and user_form.is_valid():
            # Create the User first
            user = user_form.save()
            # Log the user in
            login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
            # Attach the user to the Customer instance
            form.instance.user = user
            # Set email from user if not provided
            if not form.instance.email:
                form.instance.email = user.email or user.username + '@example.com'
            return self.form_valid(form)
        else:
            # If either form is invalid, re-render with errors
            return self.form_invalid(form, user_form)

    def form_invalid(self, form, user_form=None):
        """Re-render the form with errors."""
        context = self.get_context_data(form=form)
        if user_form is not None:
            context['user_form'] = user_form
        return self.render_to_response(context)

    def get_success_url(self):
        # Redirect to restaurants after registration
        return reverse('final_project:show_all_restaurants')

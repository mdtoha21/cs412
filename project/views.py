"""Views for browsing restaurants, creating orders, and completing purchases."""
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.db import transaction
from django.utils import timezone
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView, View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .forms import OrderCreateForm, OrderItemForm, OrderUpdateForm, RegisterForm
from .models import Customer, MenuItem, Order, OrderItem, Restaurant


class HomeView(TemplateView):
    """Render the landing page and show recent orders for logged-in users."""
    template_name = 'project/home.html'

    def get_context_data(self, **kwargs):
        """Add the current user's recent orders to the home page context."""
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            try:
                customer = self.request.user.customer
                recent_orders = Order.objects.filter(customer=customer).select_related('restaurant').order_by('-order_date')[:5]
                context['recent_orders'] = recent_orders
            except Customer.DoesNotExist:
                context['recent_orders'] = []
        return context


class RegisterView(View):
    """Handle user registration and create the linked customer profile."""
    form_class = RegisterForm
    template_name = 'registration/register.html'
    
    def get(self, request):
        """Display the registration form."""
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        """Validate registration data and create a new user account."""
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.first_name}! Your account has been created.')
            return redirect('project:order_list')
        return render(request, self.template_name, {'form': form})


class CustomerListView(ListView):
    """Show all customer records."""
    model = Customer
    template_name = 'project/customer_list.html'
    context_object_name = 'customers'


class CustomerDetailView(DetailView):
    """Show a single customer's details."""
    model = Customer
    template_name = 'project/customer_detail.html'
    context_object_name = 'customer'


class RestaurantListView(ListView):
    """Display restaurants with optional name filtering."""
    model = Restaurant
    template_name = 'project/restaurant_list.html'
    context_object_name = 'restaurants'

    def get_queryset(self):
        """Filter restaurants by the optional search query."""
        queryset = Restaurant.objects.all()
        query = self.request.GET.get('q', '').strip()
        if query:
            queryset = queryset.filter(name__icontains=query)
        return queryset


class RestaurantDetailView(DetailView):
    """Show restaurant details."""
    model = Restaurant
    template_name = 'project/restaurant_detail.html'
    context_object_name = 'restaurant'


class MenuItemListView(ListView):
    """Display all menu items with their restaurants."""
    model = MenuItem
    template_name = 'project/menuitem_list.html'
    context_object_name = 'menu_items'

    def get_queryset(self):
        """Load menu items with related restaurant data."""
        return MenuItem.objects.select_related('restaurant')


class MenuItemDetailView(DetailView):
    """Show a single menu item's details."""
    model = MenuItem
    template_name = 'project/menuitem_detail.html'
    context_object_name = 'menu_item'


class OrderListView(ListView):
    """Show the logged-in user's orders."""
    model = Order
    template_name = 'project/order_list.html'
    context_object_name = 'orders'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        """Require authentication before accessing the order list."""
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        """Return only the current customer's orders."""
        try:
            customer = self.request.user.customer
        except Customer.DoesNotExist:
            messages.error(self.request, 'Please complete your profile before viewing orders.')
            return Order.objects.none()
        return Order.objects.filter(customer=customer).select_related('customer', 'restaurant').order_by('-id')


class OrderDetailView(DetailView):
    """Show a single order with its items and checkout actions."""
    model = Order
    template_name = 'project/order_detail.html'
    context_object_name = 'order'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        """Require authentication before accessing order details."""
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        """Add the item form for the current restaurant to the page context."""
        context = super().get_context_data(**kwargs)
        context['item_form'] = OrderItemForm(restaurant=self.object.restaurant)
        return context


class OrderUpdateView(UpdateView):
    """Update the delivery address for an order."""
    model = Order
    form_class = OrderUpdateForm
    template_name = 'project/order_update_form.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        """Require authentication before allowing order updates."""
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        """Restrict updates to the current customer's orders."""
        try:
            customer = self.request.user.customer
        except Customer.DoesNotExist:
            messages.error(self.request, 'Please complete your profile before updating orders.')
            return Order.objects.none()
        return Order.objects.filter(customer=customer)

    def form_valid(self, form):
        """Save the update and show a confirmation message."""
        response = super().form_valid(form)
        messages.success(self.request, 'Delivery address updated.')
        return response

    def get_success_url(self):
        """Return to the order detail page after updating."""
        return self.object.get_absolute_url()


class OrderDeleteView(DeleteView):
    """Delete one of the current customer's orders."""
    model = Order
    template_name = 'project/order_confirm_delete.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        """Require authentication before allowing order deletion."""
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        """Restrict deletions to the current customer's orders."""
        try:
            customer = self.request.user.customer
        except Customer.DoesNotExist:
            messages.error(self.request, 'Please complete your profile before deleting orders.')
            return Order.objects.none()
        return Order.objects.filter(customer=customer)

    def delete(self, request, *args, **kwargs):
        """Delete the order and show a success message."""
        messages.success(request, 'Order deleted.')
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        """Return to the order list after deletion."""
        return reverse_lazy('project:order_list')


class OrderCreateView(View):
    """Start a new open order for the current customer."""
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        """Require authentication before creating an order."""
        return super().dispatch(*args, **kwargs)
    
    def get(self, request):
        """Create an empty order and send the user to restaurant selection."""
        # Create empty order for this customer
        try:
            customer = request.user.customer
        except Customer.DoesNotExist:
            messages.error(request, 'Please complete your profile before creating an order.')
            return redirect('project:home')
        order = Order.objects.create(customer=customer)
        messages.success(request, 'Order started. Select a restaurant and add items.')
        return redirect('project:order_select_restaurant', pk=order.pk)


class OrderSelectRestaurantView(DetailView):
    """Let the customer choose a restaurant for the current order."""
    model = Order
    template_name = 'project/order_select_restaurant.html'
    context_object_name = 'order'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        """Require authentication before showing restaurant selection."""
        return super().dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        """Add searchable restaurants to the selection page."""
        context = super().get_context_data(**kwargs)
        restaurants = Restaurant.objects.all()
        query = self.request.GET.get('q', '').strip()
        if query:
            restaurants = restaurants.filter(name__icontains=query)
        context['restaurants'] = restaurants
        context['search_query'] = query
        return context


class OrderRestaurantMenuView(DetailView):
    """Show menu items for the selected restaurant inside the current order."""
    model = Order
    template_name = 'project/order_restaurant_menu.html'
    context_object_name = 'order'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        """Require authentication before showing restaurant menus."""
        return super().dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        """Add the selected restaurant and its menu items to the page context."""
        context = super().get_context_data(**kwargs)
        restaurant_id = self.kwargs.get('restaurant_id')
        context['restaurant'] = get_object_or_404(Restaurant, pk=restaurant_id)
        context['menu_items'] = MenuItem.objects.filter(restaurant_id=restaurant_id)
        return context


@login_required
def add_order_item(request, pk):
    """Add a menu item to an order from either the menu page or the order page."""
    order = get_object_or_404(Order, pk=pk)
    if order.is_completed:
        messages.error(request, 'Cannot add items to a completed order.')
        return redirect('project:order_detail', pk=order.pk)

    if request.method == 'POST':
        # Check if this is from restaurant menu (has menu_item_id) or order detail form
        menu_item_id = request.POST.get('menu_item_id')
        
        if menu_item_id:
            # Coming from restaurant menu page
            try:
                menu_item = MenuItem.objects.get(pk=menu_item_id)
                quantity = int(request.POST.get('quantity', 1))
                
                # Set restaurant if not set yet
                if not order.restaurant:
                    order.restaurant = menu_item.restaurant
                    order.save()
                
                # Only allow items from same restaurant
                if menu_item.restaurant != order.restaurant:
                    messages.error(request, 'You can only add items from the selected restaurant.')
                else:
                    order_item, created = OrderItem.objects.get_or_create(
                        order=order,
                        menu_item=menu_item,
                        defaults={'quantity': quantity},
                    )
                    if not created:
                        order_item.quantity += quantity
                        order_item.save()

                    order.recalculate_total()
                    order.save(update_fields=['total_price'])
                    messages.success(request, f'Added {menu_item.name} to order.')
            except MenuItem.DoesNotExist:
                messages.error(request, 'Menu item not found.')
        else:
            # Coming from order detail page (using OrderItemForm)
            form = OrderItemForm(request.POST, restaurant=order.restaurant)
            if form.is_valid():
                menu_item = form.cleaned_data['menu_item']
                quantity = form.cleaned_data['quantity']

                order_item, created = OrderItem.objects.get_or_create(
                    order=order,
                    menu_item=menu_item,
                    defaults={'quantity': quantity},
                )
                if not created:
                    order_item.quantity += quantity
                    order_item.save()

                order.recalculate_total()
                order.save(update_fields=['total_price'])
                messages.success(request, 'Item added to order.')

    return redirect('project:order_detail', pk=order.pk)


@login_required
def complete_order(request, pk):
    """Finalize the order and mark it as completed."""
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST' and not order.is_completed:
        order.recalculate_total()
        order.is_completed = True
        order.order_date = timezone.now()
        order.save(update_fields=['total_price', 'is_completed', 'order_date'])
        messages.success(request, 'Order marked as completed.')

    return redirect('project:order_detail', pk=order.pk)


@login_required
def reorder_order(request, pk):
    """Create a new open order from an existing completed or open order."""
    try:
        customer = request.user.customer
    except Customer.DoesNotExist:
        messages.error(request, 'Please complete your profile before reordering.')
        return redirect('project:home')
    source_order = get_object_or_404(Order, pk=pk, customer=customer)

    if not source_order.items.exists():
        messages.error(request, 'This order has no items to reorder.')
        return redirect('project:order_detail', pk=source_order.pk)

    with transaction.atomic():
        new_order = Order.objects.create(
            customer=source_order.customer,
            restaurant=source_order.restaurant,
            delivery_address=source_order.delivery_address,
            is_completed=False,
            order_date=None,
            total_price=0,
        )

        for item in source_order.items.select_related('menu_item'):
            OrderItem.objects.create(
                order=new_order,
                menu_item=item.menu_item,
                quantity=item.quantity,
            )

        new_order.recalculate_total()
        new_order.save(update_fields=['total_price'])

    messages.success(request, 'Reorder created. Review and press Complete Purchase.')
    return redirect('project:order_detail', pk=new_order.pk)


@login_required
def create_order_for_restaurant(request, restaurant_id):
    """Create a new open order for the logged-in customer with a restaurant selected."""
    try:
        customer = request.user.customer
    except Customer.DoesNotExist:
        messages.error(request, 'Please complete your profile before ordering.')
        return redirect('project:home')
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)

    # create a new open order for this customer with the restaurant set
    order = Order.objects.create(customer=customer, restaurant=restaurant)
    messages.success(request, f'Order started for {restaurant.name}. Add items to your cart.')

    return redirect('project:order_restaurant_menu', pk=order.pk, restaurant_id=restaurant.pk)

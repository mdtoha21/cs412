"""Forms for registering users and managing FoodFlow orders."""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Customer, MenuItem, Order, OrderItem


class RegisterForm(UserCreationForm):
    """Registration form that also creates a linked `Customer` profile."""

    first_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    last_name = forms.CharField(max_length=150, required=True, help_text='Required.')
    email = forms.EmailField(required=True, help_text='Required.')
    phone = forms.CharField(max_length=30, required=True, help_text='Phone number for deliveries.')
    address = forms.CharField(widget=forms.Textarea, required=True, help_text='Delivery address.')

    class Meta:
        """Configure which `User` fields are created from the form."""

        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def clean_email(self):
        """Enforce email uniqueness across both `User` and `Customer` records."""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already registered as a user.')
        if Customer.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already registered as a customer.')
        return email

    def save(self, commit=True):
        """
        Create a new `User` and (optionally) a linked `Customer` profile.

        The `Customer` stores delivery-specific fields that don't belong on the
        auth user model.
        """
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
            # Customer creation can fail independently (e.g. uniqueness); keep the
            # user account valid and surface the issue via logs for debugging.
            try:
                Customer.objects.create(
                    user=user,
                    first_name=self.cleaned_data['first_name'],
                    last_name=self.cleaned_data['last_name'],
                    email=self.cleaned_data['email'],
                    phone=self.cleaned_data['phone'],
                    address=self.cleaned_data['address']
                )
            except Exception as e:
                # Avoid raising here: the user account was created successfully.
                print(f"Warning: Failed to create Customer profile for {user.username}: {e}")
        
        return user


class OrderCreateForm(forms.ModelForm):
    """Form for collecting delivery details when creating an order."""

    class Meta:
        """Limit editable fields to delivery address."""
        model = Order
        fields = ['delivery_address']


class OrderUpdateForm(forms.ModelForm):
    """Form for editing an order's delivery details."""

    class Meta:
        """Limit editable fields to delivery address."""
        model = Order
        fields = ['delivery_address']


class OrderItemForm(forms.ModelForm):
    """Form for adding an item + quantity to an existing order."""

    class Meta:
        """Expose only the menu item selection and quantity."""
        model = OrderItem
        fields = ['menu_item', 'quantity']

    def __init__(self, *args, restaurant=None, **kwargs):
        """
        Initialize the form and scope menu-item choices to one restaurant.

        This prevents cross-restaurant ordering in a single cart.
        """
        super().__init__(*args, **kwargs)
        if restaurant is None:
            self.fields['menu_item'].queryset = MenuItem.objects.none()
        else:
            self.fields['menu_item'].queryset = MenuItem.objects.filter(restaurant=restaurant)

"""Forms for registering users and managing FoodFlow orders."""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Customer, MenuItem, Order, OrderItem


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    last_name = forms.CharField(max_length=150, required=True, help_text='Required.')
    email = forms.EmailField(required=True, help_text='Required.')
    phone = forms.CharField(max_length=30, required=True, help_text='Phone number for deliveries.')
    address = forms.CharField(widget=forms.Textarea, required=True, help_text='Delivery address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already registered as a user.')
        if Customer.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already registered as a customer.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
            # Create linked Customer profile
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
                # Log error but ensure user is created
                print(f"Warning: Failed to create Customer profile for {user.username}: {e}")
        
        return user


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['delivery_address']


class OrderUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['delivery_address']


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['menu_item', 'quantity']

    def __init__(self, *args, restaurant=None, **kwargs):
        super().__init__(*args, **kwargs)
        if restaurant is None:
            self.fields['menu_item'].queryset = MenuItem.objects.none()
        else:
            self.fields['menu_item'].queryset = MenuItem.objects.filter(restaurant=restaurant)

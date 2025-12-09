from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import OrderItem, Order, Customer, Restaurant

class CustomUserCreationForm(UserCreationForm):
    '''Custom UserCreationForm without password validation requirements.
    
    Only checks that passwords match'''
    
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove password help text
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''
    
    def clean_password2(self):
        """Only check that passwords match, skip all other password validation."""
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError("The two password fields didn't match.")
        # Don't call super() to skip Django's password validation
        return password2
    
    def _post_clean(self):
        """Override to skip password validation."""
        from django.forms.models import construct_instance
        from django.core.exceptions import ValidationError
        
        # Skip UserCreationForm's _post_clean which validates passwords
        # Just call ModelForm's _post_clean directly
        exclude = self._get_validation_exclusions()
        try:
            self.instance = construct_instance(self, self.instance, self.fields, exclude)
        except ValidationError as e:
            self._update_errors(e)
        
        try:
            self.instance.full_clean(exclude=exclude)
        except ValidationError as e:
            self._update_errors(e)

class AddToOrderForm(forms.ModelForm):
    '''Form to add a menu item to the order.'''
    
    class Meta:
        model = OrderItem
        fields = ['quantity']

class UpdateOrderItemForm(forms.ModelForm):
    '''Form to update an order item.'''
    
    class Meta:
        model = OrderItem
        fields = ['quantity']

class CompleteOrderForm(forms.ModelForm):
    '''Form to complete an order with customer information.'''
    
    class Meta:
        model = Order
        fields = ['delivery_address']

class CreateCustomerForm(forms.ModelForm):
    '''Form to create a customer.'''
    
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'phone', 'address']

class SearchRestaurantForm(forms.Form):
    '''Form to search restaurants.'''
    query = forms.CharField(max_length=200, required=False, label='Search')
    cuisine_type = forms.CharField(max_length=100, required=False, label='Cuisine Type')


from django.shortcuts import render
from datetime import datetime, timedelta
import random
# Create your views here.


def main(request):
    ''' 
    View for the main page of the restaurant.

    Renders the 'main.html' template, which displays:
    - Restaurant name
    - Location
    - Hours of operation
    - A photo of the restaurant
    '''
    
    return render(request, 'restaurant/main.html')


def order(request):
    '''View for the order page of the restaurant.

    Selects a daily special randomly from a predefined list of specials
    and passes it to the 'order.html' template. The template displays:
    - Menu items with checkboxes
    - The daily special
    - Fields for special instructions
    - Customer information form'''

    daily_specials = [
        {"name": "BBQ Chicken Pizza", "price": 14.99},
        {"name": "Spicy Shrimp Tacos", "price": 12.99},
        {"name": "Pasta Alfredo", "price": 11.99},
    ]

    daily_special = random.choice(daily_specials)

    context = {
        "daily_special": daily_special
    }

    return render(request, 'restaurant/order.html', context)

def confirmation(request):
    '''View to process the submitted order and display a confirmation page.

    Handles POST requests from the order form. It:
    - Checks which menu items were ordered
    - Calculates the total price of the order
    - Retrieves customer information (name, phone, email)
    - Retrieves any special instructions
    - Generates an estimated ready time (30-60 minutes from now)
    - Passes all information to 'confirmation.html' for display'''
    
    if request.method == "POST":
        menu = {
            "burger": 9.99,
            "pizza": 12.99,
            "salad": 7.99,
            "special": float(request.POST.get("special_price", 0))
        }

        ordered_items = []
        total_price = 0

        for item, price in menu.items():
            if request.POST.get(item):
                ordered_items.append(item)
                total_price += price

        # customer info
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        instructions = request.POST.get("instructions")

        ready_minutes = random.randint(30, 60)
        ready_time = datetime.now() + timedelta(minutes=ready_minutes)

        context = {
            "ordered_items": ordered_items,
            "total_price": total_price,
            "name": name,
            "phone": phone,
            "email": email,
            "instructions": instructions,
            "ready_time": ready_time.strftime("%I:%M %p"),
        }

        return render(request, 'restaurant/confirmation.html', context)

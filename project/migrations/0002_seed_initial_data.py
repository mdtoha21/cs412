"""Seed initial restaurants and menu items for the FoodFlow project app."""
from decimal import Decimal

from django.db import migrations
from django.utils import timezone


def seed_data(apps, schema_editor):
    Customer = apps.get_model('project', 'Customer')
    Restaurant = apps.get_model('project', 'Restaurant')
    MenuItem = apps.get_model('project', 'MenuItem')
    Order = apps.get_model('project', 'Order')
    OrderItem = apps.get_model('project', 'OrderItem')

    customers = [
        {
            'first_name': 'Ava',
            'last_name': 'Patel',
            'email': 'ava@example.com',
            'phone': '617-555-0101',
            'address': '12 Beacon St, Boston, MA',
        },
        {
            'first_name': 'Liam',
            'last_name': 'Nguyen',
            'email': 'liam@example.com',
            'phone': '617-555-0102',
            'address': '45 Comm Ave, Boston, MA',
        },
        {
            'first_name': 'Maya',
            'last_name': 'Lopez',
            'email': 'maya@example.com',
            'phone': '617-555-0103',
            'address': '88 Boylston St, Boston, MA',
        },
    ]

    restaurants = [
        {
            'name': 'Harbor Grill',
            'address': '100 Atlantic Ave, Boston, MA',
            'phone_number': '617-555-0201',
            'cuisine_type': 'American',
        },
        {
            'name': 'Roma Slice',
            'address': '250 Hanover St, Boston, MA',
            'phone_number': '617-555-0202',
            'cuisine_type': 'Italian',
        },
        {
            'name': 'Saffron Bowl',
            'address': '15 Newbury St, Boston, MA',
            'phone_number': '617-555-0203',
            'cuisine_type': 'Indian',
        },
    ]

    menu_items = [
        ('Harbor Grill', 'Classic Burger', 'Grilled beef, cheddar, lettuce, tomato.', Decimal('12.50')),
        ('Harbor Grill', 'Crispy Fries', 'Sea salt fries with garlic aioli.', Decimal('5.25')),
        ('Roma Slice', 'Margherita Pizza', 'Tomato sauce, mozzarella, basil.', Decimal('14.00')),
        ('Roma Slice', 'Penne Alfredo', 'Cream sauce with parmesan.', Decimal('13.50')),
        ('Saffron Bowl', 'Chicken Tikka Bowl', 'Basmati rice, tikka masala chicken.', Decimal('15.25')),
    ]

    customer_map = {}
    for data in customers:
        customer, _ = Customer.objects.get_or_create(email=data['email'], defaults=data)
        customer_map[data['email']] = customer

    restaurant_map = {}
    for data in restaurants:
        restaurant, _ = Restaurant.objects.get_or_create(name=data['name'], defaults=data)
        restaurant_map[data['name']] = restaurant

    menu_map = {}
    for restaurant_name, name, description, price in menu_items:
        menu_item, _ = MenuItem.objects.get_or_create(
            restaurant=restaurant_map[restaurant_name],
            name=name,
            defaults={'description': description, 'price': price},
        )
        menu_map[(restaurant_name, name)] = menu_item

    order_specs = [
        {
            'customer_email': 'ava@example.com',
            'restaurant_name': 'Harbor Grill',
            'delivery_address': '12 Beacon St, Boston, MA',
            'is_completed': True,
            'items': [('Classic Burger', 2), ('Crispy Fries', 1)],
        },
        {
            'customer_email': 'liam@example.com',
            'restaurant_name': 'Roma Slice',
            'delivery_address': '45 Comm Ave, Boston, MA',
            'is_completed': False,
            'items': [('Margherita Pizza', 1), ('Penne Alfredo', 1)],
        },
        {
            'customer_email': 'maya@example.com',
            'restaurant_name': 'Saffron Bowl',
            'delivery_address': '88 Boylston St, Boston, MA',
            'is_completed': True,
            'items': [('Chicken Tikka Bowl', 2)],
        },
    ]

    for spec in order_specs:
        order, _ = Order.objects.get_or_create(
            customer=customer_map[spec['customer_email']],
            restaurant=restaurant_map[spec['restaurant_name']],
            delivery_address=spec['delivery_address'],
            defaults={
                'total_price': Decimal('0.00'),
                'is_completed': spec['is_completed'],
                'order_date': timezone.now() if spec['is_completed'] else None,
            },
        )

        total_price = Decimal('0.00')
        for menu_name, quantity in spec['items']:
            menu_item = menu_map[(spec['restaurant_name'], menu_name)]
            subtotal = menu_item.price * quantity
            OrderItem.objects.get_or_create(
                order=order,
                menu_item=menu_item,
                defaults={'quantity': quantity, 'item_subtotal': subtotal},
            )
            total_price += subtotal

        order.total_price = total_price
        if spec['is_completed'] and not order.order_date:
            order.order_date = timezone.now()
        order.save()


def unseed_data(apps, schema_editor):
    Customer = apps.get_model('project', 'Customer')
    Restaurant = apps.get_model('project', 'Restaurant')
    Customer.objects.filter(email__in=['ava@example.com', 'liam@example.com', 'maya@example.com']).delete()
    Restaurant.objects.filter(name__in=['Harbor Grill', 'Roma Slice', 'Saffron Bowl']).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_data, reverse_code=unseed_data),
    ]

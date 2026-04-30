"""Generate placeholder images for restaurants and menu items."""
from django.db import migrations
from django.core.files.base import ContentFile
from PIL import Image
from io import BytesIO


def add_images(apps, schema_editor):
    Restaurant = apps.get_model('project', 'Restaurant')
    MenuItem = apps.get_model('project', 'MenuItem')
    
    # Color mapping for restaurants
    restaurant_colors = {
        'Harbor Grill': '#D4753D',      # Orange/brown
        'Roma Slice': '#C41E3A',        # Italian red
        'Saffron Bowl': '#FFC72C',      # Golden/saffron
    }
    
    # Add images to restaurants if they don't have one
    for restaurant in Restaurant.objects.all():
        if not restaurant.image:
            # Create a simple colored image
            color = restaurant_colors.get(restaurant.name, '#808080')
            rgb = tuple(int(color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
            
            img = Image.new('RGB', (400, 300), rgb)
            img_io = BytesIO()
            img.save(img_io, 'JPEG', quality=85)
            img_io.seek(0)
            
            filename = f'{restaurant.name.lower().replace(" ", "_")}.jpg'
            restaurant.image.save(filename, ContentFile(img_io.getvalue()), save=True)
    
    # Color mapping for menu items by restaurant
    menu_item_colors = {
        ('Harbor Grill', 'Classic Burger'): '#8B4513',      # Brown
        ('Harbor Grill', 'Crispy Fries'): '#FFD700',         # Gold
        ('Roma Slice', 'Margherita Pizza'): '#FF6B6B',       # Red
        ('Roma Slice', 'Penne Alfredo'): '#F0E68C',          # Khaki
        ('Saffron Bowl', 'Chicken Tikka Bowl'): '#FF8C00',   # Dark orange
    }
    
    # Add images to menu items if they don't have one
    for menu_item in MenuItem.objects.all():
        if not menu_item.image:
            key = (menu_item.restaurant.name, menu_item.name)
            color = menu_item_colors.get(key, '#A9A9A9')
            rgb = tuple(int(color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
            
            img = Image.new('RGB', (300, 250), rgb)
            img_io = BytesIO()
            img.save(img_io, 'JPEG', quality=85)
            img_io.seek(0)
            
            filename = f'{menu_item.name.lower().replace(" ", "_")}.jpg'
            menu_item.image.save(filename, ContentFile(img_io.getvalue()), save=True)


def remove_images(apps, schema_editor):
    Restaurant = apps.get_model('project', 'Restaurant')
    MenuItem = apps.get_model('project', 'MenuItem')
    
    for restaurant in Restaurant.objects.all():
        if restaurant.image:
            restaurant.image.delete(save=True)
    
    for menu_item in MenuItem.objects.all():
        if menu_item.image:
            menu_item.image.delete(save=True)


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0005_alter_order_delivery_address_alter_order_restaurant'),
    ]

    operations = [
        migrations.RunPython(add_images, remove_images),
    ]

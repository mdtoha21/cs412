"""Remove generated placeholder images from restaurant and menu item records."""
# Generated migration to remove auto-generated images
from django.db import migrations
import os

def remove_images(apps, schema_editor):
    """Remove all auto-generated images from food ordering app"""
    Restaurant = apps.get_model('project', 'Restaurant')
    MenuItem = apps.get_model('project', 'MenuItem')
    
    # Remove restaurant images
    for restaurant in Restaurant.objects.all():
        if restaurant.image:
            try:
                if os.path.isfile(restaurant.image.path):
                    os.remove(restaurant.image.path)
                restaurant.image.delete(save=True)
            except Exception as e:
                print(f"Error deleting restaurant image: {e}")
    
    # Remove menu item images
    for item in MenuItem.objects.all():
        if item.image:
            try:
                if os.path.isfile(item.image.path):
                    os.remove(item.image.path)
                item.image.delete(save=True)
            except Exception as e:
                print(f"Error deleting menu item image: {e}")

def noop(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('project', '0006_add_restaurant_and_menu_images'),
    ]

    operations = [
        migrations.RunPython(remove_images, noop),
    ]

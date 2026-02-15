# Generated data migration - sample profiles for mini_insta

from django.db import migrations


def create_sample_profiles(apps, schema_editor):
    Profile = apps.get_model('mini_insta', 'Profile')
    Profile.objects.bulk_create([
        Profile(
            username='alice',
            display_name='Alice Smith',
            profile_image_url='https://picsum.photos/seed/alice/80/80',
            bio_text='Hello, I love photography!',
        ),
        Profile(
            username='bob',
            display_name='Bob Jones',
            profile_image_url='https://picsum.photos/seed/bob/80/80',
            bio_text='Developer and coffee enthusiast.',
        ),
        Profile(
            username='charlie',
            display_name='Charlie Brown',
            profile_image_url='',
            bio_text='Just another user on the internet.',
        ),
    ])


def remove_sample_profiles(apps, schema_editor):
    Profile = apps.get_model('mini_insta', 'Profile')
    Profile.objects.filter(
        username__in=['alice', 'bob', 'charlie']
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('mini_insta', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_sample_profiles, remove_sample_profiles),
    ]

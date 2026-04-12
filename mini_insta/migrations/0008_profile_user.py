from django.conf import settings
from django.db import migrations, models


def assign_profile_users(apps, schema_editor):
    Profile = apps.get_model('mini_insta', 'Profile')
    User = apps.get_model('auth', 'User')

    # First pass: exact username match.
    for profile in Profile.objects.filter(user__isnull=True):
        matched_user = User.objects.filter(username=profile.username).first()
        if matched_user:
            profile.user = matched_user
            profile.save(update_fields=['user'])

    # Fallback: assign any remaining profiles to the first available user.
    fallback_user = User.objects.order_by('id').first()
    if fallback_user:
        Profile.objects.filter(user__isnull=True).update(user=fallback_user)


class Migration(migrations.Migration):

    dependencies = [
        ('mini_insta', '0007_like'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.RunPython(assign_profile_users, migrations.RunPython.noop),
    ]

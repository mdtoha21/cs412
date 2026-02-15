from django.views.generic import ListView
from .models import Profile


class ProfileListView(ListView):
    """Display all Profile records."""
    model = Profile
    template_name = 'mini_insta/show_all_profiles.html'
    context_object_name = 'profile_list'

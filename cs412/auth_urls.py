"""Authentication URL patterns with prefix-aware login/logout redirects."""

from django.urls import include, path

from .auth_views import MountedLoginView, MountedLogoutView

app_name = 'auth'

urlpatterns = [
    path('login/', MountedLoginView.as_view(), name='login'),
    path('logout/', MountedLogoutView.as_view(), name='logout'),
    path('', include('django.contrib.auth.urls')),
]

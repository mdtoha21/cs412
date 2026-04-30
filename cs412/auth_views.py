"""Custom authentication views that preserve deployment path prefixes."""

from django.contrib.auth import views as auth_views
from django.urls import reverse


def _mount_prefix_from_request(request):
    """Return URL mount prefix (e.g., '/mdtoha') when app is hosted under a subpath."""
    marker = '/accounts/'
    path = request.path or ''

    marker_index = path.find(marker)
    if marker_index > 0:
        return path[:marker_index]

    script_name = (request.META.get('SCRIPT_NAME') or '').rstrip('/')
    return script_name


def _with_mount_prefix(request, url):
    """Prefix absolute URLs with the detected mount prefix when needed."""
    if not url or not isinstance(url, str):
        return url

    if url.startswith('http://') or url.startswith('https://'):
        return url

    prefix = _mount_prefix_from_request(request)
    if not prefix:
        return url

    if not url.startswith('/'):
        return url

    if url == prefix or url.startswith(f'{prefix}/'):
        return url

    return f'{prefix}{url}'


class MountedLoginView(auth_views.LoginView):
    """Login view that redirects with deployment prefix awareness."""

    def get_success_url(self):
        return _with_mount_prefix(self.request, super().get_success_url())


class MountedLogoutView(auth_views.LogoutView):
    """Logout view that redirects with deployment prefix awareness."""

    def get_next_page(self):
        next_page = super().get_next_page()
        if next_page:
            return _with_mount_prefix(self.request, next_page)
        return _with_mount_prefix(self.request, reverse('project:home'))

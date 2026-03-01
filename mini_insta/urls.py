from django.urls import path
from .views import ProfileListView, ProfileDetailView,PostDetailView,CreatePostView,UpdateProfileView

urlpatterns = [
    path('', ProfileListView.as_view(), name='show_all_profiles'),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='show_profile'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='show_post'),
    path('profile/<int:pk>/create_post/', CreatePostView.as_view(), name='create_post'),
    path('profile/<int:pk>/update/', UpdateProfileView.as_view(), name='update_profile'),
]


from django.urls import path
from django.conf import settings
from . import views

from .views import ProfileListView, ProfileDetailView,PostDetailView

urlpatterns=[

path('', ProfileListView.as_view(), name='show_all_profiles'),

 path('profile/<int:pk>/', ProfileDetailView.as_view(), name='show_profile'),
 path('post/<int:pk>/', PostDetailView.as_view(), name='show_post'),
 path('profile/<int:pk>/create_post/', views.CreatePostView.as_view(), name='create_post'),
 path('profile/<int:pk>/update/', views.UpdateProfileView.as_view(), name='update_profile'),
 path('post/<int:pk>/update', views.UpdatePostView.as_view(), name='update_post'),
path('post/<int:pk>/delete', views.DeletePostView.as_view(), name='delete_post'),

] 
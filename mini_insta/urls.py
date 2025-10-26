
from django.urls import path
from django.conf import settings
from . import views

from .views import ProfileListView, ProfileDetailView,PostDetailView

urlpatterns=[

path('', ProfileListView.as_view(), name='show_all_profiles'),

 path('profile/<int:pk>/', ProfileDetailView.as_view(), name='show_profile'),
 path('post/<int:pk>/', PostDetailView.as_view(), name='show_post'),

 path('profile/', views.LoggedInProfileDetailView.as_view(), name='show_logged_in_profile'),
 path('profile/create_post/', views.CreatePostView.as_view(), name='create_post'),
 path('profile/update/', views.UpdateProfileView.as_view(), name='update_profile'),
 path('post/update', views.UpdatePostView.as_view(), name='update_post'),
path('post/delete', views.DeletePostView.as_view(), name='delete_post'),


path('profile/<int:pk>/followers', views.ShowFollowersDetailView.as_view(), name='show_followers'),
path('profile/<int:pk>/following', views.ShowFollowingDetailView.as_view(), name='show_following'),
path('profile/<int:pk>/feed', views.PostFeedListView.as_view(), name='show_feed'),
path('profile/<int:pk>/search', views.SearchView.as_view(), name='search'),

] 
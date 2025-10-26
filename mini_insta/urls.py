
from django.urls import path
from django.conf import settings
from . import views
from django.contrib.auth import views as auth_views
from .views import ProfileListView, ProfileDetailView,PostDetailView
from .views import LogoutConfirmationView
from .views import DeletePostView

from .forms import CreateProfileForm
urlpatterns=[

path('', ProfileListView.as_view(), name='show_all_profiles'),

 path('profile/<int:pk>/', ProfileDetailView.as_view(), name='show_profile'),
 path('post/<int:pk>/', PostDetailView.as_view(), name='show_post'),

 path('profile/', views.LoggedInProfileDetailView.as_view(), name='show_logged_in_profile'),
 path('profile/create_post/', views.CreatePostView.as_view(), name='create_post'),
 path('profile/update/', views.UpdateProfileView.as_view(), name='update_profile'),
 path('post/update', views.UpdatePostView.as_view(), name='update_post'),
path('post/<int:pk>/delete', views.DeletePostView.as_view(), name='delete_post'),


path('profile/<int:pk>/followers', views.ShowFollowersDetailView.as_view(), name='show_followers'),
path('profile/<int:pk>/following', views.ShowFollowingDetailView.as_view(), name='show_following'),
path('profile/<int:pk>/feed', views.PostFeedListView.as_view(), name='show_feed'),
path('profile/<int:pk>/search', views.SearchView.as_view(), name='search'),



path('login/', auth_views.LoginView.as_view(template_name='mini_insta/login.html'), name='login'),
 path('logout/', auth_views.LogoutView.as_view(), name='logout'),
  path('logout/confirmation/', LogoutConfirmationView.as_view(template_name='mini_insta/logged_out.html'), name='logout_confirmation'),
path('create_profile/', views.CreateProfileView.as_view(), name='create_profile'),

] 
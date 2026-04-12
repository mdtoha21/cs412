from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from .views import ProfileListView, ProfileDetailView,PostDetailView,CreatePostView,UpdateProfileView,UpdatePostView,DeletePostView,ShowFollowersDetailView,ShowFollowingDetailView
from . import views
from . import api_views
urlpatterns = [
    path('', ProfileListView.as_view(), name='show_all_profiles'),
    path('profile/', views.MyProfileView.as_view(), name='show_my_profile'),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='show_profile'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='show_post'),
    path('profile/create_post/', CreatePostView.as_view(), name='create_post'),
    path('profile/update/', UpdateProfileView.as_view(), name='update_profile'),
    path('post/<int:pk>/update', UpdatePostView.as_view(), name='update_post'),
    path('post/<int:pk>/delete', DeletePostView.as_view(), name='delete_post'),
    path('profile/<int:pk>/followers', ShowFollowersDetailView.as_view(), name='show_followers'),
    path('profile/<int:pk>/following', ShowFollowingDetailView.as_view(), name='show_following'),
    path('profile/feed', views.PostFeedListView.as_view(), name='show_feed'),
    path('profile/search', views.SearchView.as_view(), name='search'),
    path('profile/<int:pk>/follow', views.FollowProfileView.as_view(), name='follow_profile'),
    path('profile/<int:pk>/delete_follow', views.DeleteFollowProfileView.as_view(), name='delete_follow_profile'),
    path('post/<int:pk>/like', views.LikePostView.as_view(), name='like_post'),
    path('post/<int:pk>/delete_like', views.DeleteLikePostView.as_view(), name='delete_like_post'),
    path('login/', auth_views.LoginView.as_view(template_name='mini_insta/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='logout_confirmation'), name='logout'),
    path('logout_confirmation/', TemplateView.as_view(template_name='mini_insta/logged_out.html'), name='logout_confirmation'),
    path('create_profile', views.CreateProfileView.as_view(), name='create_profile'),
    path('api/login/', api_views.api_login, name='api_login'),
    path('api/profiles/', api_views.api_profiles, name='api_profiles'),
    path('api/profiles/<int:pk>/', api_views.api_profile_detail, name='api_profile_detail'),
    path('api/profiles/<int:pk>/posts/', api_views.api_profile_posts, name='api_profile_posts'),
    path('api/profiles/<int:pk>/feed/', api_views.api_profile_feed, name='api_profile_feed'),
    path('api/me/', api_views.api_my_profile, name='api_my_profile'),
    path('api/me/posts/', api_views.api_my_posts, name='api_my_posts'),
    path('api/me/feed/', api_views.api_my_feed, name='api_my_feed'),
    path('api/posts/', api_views.api_create_post, name='api_create_post'),
]

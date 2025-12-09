from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'final_project'

urlpatterns = [
    # Restaurant views
    path('', views.RestaurantListView.as_view(), name='show_all_restaurants'),
    path('restaurant/<int:pk>/', views.RestaurantDetailView.as_view(), name='show_restaurant'),
    path('menu_item/<int:pk>/', views.MenuItemDetailView.as_view(), name='show_menu_item'),
    
    # Order views
    path('add_to_order/<int:pk>/', views.AddToOrderView.as_view(), name='add_to_order'),
    path('order/<int:pk>/', views.OrderDetailView.as_view(), name='show_order'),
    path('complete_order/<int:pk>/', views.CompleteOrderView.as_view(), name='complete_order'),
    path('order_confirmation/<int:pk>/', views.OrderConfirmationView.as_view(), name='order_confirmation'),
    
    # Order item views (Update and Delete)
    path('update_order_item/<int:pk>/', views.UpdateOrderItemView.as_view(), name='update_order_item'),
    path('delete_order_item/<int:pk>/', views.DeleteOrderItemView.as_view(), name='delete_order_item'),
    
    # Search view
    path('search/', views.SearchRestaurantView.as_view(), name='search_restaurants'),
    
    # Authentication views
    path('login/', auth_views.LoginView.as_view(template_name='final_project/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='final_project:show_all_restaurants'), name='logout'),
    path('register/', views.CreateCustomerView.as_view(), name='register'),
]


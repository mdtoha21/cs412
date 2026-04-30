"""URL routes for the FoodFlow project app."""
from django.urls import path

from . import views

app_name = 'project'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('customers/', views.CustomerListView.as_view(), name='customer_list'),
    path('customers/<int:pk>/', views.CustomerDetailView.as_view(), name='customer_detail'),
    path('restaurants/', views.RestaurantListView.as_view(), name='restaurant_list'),
    path('restaurants/<int:pk>/', views.RestaurantDetailView.as_view(), name='restaurant_detail'),
    path('menu-items/', views.MenuItemListView.as_view(), name='menuitem_list'),
    path('menu-items/<int:pk>/', views.MenuItemDetailView.as_view(), name='menuitem_detail'),
    path('orders/', views.OrderListView.as_view(), name='order_list'),
    path('orders/create/', views.OrderCreateView.as_view(), name='order_create'),
    path('orders/<int:pk>/select-restaurant/', views.OrderSelectRestaurantView.as_view(), name='order_select_restaurant'),
    path('orders/<int:pk>/restaurant/<int:restaurant_id>/menu/', views.OrderRestaurantMenuView.as_view(), name='order_restaurant_menu'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('orders/<int:pk>/edit/', views.OrderUpdateView.as_view(), name='order_update'),
    path('orders/<int:pk>/delete/', views.OrderDeleteView.as_view(), name='order_delete'),
    path('orders/<int:pk>/add-item/', views.add_order_item, name='add_order_item'),
    path('orders/<int:pk>/complete/', views.complete_order, name='complete_order'),
    path('orders/create/restaurant/<int:restaurant_id>/', views.create_order_for_restaurant, name='order_create_for_restaurant'),
    path('orders/<int:pk>/reorder/', views.reorder_order, name='reorder_order'),
]

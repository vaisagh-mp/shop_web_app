from django.urls import path
from . import views

urlpatterns = [
    # Admin Views
    path('admin_home/', views.admin_home, name='admin_home'),
    path('admin_home/view_all_products/', views.view_all_products, name='view_all_products'),
    path('admin_home/add_product/', views.add_product, name='add_product'),
    path('admin_home/edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('admin_home/delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('admin_home/view_orders/', views.view_orders, name='view_orders'),
    path('order/<int:order_id>/update_status/', views.update_order_status, name='update_order_status'),

    # Customer Views
    path('', views.home, name='home'),  # Home page, redirects based on authentication
    path('customer/home/', views.customer_home, name='customer_home'),
    path('customer/add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('customer/view_cart/', views.view_cart, name='view_cart'),
    path('customer/place_order/', views.place_order, name='place_order'),
    path('customer/view_orders/', views.view_orders_customer, name='view_orders_customer'),
    path('customer/order/<int:order_id>/', views.view_order_details, name='view_order_details'),
    path('customer/rate_product/<int:product_id>/', views.rate_product, name='rate_product'),

    # Auth Views (Login, Logout, Registration)
    path('register/', views.register_employee, name='register'),  # User registration
    path('login/', views.custom_login, name='custom-login'),  # Custom login page
    path('logout/', views.custom_logout, name='custom-logout'),  # Logout view
]

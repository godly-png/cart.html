from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    # Products
    path('', views.product_list, name='product_list'),
    path('product/<int:product_id>/', views.product_details, name='product_details'),

    # Cart
    path('cart/', views.cart, name='cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update_from_cart/<int:cart_item_id>/', views.update_from_cart, name='update_from_cart'),

     path('login/', views.login_view, name='login'),
     path('register/', views.register_view, name='register'),
     path('dashboard/', views.dashboard_view, name='dashboard'),
      path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),


    # Auth
    # path('register/', views.register_view, name='register'),
    # path('login/', views.login_view, name='login'),
    # path('dashboard/', views.dashboard_view, name='dashboard'),
    # path('logout/', views.logout_view, name='logout'),

    # Billing + Orders
    # path('billing/', views.billing_page, name='billing'),
    # path('place-order/', views.place_order, name='place_order'),




    # Summary page (correct)
    # path('summary/<int:order_id>/', views.summary, name='summary'),




    path('checkout/', views.checkout, name='checkout'),

   


  
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    
  
    path('checkout-success/<int:order_id>/', views.checkout_success, name='checkout_success'),

    

]



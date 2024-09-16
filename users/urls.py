from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_user, name='register_user'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    path('category/<int:category_id>/', views.category_products_view, name='category_products'),
    path('product/<int:product_id>/', views.product_detail_view, name='product_detail'),
    path('cart/', views.cart_view, name='cart_view'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('checkout/', views.checkout_view, name='checkout_view'),

    path('shop/', views.shop_view, name='shop_view'),
    path('contact/', views.contact_view, name='contact_view'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart_byID, name='add_to_cart'),

    path('remove-item/<int:item_id>/', views.remove_item_from_cart, name='remove-item'),
    path('cart-item-count/', views.cart_item_count, name='cart-item-count'),
]

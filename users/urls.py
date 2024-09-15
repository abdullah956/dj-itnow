from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_user, name='register_user'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('product/<int:product_id>/', views.product_detail_view, name='product_detail'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
]

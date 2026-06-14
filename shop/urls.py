from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import (
    ProductViewSet, CategoryViewSet, ManufacturerViewSet,
    CartViewSet, CartItemViewSet, RegisterView, LoginView, LogoutView, MeView
)

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='api-products')
router.register(r'categories', CategoryViewSet, basename='api-categories')
router.register(r'manufacturers', ManufacturerViewSet, basename='api-manufacturers')
router.register(r'carts', CartViewSet, basename='api-carts')
router.register(r'cart-items', CartItemViewSet, basename='api-cart-items')

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about_shop, name='about'),
    path('author/', views.about_author, name='author'),
    path('catalog/', views.catalog, name='catalog'),
    path('catalog/<int:pk>/', views.product_detail, name='product_detail'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('checkout/', views.checkout, name='checkout'),
    path('profile/', views.profile_view, name='profile'),
    
    path('api/', include(router.urls)),
    path('api/register/', RegisterView.as_view(), name='api-register'),
    path('api/login/', LoginView.as_view(), name='api-login'),
    path('api/logout/', LogoutView.as_view(), name='api-logout'),
    path('api/me/', MeView.as_view(), name='api-me'),
]
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, ProductsViewSet, CartViewSet

app_name = 'api'

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='categories')
router.register('products', ProductsViewSet, basename='products')
router.register('cart', CartViewSet, basename='cart')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]

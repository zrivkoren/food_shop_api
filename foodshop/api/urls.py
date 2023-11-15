from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet

app_name = 'api'

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='categories')

urlpatterns = [
    path('', include(router.urls)),
]

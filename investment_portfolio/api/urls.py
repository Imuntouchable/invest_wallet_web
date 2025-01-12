from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, AssetViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'assets', AssetViewSet, basename='asset')

urlpatterns = [
    path('', include(router.urls)),
]

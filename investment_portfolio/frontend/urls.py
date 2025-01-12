from django.urls import path
from .views import register, login, profile, logout_view, add_asset, delete_asset

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/<int:user_id>/', profile, name='profile'),
    path('delete_asset/<int:user_id>/<int:asset_id>/', delete_asset, name='delete_asset'),
    path('add_asset/<int:user_id>/', add_asset, name='add_asset'),
]

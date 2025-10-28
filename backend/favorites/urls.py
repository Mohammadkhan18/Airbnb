from django.urls import path
from .views import toggle_favorite

urlpatterns = [
    path('<str:listing_id>/', toggle_favorite, name='toggle_favorite'),
]

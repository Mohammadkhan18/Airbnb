from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_listing, name='create-listing'),
    path('<str:listing_id>/', views.delete_listing, name='delete-listing'),
]

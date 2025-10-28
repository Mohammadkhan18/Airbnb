from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_reservation, name='create_reservation'),
    path('<str:reservation_id>/', views.delete_reservation, name='delete_reservation'),
]

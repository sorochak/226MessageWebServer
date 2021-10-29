from django.urls import path
from . import views

urlpatterns = [
    path('get/<int:key>/', views.get_message, name='message'),
]
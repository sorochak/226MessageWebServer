from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get/<str:key>/', views.get_message, name='message'),
    path('create/', views.MessageCreate.as_view(), name='message_create'),
    path('update/<str:key>/', views.MessageUpdate.as_view(), name='message_update'),
]
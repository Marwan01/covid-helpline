from django.contrib import admin
from django.urls import path
from . import views

app_name = 'sms'
urlpatterns = [
    path('', views.sms_response, name="sms"),
    path('subscribe/', views.SubscribeView.as_view(), name="subscribe"),
    path('subscription/<int:pk>/', views.SubscriberDetailsView.as_view(), name='detail'),
    #path('broadcast/<str:number>', views.broadcast_sms, name="broadcast")
    path('broadcast/', views.broadcast_sms, name="broadcast"),
]
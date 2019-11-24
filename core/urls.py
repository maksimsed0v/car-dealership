from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('act/<self_id>/', views.act_detail, name='act_detail'),
    path('attire/<self_id>/', views.attire_detail, name='attire_detail'),
]
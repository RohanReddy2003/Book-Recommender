from django.contrib import admin
from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('recommend/', views.recommend_ui, name='recommend'),
    path('recommend_books/', views.recommend_books, name='recommend_books'),
]
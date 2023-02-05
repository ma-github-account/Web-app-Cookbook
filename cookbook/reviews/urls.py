from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('dishes/', views.dish_list, name='dish_list'),
    path('dishes/<int:pk>/', views.dish_detail, name='dish_detail'),
    path('dishes/<int:dish_pk>/reviews/new/', views.review_edit, name='review_create'),
    path('dishes/<int:dish_pk>/reviews/<int:review_pk>/', views.review_edit, name='review_edit'),
    path('dishes/<int:pk>/media/', views.dish_media, name='dish_media'),
    path('dish-search/', views.dish_search, name='dish_search'),
]



from django.urls import path
from . import views

app_name = 'anime'

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.anime_create, name='anime_create'),
    path('<int:pk>/', views.anime_detail, name='anime_detail'),
    path('<int:pk>/update/', views.anime_update, name='anime_update'),
    path('image/<int:image_id>/delete/', views.delete_image, name='delete_image'),
    path('<int:pk>/delete/', views.anime_delete, name='anime_delete'),
]

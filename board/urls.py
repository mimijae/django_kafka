from django.urls import path
from . import views


urlpatterns = [
    path('create/', views.create_post, name='create_post'),
    path('update/<int:post_id>/', views.update_post, name='update_post'),
    path('delete/<int:post_id>/', views.delete_post, name='delete_post'),
]

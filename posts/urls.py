from django.urls import path

from .views import create_post, like_post, post_delete, post_detail, post_edit

urlpatterns = [
    path('<int:pk>/', post_detail, name='post_detail'),
    path('<int:pk>/edit/', post_edit, name='post_edit'),
    path('<int:pk>/delete/', post_delete, name='post_delete'),
    path('<int:pk>/like/', like_post, name='post_like'),
    path('new/', create_post, name='create_post'),
]

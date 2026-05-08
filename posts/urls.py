from django.urls import path

from . import views

urlpatterns = [
    path('<int:pk>/', views.post_detail, name='post_detail'),
    path('<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('<int:pk>/like/', views.like_post, name='post_like'),
    path('<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('new/', views.create_post, name='create_post'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('',views.post_list,name='post_list'),
    path('<int:post_id>/',views.post_detail,name='post_detail'),
    path('unpublished/',views.post_unpublished,name='post_unpublished'),
    path('new/', views.post_create, name='post_create'),
    path('<int:post_id>/edit/', views.post_edit, name='post_edit'),
    path('<int:post_id>/delete/', views.post_delete, name='post_delete'),
]

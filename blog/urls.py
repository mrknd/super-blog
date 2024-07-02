from django.urls import path

from . import views


app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('<slug:slug>', views.post_detail, name='post_detail'),
    path('<int:pk>/share/', views.post_share, name='post_share'),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_tag'),
    path('category/<int:category_id>/', views.post_list_by_category, name='post_list_by_category'),
    path('tags/<slug:tag_slug>/', views.post_list_by_tag, name='post_list_by_tag'),

]

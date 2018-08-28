from django.urls import path
from django.urls.resolvers import RoutePattern

from . import views


app_name = 'news'

urlpatterns = [
    path('', views.articles_list, name='list'),
    path('search/', views.search_list, name='search'),
    path('create/', views.article_create, name='create'),
    path('<slug:slug>/', views.article_detail, name='detail'),
    path('<slug:slug>/edit/', views.article_edit, name='edit'),
    path('<slug:slug>/delete/', views.article_delete, name='delete'),
    path('<slug:slug>/comment/create', views.comment_create, name='create_comment'),
    path('<slug:slug>/comment/<int:comment_id>/delete', views.comment_delete, name='delete_comment'),
]

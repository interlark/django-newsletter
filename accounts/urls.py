from django.urls import path
from django.urls import include
from . import views


app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('<int:profile_id>/', views.profile_detail, name='detail'),
    path('<int:profile_id>/delete/', views.delete_profile, name='delete'),
    path('<int:profile_id>/change_password/', views.profile_change_password, name='change_password'),
    path('<int:profile_id>/edit/', views.update_profile, name='edit'),
    path('<int:profile_id>/give_privileges/', views.profile_give_privileges, name='give_privileges'),
    path('<int:profile_id>/delete_privileges/', views.profile_delete_privileges, name='delete_privileges'),
]

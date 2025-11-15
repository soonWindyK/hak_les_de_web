"""
URL configuration for main app.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('nko/', views.nko_list, name='nko'),
    path('nko/<int:nko_id>/', views.nko_detail, name='nko_detail'),
    path('news/', views.news_list, name='news'),
    path('news/<int:news_id>/', views.news_detail, name='news_detail'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('knowledge/', views.knowledge_list, name='knowledge'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_redirect, name='profile'),
    path('profile/user/', views.user_profile, name='user_profile'),
    path('profile/moderator/', views.moderator_dashboard, name='moderator_dashboard'),
    path('profile/admin/', views.admin_dashboard, name='admin_dashboard'),
]

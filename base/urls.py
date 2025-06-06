from django.urls import path

from . import views

urlpatterns = [
    # login and logout
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    # user profile
    path('profile/<str:pk>/', views.user_profile, name='user-profile'),
    path('update-profile/', views.update_profile, name='update-profile'),
    # home
    path('', views.home, name='home'),
    path('topics/', views.topics_page, name='topics'),
    path('activity/', views.activity_page, name='activity'),
    # crud room
    path('room/<str:pk>/', views.room, name='room'),
    path('create-room/', views.create_room, name='create-room'),
    path('update-room/<str:pk>/', views.update_room, name='update-room'),
    path('delete-room/<str:pk>/', views.delete_room, name='delete-room'),
    # crud message
    path('delete-message/<str:pk>/', views.delete_message, name='delete-message'),
]

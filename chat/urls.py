from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register, name='register'),

    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='chat/reset_password_templates/reset_password.html'), 
        name='password_reset'
    ),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='chat/reset_password_templates/reset_password_sent.html'), 
        name='password_reset_done'),

    path('password_reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
       template_name='chat/reset_password_templates/reset_password_form.html' ), 
       name='password_reset_confirm'),

    path('password_reset/complete', auth_views.PasswordResetCompleteView.as_view(
        template_name='chat/reset_password_templates/reset_password_complete.html'), 
        name='password_reset_complete'),

    path('edit/', views.edit, name='edit'),

    path('friends/', views.friends, name='friends'),
    path('ajax/search/<str:input>/', views.search, name='search'),
    path('ajax/invite/<int:pk>/', views.invite_friend, name='invite'),
    path('ajax/decline/<int:pk>/', views.decline_invitation, name='decline'),
    path('ajax/accept/<int:pk>/', views.accept_invitation, name='accept'),
    path('ajax/delete_friend/<int:pk>/', views.delete_friend, name='delete_friend'),
    path('ajax/filter/<str:input>/', views.filter_friends, name='filter_friends'),

    path('chat_rooms/', views.chat_rooms, name='chat_rooms'),
]
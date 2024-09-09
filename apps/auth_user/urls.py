from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('update-profile/', views.UserUpdateView.as_view(), name='update-profile'),

    path('activate/', views.UserActivationView.as_view(), name='activate'),

    path('password-reset/', views.UserPasswordResetView.as_view(), name='password-reset'),
    path('password-reset-confirm/', views.UserPasswordResetConfirmView.as_view(), name='password-reset-confirm'),

    path('forgot-password/', views.UserForgotPasswordView.as_view(), name='forgot-password'),
    path('change-password/', views.UserChangePasswordView.as_view(), name='change-password'),
]

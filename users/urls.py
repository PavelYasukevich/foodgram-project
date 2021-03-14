from django.contrib.auth import views as auth_views
from django.urls import include, path

from .views import SignUp

urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
    path(
        'login/',
        auth_views.LoginView.as_view(template_name='users/authForm.html'),
        name='login',
    ),
    path(
        'password_change/',
        auth_views.PasswordChangeView.as_view(
            template_name='users/changePassword.html'
        ),
        name='password_change',
    ),
    path(
        'password_reset/',
        auth_views.PasswordResetView.as_view(
            template_name='users/resetPassword.html'
        ),
        name='password_reset',
    ),
    path(
        'password_reset_confirm/',
        auth_views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm',
    ),
    path(
        'password_reset_complete/',
        auth_views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete',
    ),
    path('', include('django.contrib.auth.urls')),
]

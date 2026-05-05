from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from . import forms, views

# app_name = 'accounts'

urlpatterns = [
    path(
        'login/',
        LoginView.as_view(
            template_name='accounts/login.html',
            redirect_authenticated_user=True,
            authentication_form=forms.CustomAuthenticationForm,
        ),
        name='login',
    ),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    # HTMX urls
    path('check_username/', views.check_username, name='check_username'),
    path('check_email/', views.check_email, name='check_email'),
    path('check_password1/', views.check_password1, name='check_password1'),
    path('check_password2/', views.check_password2, name='check_password2'),
]

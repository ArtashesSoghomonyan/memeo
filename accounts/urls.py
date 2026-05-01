from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .views import profile, signup

urlpatterns = [
    path('login/', LoginView.as_view(template_name='accounts/login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('signup/', signup, name='signup'),
    path('profile/', profile, name='profile'),
]

from django.urls import path
from .views import RegisterUserView, logaut_user, LoginUserView, EmailChangeView, ChangePasswordView, ProfileDeleteView, \
    ProfileUpdateView

urlpatterns = (
    path('', ProfileUpdateView.as_view(), name='profile'),
    path('register', RegisterUserView.as_view(), name='register_user'),
    path('login', LoginUserView.as_view(), name='login_user'),
    path('logout', logaut_user, name='logout_user'),
    path('email_change', EmailChangeView.as_view(), name='email_change'),
    path('change_password', ChangePasswordView.as_view(), name='change_password'),
    path('delete', ProfileDeleteView.as_view(), name='delete_profile'),
)

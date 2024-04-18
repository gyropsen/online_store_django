from django.urls import path
from users.apps import UsersConfig
from users.views import Login, Logout, UserRegisterView, UserUpdateView, RestorePassword

app_name = UsersConfig.name

urlpatterns = [
    path('', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('profile/', UserUpdateView.as_view(), name='profile'),
    path('restore_password/', RestorePassword.as_view(), name='restore_password'),
]
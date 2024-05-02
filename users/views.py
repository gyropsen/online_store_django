import random
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, UpdateView, FormView
from django.urls import reverse_lazy

from config import settings
from users.forms import UserAuthenticationForm, UserRegistrationForm, UserUserChangeForm, RestorePasswordForm
from users.models import User
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password


class Login(LoginView):
    template_name = 'users/login.html'
    form_class = UserAuthenticationForm
    success_url = reverse_lazy('catalog:index')


class Logout(LogoutView):
    pass


class UserRegisterView(CreateView):
    model = User
    form_class = UserRegistrationForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/register.html'

    def form_valid(self, form):
        new_user = form.save()
        send_mail(
            subject='Поздравляем с регистрацией',
            message='Вы зарегистрировались на нашей платформе. Добро пожаловать!',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[new_user.email],
        )
        new_user.save()
        return super().form_valid(form)


class UserUpdateView(UpdateView):
    model = User
    success_url = reverse_lazy('users:profile')
    form_class = UserUserChangeForm

    def get_object(self, queryset=None):
        return self.request.user


# def restore_password(request):
#     print(request)
#     if request.method == 'POST':
#         user = get_object_or_404(User, email=request.email)
#         user.password = make_password(''.join(str(random.randint(0, 9)) for _ in range(12)))
#         send_mail(
#             subject='Вы сменили пароль',
#             message=f'Ваш новый пароль {user.password}',
#             from_email=settings.EMAIL_HOST_USER,
#             recipient_list=[request.user.email],
#         )
#     # request.user.set_password(new_password)
#     # request.user.save()
#
#     # return render(request, )
#     return render(request, 'users/restore_password.html', {'form': RestorePasswordForm})

class RestorePassword(FormView):
    form_class = RestorePasswordForm
    template_name = 'users/restore_password.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        if form.is_valid():
            email = form.cleaned_data.get('email')
            user = get_object_or_404(User, email=email)
            new_password = ''.join(str(random.randint(0, 9)) for _ in range(12))
            user.password = make_password(new_password)
            send_mail(
                subject='Вы сменили пароль',
                message=f'Ваш новый пароль {new_password}',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
            )
            user.save()

        return super().form_valid(form)

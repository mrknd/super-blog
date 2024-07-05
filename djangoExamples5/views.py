from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import auth, messages

from .forms import UserRegisterForm

import re


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        password_regex = r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$'

        if not re.match(email_regex, email):
            messages.error(request, 'Невірний формат електронної пошти')
            return redirect('register')

        if not re.match(password_regex, password):
            messages.error(request, 'Пароль повинен містити мінімум 8 символів, одну літеру та одну цифру')
            return redirect('register')

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username вже зайнятий')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Email вже зайнятий')
                    return redirect('register')
                else:
                    user = User.objects.create_user(username=username,
                                                    email=email,
                                                    password=password)
                    # auth.login(request, user)
                    # messages.success(request, 'You are now logged in')
                    # return redirect('dashboard')
                    user.save()
                    messages.success(request, 'Обліковий запис створено')
                    return redirect('login')
        else:
            messages.error(request, 'Паролі не співпадають')
            return redirect('register')

    else:
        return render(request=request, template_name='blog/post/register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, f'Вітаємо в банді {username}')
            return redirect('home')
        else:
            messages.error(request, 'Неправильний логін або пароль')
            return redirect(request.META.get('HTTP_REFERER', 'home'))

    return render(request=request, template_name='blog/post/login.html')


def logout(request):
    auth.logout(request)
    messages.success(request, f'Скоро побачимось')
    return redirect('home')

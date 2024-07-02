from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import auth, messages

from .forms import RegistrationForm


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already taken')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Email already taken')
                    return redirect('register')
                else:
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        password=password)
                    # auth.login(request, user)
                    # messages.success(request, 'You are now logged in')
                    # return redirect('dashboard')
                    user.save()
                    messages.success(request, 'Account created')
                    return redirect('login')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('register')

    else:
        return render(request=request, template_name='blog/post/home.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        messages.success(request, f'Вітаємо в банді {username}')

        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Неправильний логін або пароль')
            return redirect(request.META.get('HTTP_REFERER', 'home'))

    return render(request=request, template_name='blog/post/login.html')


def logout(request):
    auth.logout(request)
    messages.success(request, f'Скоро побачимось')
    return redirect('home')

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.models import Group


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.is_staff = True
            new_user.save()
            new_user.groups.add(Group.objects.get(name='client'))
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт создан для {username}!')
            return redirect('main')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})


def main(request):
    return render(request, 'core/main.html')

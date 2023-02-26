from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from .forms import RegistrationForm, LoginForm
from django.contrib.auth.decorators import login_required
from .forms import UserProfileEditForm, UserEditForm, AddPredictionForm
from .models import UserProfile


def homepage_view(request):
    return render(request, 'home.html')


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            user_profile = UserProfile.objects.create(user=user, date_of_birth=None, 
                                                 avatar='images/userdata/unnamed.jpg', about='...', count=0)
            return redirect('/')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def profile_view(request):
    user_profile = request.user.userprofile
    return render(request, 'userprofile/profile.html', {'user_profile': user_profile})


@login_required
def edit_profile_view(request):
    user_profile = request.user.userprofile
    if request.method == 'POST':
        form = UserProfileEditForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileEditForm(instance=user_profile)
    return render(request, 'userprofile/edit_profile.html', {'form': form})


@login_required
def profile_settings_view(request):
    user = request.user
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserEditForm(instance=user)
    return render(request, 'userprofile/settings_profile.html', {'form': form})


@login_required
def predict_view(request):
    # прототип функции, ML добавлю позже
    user = request.user
    prediction = 'Revenue Value'
    if request.method == 'POST':
        form = AddPredictionForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city']
            city_group = form.cleaned_data['city_group']
            type = form.cleaned_data['type']
            date = form.cleaned_data['date']
            P1 = form.cleaned_data['P1']
            P2 = form.cleaned_data['P2']
            prediction = 'Revenue Value'
    else:
        form=AddPredictionForm()
    return render(request, 'predict_revenue.html', {'form': form, 'prediction': prediction})







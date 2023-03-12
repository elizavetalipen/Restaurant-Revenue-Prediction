from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth import update_session_auth_hash
from .forms import RegistrationForm, LoginForm
from django.contrib.auth.decorators import login_required
from .forms import UserProfileEditForm, UserEditForm, AddPredictionForm
from .models import UserProfile, Prediction
from django.http import HttpResponse
from .utils import *
from django.template.loader import render_to_string
import io
import json
from PyPDF2 import PdfFileWriter, PdfFileReader
import logging
from .exceptions import NotFoundError, ValidationError
from datetime import datetime


logger = logging.getLogger(__name__)

def handle_exceptions(view_func):
    def wrapper(request, *args, **kwargs):
        try:
            return view_func(request, *args, **kwargs)
        except (NotFoundError, ValidationError) as e:
            logger.exception(f"{type(e).__name__}: {str(e)} at {datetime.now()}")
            return render(request, 'error_page.html', {'status_code': e.status_code, 'error_message': e.error_message})
        except Exception as e:
            logger.exception(f"{type(e).__name__}: {str(e)} at {datetime.now()}")
            return render(request, 'error_page.html', {'status_code': 500, 'error_message': 'Internal Server Error'})
    return wrapper


@handle_exceptions
def homepage_view(request):
    return render(request, 'home.html')


@handle_exceptions
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
            logger.info(f'New user {username} registered at {datetime.now()}')
            return redirect('/')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


@handle_exceptions
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                logger.info(f'User {username} logged in at {datetime.now()}')
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


@handle_exceptions
def logout_view(request):
    logout(request)
    return redirect('home')


@handle_exceptions
@login_required
def profile_view(request):
    user_profile = request.user.userprofile
    return render(request, 'userprofile/profile.html', {'user_profile': user_profile})


@handle_exceptions
@login_required
def edit_profile_view(request):
    
    user_profile = request.user.userprofile
    if request.method == 'POST':
        form = UserProfileEditForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            logger.info(f'User {request.user.username} edited profile at {datetime.now()}')
            return redirect('profile')
    else:
        form = UserProfileEditForm(instance=user_profile)
    return render(request, 'userprofile/edit_profile.html', {'form': form})


@handle_exceptions
@login_required
def profile_settings_view(request):
    user = request.user
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            new_password = form.cleaned_data['password']
            if new_password:
                user.set_password(new_password)
            user.save()
            logger.info(f'User {user.username} changed profile settings at {datetime.now()}')
            update_session_auth_hash(request, user)
            return redirect('profile')
    else:
        form = UserEditForm(instance=user)
    return render(request, 'userprofile/settings_profile.html', {'form': form})


@handle_exceptions
@login_required
def predict_view(request):
    user = request.user
    prediction = 'Revenue Value'
    if request.method == 'POST':
        form = AddPredictionForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city']
            city_group = form.cleaned_data['city_group']
            type = form.cleaned_data['type']
            date = form.cleaned_data['date']
            P2 = form.cleaned_data['P2']
            P6 = form.cleaned_data['P6']
            P23 = form.cleaned_data['P23']
            P28 = form.cleaned_data['P28']

            preds_dict = {"City": city, 'City Group': city_group,
                'Type': type,'Open Date': date.strftime('%Y-%m-%d'),
                'P2': P2, 'P6': P6, 'P23': P23,'P28': P28}
            
            prediction = make_prediction(preds_dict)

            logger.info(f'User {user.username} made new prediction at {datetime.now()}')
            preds_dict["Prediction"]=prediction

            new_prediction = Prediction.objects.create(user=request.user,predicted_revenue=prediction)
            user_profile = UserProfile.objects.get(user=request.user)
            user_profile.count += 1
            user_profile.save()
        
            if 'save_pdf' in request.POST:
                pdf_content = dict_to_pdf(preds_dict)
                response = HttpResponse(pdf_content, content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="prediction.pdf"'
                logger.info(f'User {user.username} saved prediction as pdf file at {datetime.now()}')
                return response

            if 'save_json' in request.POST:
                json_content = json.dumps(preds_dict, indent=4)
                response = HttpResponse(json_content, content_type='application/json')
                response['Content-Disposition'] = 'attachment; filename="prediction.json"'
                logger.info(f'User {user.username} saved prediction as json file at {datetime.now()}')
                return response

    else:
        form=AddPredictionForm()
    return render(request, 'predict_revenue.html', {'form': form, 'prediction': prediction})






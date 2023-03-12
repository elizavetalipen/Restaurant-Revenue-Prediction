from django.urls import path
from .views import *

urlpatterns = [
    path('', homepage_view, name='home'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', edit_profile_view, name='edit_profile'),
    path('profile/settings/', profile_settings_view, name='profile_settings'),
    path('predict/',predict_view, name='predict'),
    path('error_page/', handle_exceptions, name="handle_exceptions"),
]

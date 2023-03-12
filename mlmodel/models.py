from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# модель для данных, отображаемых на странице пользователя
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    avatar = models.ImageField(upload_to='images/userdata', blank=True)
    about = models.CharField(max_length=500)
    # количество проведенных вычислений
    count = models.IntegerField()


class Prediction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    predicted_revenue = models.DecimalField(max_digits=10, decimal_places=2)
    prediction_date = models.DateTimeField(default=datetime.now())

    







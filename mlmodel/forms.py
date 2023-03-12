from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.forms import PasswordChangeForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Field, Row, Column
from django.contrib.auth.models import User
from .models import UserProfile, Prediction


# форма для редактирования информации в профиле
class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['date_of_birth', 'avatar', 'about']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save'))
        self.helper.layout = Layout(
            Field('date_of_birth', css_class='form-control'),
            Field('avatar', css_class='form-control-file'),
            Field('about', css_class='form-control'),
        )


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']
    
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.fields['password'].widget = forms.PasswordInput()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save'))
        self.helper.layout = Layout(
            Div(
            Field('email', css_class='form-control col-md-6'),
            Field('password', css_class='form-control col-md-6'),
            css_class='form-group'
            )
        )


class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Register'))

        self.helper.layout = Layout(
            Div(
                Field('username', css_class='form-control col-md-6'),
                Field('email', css_class='form-control col-md-6'),
                css_class='form-group'
            ),
            Div(
                Field('password1', css_class='form-control col-md-6'),
                Field('password2', css_class='form-control col-md-6'),
                css_class='form-group'
            )
        )


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Login'))

        self.helper.layout = Layout(
            Div(
                Field('username', css_class='form-control col-md-6'),
                css_class='form-group'
            ),
            Div(
                Field('password', css_class='form-control col-md-6'),
                css_class='form-group'
            )
        )

# форма для ввода данных для предсказания
class AddPredictionForm(forms.Form):

    CITY_GROUPS = [('Big Cities', 'Big Cities'),('Other', 'Other'),]
    TYPES = [('FC', 'FC'),('DT', 'DT'),('IL','IL')]

    city = forms.CharField(max_length=30)
    city_group = forms.ChoiceField(choices=CITY_GROUPS)
    type = forms.ChoiceField(choices=TYPES)
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    P2 = forms.FloatField()
    P6 = forms.FloatField()
    P23 = forms.FloatField()
    P28 = forms.FloatField()

    def __init__(self, *args, **kwargs):
        super(AddPredictionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))
        self.helper.layout = Layout(
            Row(
                Column('city', css_class='form-group col-md-6 mb-0'),
                Column('city_group', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('type', css_class='form-group col-md-6 mb-0'),
                Column('date', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('P2', css_class='form-group col-md-6 mb-0'),
                Column('P6', css_class='form-group col-md-6 mb-0'),
                Column('23', css_class='form-group col-md-6 mb-0'),
                Column('P28', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
        )


from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.validators import RegexValidator

from .models import Profile

username_validator = RegexValidator(
    regex=r'^[a-z_]+$',
    message='Username must be lowercase or underscore only.'
)

email_validator = RegexValidator(
    regex=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
    message='Email must be a valid email address.'
)

first_name_validator = RegexValidator(
    regex=r'^[a-zA-Z]+$',
    message='First name must be alphabetic only.'
)

last_name_validator = RegexValidator(
    regex=r'^[a-zA-Z]+$',
    message='Last name must be alphabetic only.'
)

class SignupForm(UserCreationForm):
    username = forms.CharField(
        label='',
        max_length=50,
        validators=[username_validator],
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full border rounded py-2 px-3 text-gray-700 mb-3',
            'placeholder': 'Username',
        }))
    email = forms.EmailField(
        label='',
        max_length=254,
        validators=[email_validator],
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full border rounded py-2 px-3 text-gray-700 mb-3',
            'placeholder': 'Email',
        })
    )
    first_name = forms.CharField(
        label='',
        max_length=30,
        validators=[first_name_validator],
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full border rounded py-2 px-3 text-gray-700 mb-3',
            'placeholder': 'First name',
        })
    )
    last_name = forms.CharField(
        label='',
        max_length=30,
        validators=[last_name_validator],
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full border rounded py-2 px-3 text-gray-700 mb-3',
            'placeholder': 'Last name',
        })
    )
    password1 = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={
            'class': 'w-full border rounded py-2 px-3 text-gray-700 mb-3',
            'placeholder': 'Password',
        })
    )
    password2 = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={
            'class': 'w-full border rounded py-2 px-3 text-gray-700 mb-3',
            'placeholder': 'Confirm password',
        })
    )

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email').lower() # type: ignore
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email


class ProfileForm(forms.ModelForm):
    bio = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)

    class Meta:
        model = Profile
        fields = ['profile_picture', 'bio', 'birth_date']


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'class': 'w-full border rounded py-2 px-3 text-gray-700 mb-3',
            'placeholder': 'Username',
        })
    )
    password = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={
            'class': 'w-full border rounded py-2 px-3 text-gray-700 mb-3',
            'placeholder': 'Password',
        })
    )

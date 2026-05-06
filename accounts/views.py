from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import ProfileForm, SignupForm, email_validator, username_validator
from .models import Profile


def signup(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = Profile.objects.create(user=form.instance)
            profile.save()
            login(request, user)
            messages.success(
                request, 'Congratulations! You have successfully registered.'
            )
            return redirect('home')
    else:
        form = SignupForm()

    context = {
        'title': 'Register',
        'form': form,
    }

    return render(request, 'accounts/signup.html', context)


@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Congratulations! Your profile has been updated.')
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user.profile)

    context = {
        'title': 'Profile',
        'form': form,
    }

    return render(request, 'accounts/profile.html', context)


# Validation views


def check_username(request):
    username = request.POST.get('username')

    try:
        if username != '':
            username_validator(username)
    except ValidationError:
        return HttpResponse(
            "<p class='field-error'>❌This username is not valid. Usernames should only contain lowercase letters and underscores.</p>"
        )

    if username == '':
        return HttpResponse("")

    if get_user_model().objects.filter(username=username).exists():
        return HttpResponse(
            "<p class='field-error'>❌This username is already taken.</p>"
        )
    return HttpResponse("<p class='field-success'>☑️ This username is available.</p>")


def check_email(request):
    email = request.POST.get('email')

    try:
        if email != '':
            email_validator(email)
    except ValidationError:
        return HttpResponse("<p class='field-error'>❌This email is not valid.</p>")

    if email == '':
        return HttpResponse("")

    if get_user_model().objects.filter(email=email).exists():
        return HttpResponse(
            "<p class='field-error'>❌This email is already in use.</p>"
        )
    return HttpResponse("<p class='field-success'>☑️ This email is available.</p>")


def check_password1(request):
    password1 = request.POST.get('password1')

    try:
        if password1 != '':
            validate_password(password1)
    except ValidationError as e:
        return HttpResponse(f"<p class='field-error'>❌{ e.messages[0] }</p>")

    if password1 == '':
        return HttpResponse("")

    return HttpResponse("<p class='field-success'>☑️ This password is valid.</p>")


def check_password2(request):
    password1 = request.POST.get('password1')
    password2 = request.POST.get('password2')

    if password2 != '' and password2 != password1:
        return HttpResponse("<p class='field-error'>❌Passwords do not match.</p>")

    return HttpResponse("<p class='field-success'>☑️ Passwords match.</p>")

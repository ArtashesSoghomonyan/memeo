from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import ProfileForm, SignupForm
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
            messages.success(request, 'Congratulations! You have successfully registered.')
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

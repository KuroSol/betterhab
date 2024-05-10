from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, ProfileForm

def register(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(request, 'Your account has been created!')
            return redirect('login')
    else:
        user_form = UserRegisterForm()
        profile_form = ProfileForm()
    return render(request, 'profiles/register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

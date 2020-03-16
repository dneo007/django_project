from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, FacialRecForm
from .models import Profile


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        f_form = FacialRecForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            f_form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(username=username, password=raw_password)
            login(request, account)
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('profile')
    else:
        form = UserRegisterForm()
        f_form = FacialRecForm()
    return render(request, 'users/register.html', {'form': form, 'f_form': f_form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        f_form = FacialRecForm(request.POST, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            f_form.save()
            messages.success(request, f'Your account has been updated!')

            if Profile.objects.get(user=request.user).fc:
                return redirect('blog-about')

            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        f_form = FacialRecForm(instance=request.user.profile)
        checked = Profile.objects.get(user=request.user).fc

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'f_form': f_form,
        'checked': checked,
    }

    return render(request, 'users/profile.html', context)

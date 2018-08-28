from django.contrib.auth import login as login_dj, logout as logout_dj, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.urls import reverse_lazy
from accounts.utils import DEFAULT_AVATAR_PATH
from .models import Profile
from .forms import ProfileCreateForm, ProfileUpdateForm


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login_dj(request, form.get_user())
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('news:list')
    else:
        form = AuthenticationForm()
    context = {'user_form': form}
    return render(request, 'accounts/login.html', context)


def logout(request):
    if request.method == 'POST':
            logout_dj(request)
    return redirect('news:list')


@transaction.atomic
def signup(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        profile_form = ProfileCreateForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.user = user_form.save()
            profile.save()
            login_dj(request, profile.user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('news:list') #account:profile_detail
    else:
        user_form = UserCreationForm()
        profile_form = ProfileCreateForm()
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'accounts/signup.html', context)


def profile_detail(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)
    context = {'profile': profile, 'default_avatar_path': DEFAULT_AVATAR_PATH}
    return render(request, 'accounts/detail.html', context)


@login_required(login_url=reverse_lazy('accounts:login'))
def update_profile(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)
    if request.user.is_superuser or profile.user == request.user:
        if request.method == 'POST':
            form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
            if form.is_valid():
                form.save()
                return redirect('accounts:detail', profile_id)
        else:
            form = ProfileUpdateForm(instance=request.user.profile)
        context = {'form': form, 'profile': profile}
        return render(request, 'accounts/edit.html', context)
    else:
        raise PermissionDenied


@login_required(login_url=reverse_lazy('accounts:login'))
def delete_profile(request, profile_id):
    if request.method == 'POST':
        profile = get_object_or_404(Profile, id=profile_id)
        if request.user.is_superuser or profile.user == request.user:
            profile.user.delete()
        else:
            raise PermissionDenied
    return redirect('accounts:detail', profile_id)


@login_required(login_url=reverse_lazy('accounts:login'))
def profile_change_password(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)
    if request.user.is_superuser or profile.user == request.user:
        if request.method == 'POST':
            if profile.user:
                form = PasswordChangeForm(data=request.POST, user=profile.user)
                if form.is_valid():
                    user = form.save()
                    update_session_auth_hash(request, user)
                    return redirect('accounts:detail', profile_id)
            else:
                raise Http404
        else:
            form = PasswordChangeForm(user=profile.user)
    else:
        raise PermissionDenied
    context = {'form': form, 'profile': profile }
    return render(request, 'accounts/change_password.html', context)


@login_required(login_url=reverse_lazy('accounts:login'))
def profile_give_privileges(request, profile_id):
    if request.method == 'POST':
        profile = get_object_or_404(Profile, id=profile_id)
        if request.user.is_superuser:
            if profile.user:
                profile.user.is_superuser = True
                profile.user.save()
            else:
                raise Http404
        else:
            raise PermissionDenied
    return redirect('accounts:detail', profile_id)


@login_required(login_url=reverse_lazy('accounts:login'))
def profile_delete_privileges(request, profile_id):
    if request.method == 'POST':
        profile = get_object_or_404(Profile, id=profile_id)
        if request.user.is_superuser:
            if profile.user:
                profile.user.is_superuser = False
                profile.user.save()
            else:
                raise Http404
        else:
            raise PermissionDenied
    return redirect('accounts:detail', profile_id)

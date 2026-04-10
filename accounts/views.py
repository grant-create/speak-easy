from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from languages.models import Language

from .forms import RegisterForm
from .models import UserLanguage


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('add_language')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('profile')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def profile(request):
    user_languages = request.user.user_languages.select_related('language').order_by('started_at')
    return render(request, 'accounts/profile.html', {'user_languages': user_languages})


@login_required
def add_language(request):
    enrolled_ids = request.user.user_languages.values_list('language_id', flat=True)
    available = Language.objects.exclude(id__in=enrolled_ids)

    if request.method == 'POST':
        lang_id = request.POST.get('language')
        language = get_object_or_404(Language, id=lang_id)
        # deactivate others, make this one active
        request.user.user_languages.update(is_active=False)
        UserLanguage.objects.create(user=request.user, language=language, is_active=True)
        messages.success(request, f'Started learning {language.name}!')
        return redirect('profile')

    return render(request, 'accounts/add_language.html', {'available': available})


@login_required
def switch_language(request, language_id):
    language = get_object_or_404(Language, id=language_id)
    request.user.user_languages.update(is_active=False)
    request.user.user_languages.filter(language=language).update(is_active=True)
    return redirect('lesson_list')

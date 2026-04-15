import logging

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import get_object_or_404, redirect, render

from languages.models import Language

from .forms import RegisterForm
from .models import RateLimit, UserLanguage

logger = logging.getLogger(__name__)

_LOGIN_MAX = 5      # attempts
_LOGIN_WINDOW = 15  # minutes
_REGISTER_MAX = 10
_REGISTER_WINDOW = 60


def login_view(request):
    if request.method == 'POST':
        ip = _get_ip(request)
        RateLimit.clear_old(_LOGIN_WINDOW)

        if RateLimit.is_limited(ip, 'login', _LOGIN_MAX, _LOGIN_WINDOW):
            logger.warning('Login rate limit hit from %s', ip)
            return render(request, 'accounts/login.html', {
                'form': AuthenticationForm(),
                'rate_limited': True,
            })

        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            logger.info('Successful login: %s', form.get_user().username)
            login(request, form.get_user())
            return redirect('profile')
        else:
            RateLimit.record(ip, 'login')
            logger.warning('Failed login attempt from %s', ip)
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        ip = _get_ip(request)
        RateLimit.clear_old(_REGISTER_WINDOW)

        if RateLimit.is_limited(ip, 'register', _REGISTER_MAX, _REGISTER_WINDOW):
            logger.warning('Register rate limit hit from %s', ip)
            return render(request, 'accounts/register.html', {
                'form': RegisterForm(),
                'rate_limited': True,
            })

        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            logger.info('New user registered: %s', user.username)
            login(request, user)
            return redirect('add_language')
        else:
            RateLimit.record(ip, 'register')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


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
        # Validate lang_id is a positive integer before hitting the DB
        raw_id = request.POST.get('language', '')
        try:
            lang_id = int(raw_id)
            if lang_id <= 0:
                raise ValueError
        except (ValueError, TypeError):
            return render(request, 'accounts/add_language.html', {
                'available': available,
                'error': 'Invalid language selection.',
            })

        language = get_object_or_404(Language, id=lang_id)
        request.user.user_languages.update(is_active=False)
        UserLanguage.objects.create(user=request.user, language=language, is_active=True)
        messages.success(request, f'Started learning {language.name}!')
        return redirect('profile')

    return render(request, 'accounts/add_language.html', {'available': available})


@login_required
def switch_language(request, language_id):
    # Ensure the user is actually enrolled in the requested language
    user_language = get_object_or_404(UserLanguage, user=request.user, language_id=language_id)
    request.user.user_languages.update(is_active=False)
    user_language.is_active = True
    user_language.save(update_fields=['is_active'])
    return redirect('lesson_list')


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _get_ip(request):
    x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded:
        return x_forwarded.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '0.0.0.0')

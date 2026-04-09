from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import Lesson


@login_required
def lesson_list(request):
    active_language = request.user.active_language
    if not active_language:
        return redirect('add_language')
    lessons = Lesson.objects.filter(language=active_language)
    return render(request, 'lessons/lesson_list.html', {
        'lessons': lessons,
        'language': active_language,
    })


@login_required
def lesson_detail(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    phrases = lesson.phrases.all()
    return render(request, 'lessons/lesson_detail.html', {
        'lesson': lesson,
        'phrases': phrases,
    })

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST

from lessons.models import Lesson

from .models import UserLessonProgress


@require_POST
@login_required
def mark_complete(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    progress, _ = UserLessonProgress.objects.get_or_create(user=request.user, lesson=lesson)
    progress.mark_complete()
    return redirect('lesson_list')

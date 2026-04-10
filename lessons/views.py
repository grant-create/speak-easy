import random

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from progress.models import UserLessonProgress

from .models import Lesson, Phrase


@login_required
def lesson_list(request):
    active_language = request.user.active_language
    if not active_language:
        return redirect('add_language')

    lessons = Lesson.objects.filter(language=active_language)
    completed_ids = set(
        UserLessonProgress.objects.filter(
            user=request.user, lesson__in=lessons, completed=True
        ).values_list('lesson_id', flat=True)
    )

    return render(request, 'lessons/lesson_list.html', {
        'lessons': lessons,
        'language': active_language,
        'completed_ids': completed_ids,
        'completed_count': len(completed_ids),
        'total_count': lessons.count(),
    })


@login_required
def lesson_detail(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    phrases = lesson.phrases.all()
    progress, _ = UserLessonProgress.objects.get_or_create(user=request.user, lesson=lesson)

    return render(request, 'lessons/lesson_detail.html', {
        'lesson': lesson,
        'phrases': phrases,
        'is_completed': progress.completed,
    })


@login_required
def lesson_quiz(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    phrases = list(lesson.phrases.all())

    if len(phrases) < 2:
        return redirect('lesson_detail', lesson_id=lesson_id)

    session_key = f'quiz_{lesson_id}'

    # Initialize or restart quiz
    if session_key not in request.session or 'restart' in request.GET:
        question_ids = [p.id for p in phrases]
        random.shuffle(question_ids)
        request.session[session_key] = {
            'questions': question_ids,
            'answers': {},
            'last_result': None,
        }

    quiz_data = request.session[session_key]
    question_ids = quiz_data['questions']
    current_index = int(request.GET.get('q', 0))

    if current_index >= len(question_ids):
        return redirect('quiz_complete', lesson_id=lesson_id)

    # POST — submit answer
    if request.method == 'POST':
        chosen = request.POST.get('chosen', '')
        correct = request.POST.get('correct', '')
        phrase_id = int(request.POST.get('phrase_id'))
        is_correct = chosen == correct

        quiz_data['answers'][str(phrase_id)] = is_correct
        quiz_data['last_result'] = {
            'is_correct': is_correct,
            'chosen': chosen,
            'correct_answer': correct,
        }
        request.session[session_key] = quiz_data
        request.session.modified = True

        url = reverse('lesson_quiz', args=[lesson_id]) + f'?q={current_index}&answered=1'
        return redirect(url)

    # GET — show question or result
    show_result = 'answered' in request.GET
    last_result = quiz_data.get('last_result') if show_result else None
    current_phrase = get_object_or_404(Phrase, id=question_ids[current_index])

    # Pull 3 random wrong answers from the same language
    distractors = list(
        Phrase.objects.filter(lesson__language=lesson.language)
        .exclude(id=current_phrase.id)
        .values_list('translation', flat=True)
    )
    wrong = random.sample(distractors, min(3, len(distractors)))
    choices = wrong + [current_phrase.translation]
    random.shuffle(choices)

    next_index = current_index + 1
    is_last = next_index >= len(question_ids)

    return render(request, 'lessons/quiz.html', {
        'lesson': lesson,
        'phrase': current_phrase,
        'choices': choices,
        'current': current_index + 1,
        'total': len(question_ids),
        'current_index': current_index,
        'next_index': next_index,
        'is_last': is_last,
        'show_result': show_result,
        'last_result': last_result,
    })


@login_required
def quiz_complete(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    session_key = f'quiz_{lesson_id}'
    quiz_data = request.session.get(session_key, {})
    answers = quiz_data.get('answers', {})

    correct = sum(1 for v in answers.values() if v)
    total = len(answers)
    score_percent = int(correct / total * 100) if total else 0

    progress, _ = UserLessonProgress.objects.get_or_create(user=request.user, lesson=lesson)
    if not progress.completed:
        progress.mark_complete()

    if session_key in request.session:
        del request.session[session_key]

    return render(request, 'lessons/quiz_complete.html', {
        'lesson': lesson,
        'correct': correct,
        'total': total,
        'score_percent': score_percent,
    })

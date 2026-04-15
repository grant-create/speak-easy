import logging
import random

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

logger = logging.getLogger(__name__)

# Maximum character length we'll accept for a quiz answer choice
_MAX_ANSWER_LEN = 500

from progress.models import UserLessonProgress

from .models import FavoritePhrase, Lesson, Phrase


# ---------------------------------------------------------------------------
# Quiz helpers
# ---------------------------------------------------------------------------

def _build_questions(phrases):
    """Assign a random question type to each phrase and return a shuffled list."""
    questions = []
    for phrase in phrases:
        types = ['translate', 'reverse']
        if phrase.word_breakdown and len(phrase.word_breakdown) > 1:
            types.append('fill_blank')
        q_type = random.choice(types)
        q = {'id': phrase.id, 'type': q_type}
        if q_type == 'fill_blank':
            item = random.choice(phrase.word_breakdown)
            # Fall back if the blank word IS the entire original (e.g. single-word entries)
            if item['word'].strip() == phrase.original.strip():
                q['type'] = 'translate'
            else:
                q['blank_word'] = item['word']
                q['blank_meaning'] = item['meaning']
        questions.append(q)
    random.shuffle(questions)
    return questions


def _get_distractors(q_type, language, exclude_phrase_id, correct, blank_word=None):
    """Return up to 3 wrong answer strings for the given question type."""
    qs = Phrase.objects.filter(lesson__language=language).exclude(id=exclude_phrase_id)

    if q_type == 'translate':
        pool = list(qs.values_list('translation', flat=True))
    elif q_type == 'reverse':
        pool = list(qs.values_list('original', flat=True))
    else:  # fill_blank
        all_breakdowns = qs.values_list('word_breakdown', flat=True)
        pool = list({
            item['word']
            for breakdown in all_breakdowns
            if breakdown
            for item in breakdown
            if item['word'].lower() != (blank_word or '').lower()
        })

    pool = [p for p in pool if p != correct]
    return random.sample(pool, min(3, len(pool)))


# ---------------------------------------------------------------------------
# Lesson views
# ---------------------------------------------------------------------------

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
        'streak': request.user.streak,
    })


@login_required
def lesson_detail(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    phrases = list(lesson.phrases.all())
    progress, _ = UserLessonProgress.objects.get_or_create(user=request.user, lesson=lesson)

    favorited_ids = set(
        FavoritePhrase.objects.filter(
            user=request.user, phrase__in=phrases
        ).values_list('phrase_id', flat=True)
    )

    return render(request, 'lessons/lesson_detail.html', {
        'lesson': lesson,
        'phrases': phrases,
        'is_completed': progress.completed,
        'favorited_ids': favorited_ids,
    })


# ---------------------------------------------------------------------------
# Quiz views
# ---------------------------------------------------------------------------

@login_required
def lesson_quiz(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    phrases = list(lesson.phrases.all())

    if len(phrases) < 2:
        return redirect('lesson_detail', lesson_id=lesson_id)

    session_key = f'quiz_{lesson_id}'

    if session_key not in request.session or 'restart' in request.GET:
        request.session[session_key] = {
            'questions': _build_questions(phrases),
            'answers': {},
            'last_result': None,
        }

    quiz_data = request.session[session_key]
    questions = quiz_data['questions']
    current_index = int(request.GET.get('q', 0))

    if current_index >= len(questions):
        return redirect('quiz_complete', lesson_id=lesson_id)

    current_q = questions[current_index]
    phrase_id = current_q['id']
    q_type = current_q['type']
    current_phrase = get_object_or_404(Phrase, id=phrase_id)

    # POST — submit answer
    if request.method == 'POST':
        chosen = request.POST.get('chosen', '')[:_MAX_ANSWER_LEN]

        # Derive the correct answer server-side — never trust the client
        blank_word = current_q.get('blank_word')
        if q_type == 'translate':
            correct = current_phrase.translation
        elif q_type == 'reverse':
            correct = current_phrase.original
        else:  # fill_blank
            correct = blank_word or ''

        is_correct = chosen.strip() == correct.strip()

        quiz_data['answers'][str(phrase_id)] = is_correct
        quiz_data['last_result'] = {
            'is_correct': is_correct,
            'correct_answer': correct,
            'question_type': q_type,
        }
        request.session[session_key] = quiz_data
        request.session.modified = True

        url = reverse('lesson_quiz', args=[lesson_id]) + f'?q={current_index}&answered=1'
        return redirect(url)

    # GET — build question context
    show_result = 'answered' in request.GET
    last_result = quiz_data.get('last_result') if show_result else None

    blank_word = current_q.get('blank_word')
    if q_type == 'translate':
        question_text = current_phrase.original
        correct_answer = current_phrase.translation
        show_pronunciation = True
    elif q_type == 'reverse':
        question_text = current_phrase.translation
        correct_answer = current_phrase.original
        show_pronunciation = False
    else:  # fill_blank
        question_text = current_phrase.original.replace(blank_word, '___', 1)
        correct_answer = blank_word
        show_pronunciation = True

    distractors = _get_distractors(q_type, lesson.language, phrase_id, correct_answer, blank_word)
    choices = distractors + [correct_answer]
    random.shuffle(choices)

    next_index = current_index + 1

    return render(request, 'lessons/quiz.html', {
        'lesson': lesson,
        'phrase': current_phrase,
        'question_text': question_text,
        'question_type': q_type,
        'show_pronunciation': show_pronunciation,
        'correct_answer': correct_answer,
        'choices': choices,
        'current': current_index + 1,
        'total': len(questions),
        'current_index': current_index,
        'next_index': next_index,
        'is_last': next_index >= len(questions),
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

    request.user.update_streak()

    if session_key in request.session:
        del request.session[session_key]

    return render(request, 'lessons/quiz_complete.html', {
        'lesson': lesson,
        'correct': correct,
        'total': total,
        'score_percent': score_percent,
        'streak': request.user.streak,
    })


# ---------------------------------------------------------------------------
# Review views
# ---------------------------------------------------------------------------

@login_required
def review_quiz(request):
    user = request.user
    language = user.active_language
    if not language:
        return redirect('add_language')

    completed_lesson_ids = set(
        UserLessonProgress.objects.filter(
            user=user, lesson__language=language, completed=True
        ).values_list('lesson_id', flat=True)
    )

    if not completed_lesson_ids:
        return redirect('lesson_list')

    session_key = 'quiz_review'

    if session_key not in request.session or 'restart' in request.GET:
        all_phrases = list(Phrase.objects.filter(lesson__in=completed_lesson_ids))
        random.shuffle(all_phrases)
        selected = all_phrases[:15]
        request.session[session_key] = {
            'questions': _build_questions(selected),
            'answers': {},
            'last_result': None,
        }

    quiz_data = request.session[session_key]
    questions = quiz_data['questions']
    current_index = int(request.GET.get('q', 0))

    if current_index >= len(questions):
        return redirect('review_complete')

    current_q = questions[current_index]
    phrase_id = current_q['id']
    q_type = current_q['type']
    current_phrase = get_object_or_404(Phrase, id=phrase_id)

    # POST — submit answer
    if request.method == 'POST':
        chosen = request.POST.get('chosen', '')[:_MAX_ANSWER_LEN]

        # Derive the correct answer server-side — never trust the client
        blank_word = current_q.get('blank_word')
        if q_type == 'translate':
            correct = current_phrase.translation
        elif q_type == 'reverse':
            correct = current_phrase.original
        else:  # fill_blank
            correct = blank_word or ''

        is_correct = chosen.strip() == correct.strip()

        quiz_data['answers'][str(phrase_id)] = is_correct
        quiz_data['last_result'] = {
            'is_correct': is_correct,
            'correct_answer': correct,
            'question_type': q_type,
        }
        request.session[session_key] = quiz_data
        request.session.modified = True

        url = reverse('review_quiz') + f'?q={current_index}&answered=1'
        return redirect(url)

    # GET — build question context
    show_result = 'answered' in request.GET
    last_result = quiz_data.get('last_result') if show_result else None

    blank_word = current_q.get('blank_word')
    if q_type == 'translate':
        question_text = current_phrase.original
        correct_answer = current_phrase.translation
        show_pronunciation = True
    elif q_type == 'reverse':
        question_text = current_phrase.translation
        correct_answer = current_phrase.original
        show_pronunciation = False
    else:  # fill_blank
        question_text = current_phrase.original.replace(blank_word, '___', 1)
        correct_answer = blank_word
        show_pronunciation = True

    distractors = _get_distractors(q_type, language, phrase_id, correct_answer, blank_word)
    choices = distractors + [correct_answer]
    random.shuffle(choices)

    next_index = current_index + 1

    return render(request, 'lessons/review_quiz.html', {
        'language': language,
        'phrase': current_phrase,
        'question_text': question_text,
        'question_type': q_type,
        'show_pronunciation': show_pronunciation,
        'correct_answer': correct_answer,
        'choices': choices,
        'current': current_index + 1,
        'total': len(questions),
        'current_index': current_index,
        'next_index': next_index,
        'is_last': next_index >= len(questions),
        'show_result': show_result,
        'last_result': last_result,
    })


@login_required
def review_complete(request):
    session_key = 'quiz_review'
    quiz_data = request.session.get(session_key, {})
    answers = quiz_data.get('answers', {})

    if not answers:
        return redirect('lesson_list')

    correct = sum(1 for v in answers.values() if v)
    total = len(answers)
    score_percent = int(correct / total * 100) if total else 0

    request.user.update_streak()

    if session_key in request.session:
        del request.session[session_key]

    return render(request, 'lessons/review_complete.html', {
        'correct': correct,
        'total': total,
        'score_percent': score_percent,
        'streak': request.user.streak,
    })


# ---------------------------------------------------------------------------
# Favorites views
# ---------------------------------------------------------------------------

@login_required
@require_POST
def toggle_favorite(request, phrase_id):
    phrase = get_object_or_404(Phrase, id=phrase_id)
    fav, created = FavoritePhrase.objects.get_or_create(user=request.user, phrase=phrase)
    if not created:
        fav.delete()

    fallback = reverse('lesson_detail', args=[phrase.lesson.id])
    next_url = request.POST.get('next', fallback)

    # Reject redirects to external hosts (open redirect prevention)
    if not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        next_url = fallback

    return redirect(next_url)


@login_required
def favorites_list(request):
    favorites = (
        FavoritePhrase.objects
        .filter(user=request.user)
        .select_related('phrase__lesson__language')
    )
    return render(request, 'lessons/favorites.html', {'favorites': favorites})

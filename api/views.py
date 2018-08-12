import datetime
import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect

from compose.models import DailyEntry, get_current_streak, get_longest_streak


@login_required
def fetch(request):
    today = datetime.date.today()
    user = request.user

    entry = DailyEntry.objects.today(user=user)
    total_word_count = sum(e.word_count
        for e in DailyEntry.objects.filter(user=user, date__lt=today))
    word_count_this_month = sum(e.word_count
        for e in DailyEntry.objects.filter(user=user, date__month=today.month))
    response = {
        'longest_streak': get_longest_streak(user),
        'streak_length': get_current_streak(user),
        'text': entry.text,
        'total_word_count': total_word_count,
        'word_count': entry.word_count,
        'word_count_goal': entry.word_count_goal,
        'word_count_this_month': word_count_this_month,
    }
    return JsonResponse(response)


@login_required
def update(request):
    if request.method == 'POST':
        try:
            obj = json.loads(request.body.decode('utf-8'))
        except (json.JSONDecodeError, UnicodeDecodeError):
            return HttpResponse(status_code=400)

        text = obj.get('text')
        word_count_goal = obj.get('word_count_goal')

        entry = DailyEntry.objects.today(user=request.user)
        if text is not None:
            entry.text = text
        if word_count_goal is not None:
            entry.word_count_goal = word_count_goal
        entry.save()
        return HttpResponse()
    else:
        return redirect('compose:index')

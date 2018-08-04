import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect

from compose.models import DailyEntry


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
        if text:
            entry.text = text
        if word_count_goal:
            entry.word_count_goal = word_count_goal
        entry.save()
        return HttpResponse()
    else:
        return redirect('compose:index')

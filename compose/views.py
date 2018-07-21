import datetime
import json

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .models import DailyWriting


def index(request):
    today = datetime.date.today()
    try:
        dailywriting = DailyWriting.objects.get(date=today)
    except DailyWriting.DoesNotExist:
        text = ''
    else:
        text = dailywriting.text
    past_writing = DailyWriting.objects.filter(date__lt=today).order_by('-date')
    word_count = sum(w.word_count for w in past_writing)
    context = {'writing': text, 'past': past_writing,
        'word_count': word_count}
    return render(request, 'compose/index.html', context)

def upload(request):
    if request.method == 'POST':
        obj = json.loads(request.body.decode('utf-8'))
        text = obj['text']
        dailywriting, created = DailyWriting.objects.get_or_create(
                date=datetime.date.today())
        if text:
            dailywriting.text = text
            dailywriting.save()
        else:
            dailywriting.delete()
        return HttpResponse()
    else:
        return redirect('compose:index')

def archive(request, year, month, day):
    today = datetime.date.today()
    date = datetime.date(year, month, day)
    dailywriting = get_object_or_404(DailyWriting, date=date)
    past_writing = DailyWriting.objects.filter(date__lt=today).order_by('-date')
    context = {'writing': dailywriting, 'past': past_writing}
    return render(request, 'compose/archive.html', context)

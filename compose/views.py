import datetime
import json

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .models import DailyWriting


def index(request):
    today = datetime.date.today()
    dailywriting, _ = DailyWriting.objects.get_or_create(date=today)
    past_writing = DailyWriting.objects.filter(date__lt=today)
    context = {'saved_text': dailywriting.text, 'past': past_writing}
    return render(request, 'compose/index.html', context)

def upload(request):
    if request.method == 'POST':
        obj = json.loads(request.body.decode('utf-8'))
        text = obj['text']
        dailywriting, _ = DailyWriting.objects.get_or_create(
                date=datetime.date.today())
        dailywriting.text = text
        dailywriting.save()
        return HttpResponse()
    else:
        print('Redirecting!')
        return redirect('compose:index')

def archive(request, year, month, day):
    date = datetime.date(year, month, day)
    dailywriting = get_object_or_404(DailyWriting, date=date)
    context = {'writing': dailywriting}
    return render(request, 'compose/archive.html', context)

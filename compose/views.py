import datetime

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
    if request.POST:
        text = request.POST['text']
        dailywriting, _ = DailyWriting.objects.get_or_create(
                date=datetime.date.today())
        dailywriting.text = text
        if len(text) > len(dailywriting.backup):
            dailywriting.backup = text
        dailywriting.save()
        return HttpResponse()
    else:
        return redirect('compose:index')

def archive(request, year, month, day):
    date = datetime.date(year, month, day)
    dailywriting = get_object_or_404(DailyWriting, date=date)
    context = {'writing': dailywriting}
    return render(request, 'compose/archive.html', context)

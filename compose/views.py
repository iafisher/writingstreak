import datetime

from django.http import HttpResponse
from django.shortcuts import redirect, render

from .models import DailyWriting


def index(request):
    dailywriting, _ = DailyWriting.objects.get_or_create(
            date=datetime.date.today())
    context = {
        'saved_text': dailywriting.text
    }
    return render(request, 'compose/index.html', context)

def upload(request):
    if request.POST:
        text = request.POST['text']
        dailywriting, _ = DailyWriting.objects.get_or_create(
                date=datetime.date.today())
        dailywriting.text = text
        dailywriting.save()
        return HttpResponse()
    else:
        return redirect('compose:index')

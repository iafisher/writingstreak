import datetime
import json

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .models import DailyEntry, get_current_streak


@login_required
def index(request):
    entry = DailyEntry.objects.today(user=request.user)
    past_entries = DailyEntry.objects.filter(date__lt=datetime.date.today(),
        user=request.user).order_by('-date')
    total_word_count = sum(e.word_count for e in past_entries)
    words_to_goal = max(entry.word_count_goal - entry.word_count, 0)
    context = {
        'entry': entry,
        'past_entries': past_entries,
        'streak_length': get_current_streak(request.user),
        'total_word_count': total_word_count,
        'user': request.user,
        'words_to_goal': words_to_goal
    }
    return render(request, 'compose/index.html', context)


@login_required
def update_text(request):
    if request.method == 'POST':
        obj = json.loads(request.body.decode('utf-8'))
        text = obj['text']
        entry = DailyEntry.objects.today(user=request.user)
        entry.text = text
        entry.save()
        return HttpResponse()
    else:
        return redirect('compose:index')


@login_required
def update_word_count(request):
    if request.method == 'POST':
        try:
            obj = json.loads(request.body.decode('utf-8'))
            new_wc = obj['wordCountGoal']
        except (UnicodeDecodeError, json.decoder.JSONDecodeError, KeyError):
            return HttpResponse(status_code=400)

        entry = DailyEntry.objects.today(user=request.user)
        entry.word_count_goal = new_wc
        entry.save()
        return HttpResponse()
    else:
        return redirect('compose:index')


@login_required
def archive(request, year, month, day):
    today = datetime.date.today()
    date = datetime.date(year, month, day)
    dailywriting = get_object_or_404(DailyEntry, date=date, user=request.user)
    past_writing = DailyEntry.objects.filter(date__lt=today,
        user=request.user).order_by('-date')
    context = {'writing': dailywriting, 'past': past_writing,
        'user': request.user}
    return render(request, 'compose/archive.html', context)


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect(request.POST['next'] or '/')
        else:
            blank_form = AuthenticationForm()
            context = {
                'form': blank_form,
                'errormsg': 'Invalid username or password',
            }
            return render(request, 'compose/login.html', context)
    else:
        form = AuthenticationForm()
        context = {
            'form': form,
            'next': request.GET.get('next')
        }
        return render(request, 'compose/login.html', context)


def logout(request):
    auth.logout(request)
    return redirect('compose:login')

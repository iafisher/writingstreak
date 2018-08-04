import datetime
import itertools
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
    past_entries_by_month = get_past_entries_by_month(request.user)

    total_word_count = sum(e.word_count
        for _, past_entries in past_entries_by_month
        for e in past_entries)
    words_to_goal = max(entry.word_count_goal - entry.word_count, 0)
    context = {
        'entry': entry,
        'past_entries_by_month': past_entries_by_month,
        'streak_length': get_current_streak(request.user),
        'total_word_count': total_word_count,
        'user': request.user,
        'words_to_goal': words_to_goal
    }
    return render(request, 'compose/index.html', context)


def get_past_entries_by_month(user, *, exclude=None):
    """Return a list of (month, entries) pairs in reverse chronological order,
    where `month` is the month and year as a string and `entries` is a list of
    DailyEntry objects, also in reverse chronological order.
    """
    past_entries = DailyEntry.objects.filter(date__lt=datetime.date.today(),
        user=user).exclude(date=exclude).order_by('-date')
    key = lambda e: (e.date.month, e.date.year)
    return [month(g) for _, g in itertools.groupby(past_entries, key)]


def month(entrygroup):
    entrygroup = list(entrygroup)
    return (entrygroup[0].date.strftime('%B %Y'), entrygroup)


@login_required
def update(request):
    if request.method == 'POST':
        try:
            obj = json.loads(request.body.decode('utf-8'))
        except (JSONDecodeError, UnicodeDecodeError):
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


@login_required
def archive(request, year, month, day):
    date = datetime.date(year, month, day)
    entry = get_object_or_404(DailyEntry, date=date, user=request.user)
    past_entries_by_month = get_past_entries_by_month(request.user,
        exclude=date)
    context = {
        'entry': entry,
        'past_entries_by_month': past_entries_by_month,
        'user': request.user
    }
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

import datetime
import itertools

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import get_object_or_404, redirect, render

from .models import DailyEntry, get_current_streak


@login_required
def index(request):
    past_entries_by_month = get_past_entries_by_month(request.user)
    context = {
        'past_entries_by_month': past_entries_by_month,
        'user': request.user,
    }
    return render(request, 'compose/index.html', context)


def get_past_entries_by_month(user, *, exclude=None):
    """Return a list of (month, entries) pairs in reverse chronological order,
    where `month` is the month and year as a string and `entries` is a list of
    DailyEntry objects, also in reverse chronological order.
    """
    past_entries = DailyEntry.objects \
        .filter(date__lt=datetime.date.today(), user=user) \
        .exclude(date=exclude) \
        .exclude(word_count=0) \
        .order_by('-date')
    key = lambda e: (e.date.month, e.date.year)
    return [month(g) for _, g in itertools.groupby(past_entries, key)]


def month(entrygroup):
    entrygroup = list(entrygroup)
    return (entrygroup[0].date.strftime('%B %Y'), entrygroup)


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
        if request.user.is_authenticated:
            return redirect('/')

        form = AuthenticationForm()
        context = {
            'form': form,
            'next': request.GET.get('next')
        }
        return render(request, 'compose/login.html', context)


def logout(request):
    auth.logout(request)
    return redirect('compose:login')

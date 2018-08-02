import datetime
import json

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.db.models.fields import related_descriptors
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .models import DailyWriting, WSUser


@login_required
def index(request):
    try:
        wsuser = request.user.wsuser
    except related_descriptors.RelatedObjectDoesNotExist:
        wsuser = WSUser(user=request.user)
        wsuser.save()

    today = datetime.date.today()
    try:
        dailywriting = DailyWriting.objects.get(date=today, user=wsuser)
    except DailyWriting.DoesNotExist:
        text = ''
    else:
        text = dailywriting.text

    past_writing = DailyWriting.objects.filter(date__lt=today, user=wsuser) \
        .order_by('-date')
    word_count = sum(w.word_count for w in past_writing)
    context = {'writing': text, 'past': past_writing,
        'word_count': word_count, 'user': wsuser}
    return render(request, 'compose/index.html', context)


@login_required
def upload(request):
    if request.method == 'POST':
        obj = json.loads(request.body.decode('utf-8'))
        text = obj['text']
        dailywriting, created = DailyWriting.objects.get_or_create(
                date=datetime.date.today(), user=request.user.wsuser)
        if text:
            dailywriting.text = text
            dailywriting.save()
        else:
            dailywriting.delete()
        return HttpResponse()
    else:
        return redirect('compose:index')


@login_required
def update_wc(request):
    if request.method == 'POST':
        obj = json.loads(request.body.decode('utf-8'))
        new_wc = obj['wordCount']
        request.user.wsuser.word_count = new_wc
        request.user.wsuser.save()
        return HttpResponse()
    else:
        return redirect('compose:index')


@login_required
def archive(request, year, month, day):
    today = datetime.date.today()
    date = datetime.date(year, month, day)
    dailywriting = get_object_or_404(DailyWriting, date=date,
        user=request.user.wsuser)
    past_writing = DailyWriting.objects.filter(date__lt=today) \
        .order_by('-date')
    context = {'writing': dailywriting, 'past': past_writing,
        'user': request.user.wsuser}
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

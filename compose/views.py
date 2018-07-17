from django.http import HttpResponse
from django.shortcuts import redirect, render

def index(request):
    return render(request, 'compose/index.html')

def upload(request):
    if request.POST:
        text = request.POST['text']
        print(text)
        return HttpResponse()
    else:
        return redirect('compose:index')

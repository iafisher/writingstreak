from django.shortcuts import render

def index(request):
    return render(request, 'compose/index.html')

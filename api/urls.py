from django.urls import path

from . import views

app_name = 'api'

urlpatterns = [
    path('fetch', views.fetch, name='fetch'),
    path('update', views.update, name='update'),
]

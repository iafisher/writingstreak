from django.urls import path

from . import views

app_name = 'compose'

urlpatterns = [
    path('', views.index, name='index'),
    path('upload', views.upload, name='upload'),
    path('archive/<int:year>/<int:month>/<int:day>', views.archive,
        name='archive'),
]

from django.urls import path

from . import views

app_name = 'compose'

urlpatterns = [
    path('', views.index, name='index'),
    path('archive/<int:year>/<int:month>/<int:day>', views.archive,
        name='archive'),

    path('login', views.login, name='login'),
    path('login/', views.login, name='login'),
    path('logout', views.logout, name='logout'),
]

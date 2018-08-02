from django.urls import include, path

from . import views

app_name = 'compose'

urlpatterns = [
    path('', views.index, name='index'),
    path('archive/<int:year>/<int:month>/<int:day>', views.archive,
        name='archive'),

    path('login', views.login, name='login'),
    path('login/', views.login, name='login'),
    path('logout', views.logout, name='logout'),

    path('upload', views.upload, name='upload'),
    path('update_wc', views.update_wc, name='update_wc'),
]

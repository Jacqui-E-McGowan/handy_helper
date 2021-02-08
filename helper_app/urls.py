from django.urls import path     
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('dashboard', views.dashboard),
    path('new', views.new),
    path('create', views.create),
    path('dashboard/<int:job_id>/edit', views.edit),
    path('dashboard/<int:job_id>/update', views.update),
    path('dashboard/<int:job_id>/details', views.details),
    path('dashboard/<int:job_id>/add', views.add),
    path('dashboard/<int:job_id>/remove', views.remove),
    path('dashboard/<int:job_id>/giveup', views.giveup),
    path('logout', views.logout),
]
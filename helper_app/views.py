from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
    return render(request, 'index.html')

def register(request):
    errors = User.objects.register_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        )
    request.session['user_id'] = user.id 
    request.session['greeting'] = user.first_name
    return redirect('/dashboard')

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.get(email=request.POST['login_email'])
        request.session['user_id'] = user.id
        request.session['greeting'] = user.first_name
        return redirect('/dashboard')

def dashboard(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        context = {
            'jobs': Job.objects.all(),
            'this_user': User.objects.get(id=request.session['user_id'])
        }
    return render(request, 'dashboard.html', context)
    
def new(request):
    return render(request, 'new.html')

def create(request):
    errors = Job.objects.job_validator(request.POST)
    if errors:
        for (key, value) in errors.items():
            messages.error(request, value)
        return redirect('/new')
    
    else:
        user = User.objects.get(id=request.session['user_id'])
        job = Job.objects.create(
            title = request.POST['title'],
            description = request.POST['description'],
            location = request.POST['location'],
            category = request.POST['category'],
            created_by = user
        )

        return redirect('/dashboard')

def edit(request, job_id):
    one_job = Job.objects.get(id=job_id)
    context = {
        'job': one_job
    }
    return render(request, 'edit.html', context)

def update(request, job_id):
    job = Job.objects.get(id=job_id)
    errors = Job.objects.edit_validator(request.POST)
    if errors:
        for (key, value) in errors.items():
            messages.error(request, value)
        return redirect(f'/dashboard/{job.id}/edit')

    job = Job.objects.get(id=job_id)
    to_update = Job.objects.get(id=job_id)
    to_update.title = request.POST['title']
    to_update.description = request.POST['description']
    to_update.description = request.POST['location']
    to_update.save()

    return redirect('/dashboard')

def details(request, job_id):
    context = {
        'jobs': Job.objects.all(),
        'job': Job.objects.get(id=job_id),
        'current_user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'details.html', context)

def add(request, job_id):
    user = User.objects.get(id=request.session['user_id'])
    job = Job.objects.get(id=job_id)
    user.added.add(job)

    return redirect('/dashboard')

def remove(request, job_id):
    job = Job.objects.get(id=job_id)
    job.delete()

    return redirect('/dashboard')

def giveup(request, job_id):
    user = User.objects.get(id=request.session['user_id'])
    job = Job.objects.get(id=job_id)
    user.added.remove(job)

    return redirect('/dashboard')

def logout(request):
    request.session.flush()
    return redirect('/')


# from .forms import UpdateProfile
from .utils import client, db
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import PasswordChangeView
from .forms import UpdateProfile
from .forms import SignupForm
from .forms import ContactForm
from django.http import JsonResponse

from .models import FileShare, Contact
from .forms import FileUploadForm, FileShareForm

from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import logout, login
from django.contrib.auth.models import User
from django.contrib import messages

# from .models import File

import os
from django.http import Http404, FileResponse
from django.conf import settings

from .models import UploadedFile, FileShare
import uuid
from django.views.generic.list import ListView

from django.views.generic.edit import CreateView
# Create your views here.
from django.contrib.auth.decorators import login_required


@login_required
def index(request):

    return render(request, 'index.html')


def signupUser(request):
    print("new account")
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data['full_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            user_data = {
                "username": username,
                "full_name": full_name,
                "email": email
            }
            try:
                users_collection = db['users']
                users_collection.insert_one(user_data)
            except Exception as e:
                print(f"Error inserting user data: {e}")

            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            if password1 == password2:
                user = form.save()
                login(request, user)
                messages.success(request, "Account created successfully")
                return redirect('/login')
            else:
                messages.error(request, "Error! Check again")
                form.add_error('password2', 'Passwords do not match.')

    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def loginUser(request):

    print("Hello login")
    if request.method == "POST":
        print("Wah ji wha")

        username = request.POST.get('username')
        password = request.POST.get('password')

        print(username, password)
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'index.html')

        else:
            messages.error(request, "Invalid username or password")
            return render(request, 'login.html')
    return render(request, 'login.html')


@login_required
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            username = request.user.username
            email = form.cleaned_data['email']
            desc = form.cleaned_data['desc']
            contact_data = {
                "username": username,
                "email": email,
                "desc": desc}
            contact_collection = db['contactissues']
            contact_collection.insert_one(contact_data)
            uploaded_issue = form.save(commit=False)
            uploaded_issue.user = request.user
            uploaded_issue.save()
            return redirect('/contact')
    else:
        form = ContactForm()
        return render(request, 'Contact.html', {'form': form})

    return render(request, 'Contact.html')


@login_required
def uploadedfiles(request):

    files = UploadedFile.objects.filter(user=request.user)
    return render(request, 'Uploadedfiles.html', {'files': files})


@login_required
def upload(request):

    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():

            uploaded_file = form.save(commit=False)
            uploaded_file.user = request.user

            uploaded_file.save()
            uploadedfiles_data = {
                'uploaded_file_path': uploaded_file.file.url
            }
            uploadedfilescollection = db['uploaded_files']
            uploadedfilescollection.insert_one(uploadedfiles_data)

            return redirect('/uploadedfiles')
    else:
        form = FileUploadForm()
        return render(request, 'Fileupload.html', {'form': form})

    return render(request, 'Fileupload.html')


def logoutUser(request):
    logout(request)
    return redirect('/login')


@login_required
def profile(request):
    user = request.user
    sent_files = FileShare.objects.filter(sender=request.user)

    return render(request, 'profile.html', {'sent_files': sent_files})


@login_required
def share(request):

    if request.method == 'POST':
        form = FileShareForm(request.POST, request.FILES)
        print(form.data)
        print(request.POST)
        if form.is_valid():
            print("share")

            share = form.save(commit=False)
            share.sender = request.user
            share.save()

            share_data = {
                'sender': share.sender.username,
                'shared_at': share.shared_at,
                "shared_file": share.file.url
            }
            sharefiles_collection = db['shared_files']
            sharefiles_collection.insert_one(share_data)
            print(share.sender)
            print(share.shared_at)
            messages.success(request, 'File sent successfully!')
            return redirect('profile')
        else:
            print(form.errors)

    form = FileShareForm()

    return render(request, 'fileshare.html', {'form': form})


@login_required
def inbox(request):
    received_files = FileShare.objects.filter(
        receiver=request.user)

    return render(request, 'inbox.html', {'received_files': received_files})


@login_required
def updateprofile(request):
    user = request.user
    if request.method == 'POST':
        form = UpdateProfile(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('/profile')
    else:
        form = UpdateProfile(instance=user)
    return render(request, 'updateprofile.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('profile')

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .forms import RegisterForm, EmergencyContactForm
from .models import EmergencyContact


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('accounts:login')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'accounts/login.html')


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('accounts:login')

@login_required
def profile(request):
    contacts = request.user.emergencycontact_set.all()
    return render(request, 'accounts/profile.html', {
        'user': request.user,
        'contacts': contacts
    })



@login_required
def add_contact(request):
    if request.method == 'POST':
        form = EmergencyContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user
            contact.save()
            messages.success(request, 'Contact added!')
            return redirect('accounts:profile')
    else:
        form = EmergencyContactForm()
    return render(request, 'accounts/add_contact.html', {'form': form})


@login_required
def update_contact(request, pk):
    contact = get_object_or_404(EmergencyContact, pk=pk, user=request.user)
    if request.method == 'POST':
        form = EmergencyContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contact updated!')
            return redirect('accounts:profile')
    else:
        form = EmergencyContactForm(instance=contact)
    return render(request, 'accounts/update_contact.html', {'form': form})


@login_required
def delete_contact(request, pk):
    contact = get_object_or_404(EmergencyContact, pk=pk, user=request.user)
    if request.method == 'POST':
        contact.delete()
        messages.success(request, 'Contact deleted!')
        return redirect('accounts:profile')
    return render(request, 'accounts/delete_contact.html', {'contact': contact})
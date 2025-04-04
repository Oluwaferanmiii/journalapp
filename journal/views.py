from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import JournalEntry
from .forms import JournalEntryForm
from django.db.models import Q


def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Registration successful! Please log in.")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'journal/register.html', {'form': form})


def login_user(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
        messages.error(request, "Invalid username or password")
    else:
        form = AuthenticationForm()
    return render(request, 'journal/login.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard_view(request):
    entries = JournalEntry.objects.filter(
        user=request.user).order_by('-created_at')
    return render(request, 'journal/dashboard.html', {'entries': entries})


@login_required
def create_entry_view(request):
    entries = JournalEntry.objects.filter(
        user=request.user).order_by('-created_at')
    if request.method == "POST":
        form = JournalEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            return redirect('dashboard')
    else:
        form = JournalEntryForm()
    return render(request, 'journal/dashboard.html', {'form': form, 'entries': entries})


@login_required
def edit_entry_view(request, entry_id):
    entry = get_object_or_404(JournalEntry, id=entry_id, user=request.user)
    entries = JournalEntry.objects.filter(
        user=request.user).order_by('-created_at')
    if request.method == "POST":
        form = JournalEntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = JournalEntryForm(instance=entry)
    return render(request, 'journal/dashboard.html', {'form': form, 'entry': entry, 'entries': entries})


@login_required
def delete_entry_view(request, entry_id):
    entry = get_object_or_404(JournalEntry, id=entry_id, user=request.user)
    entries = JournalEntry.objects.filter(
        user=request.user).order_by('-created_at')
    if request.method == "POST":
        entry.delete()
        return redirect('dashboard')
    return render(request, 'journal/dashboard.html', {'entry': entry, 'entries': entries})


@login_required
def search_entries_view(request):
    query = request.GET.get('q', '')
    entries = JournalEntry.objects.filter(Q(title__icontains=query) | Q(
        content__icontains=query), user=request.user).order_by('-created_at')
    return render(request, 'journal/dashboard.html', {'entries': entries, 'query': query})


@login_required
def filter_by_mood_view(request, mood):
    entries = JournalEntry.objects.filter(
        user=request.user, mood=mood).order_by('-created_at')
    return render(request, 'journal/dashboard.html', {'entries': entries, 'mood_filter': mood})

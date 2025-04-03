from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
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
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'journal/register.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            messages.error(request, "Invalid username or password")
        return render(request, 'journal/login.html')


def logout_user(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard_view(request):
    if request.method == "POST":
        entries = JournalEntry.objects.filter(
            user=request.user).order_by('-created_at')
        return render(request, 'journal/dashboard.html', {'entries': entries})


@login_required
def create_entry_view(request):
    if request.method == "POST":
        form = JournalEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            return redirect('dashboard')
    else:
        form = JournalEntryForm()
    return render(request, 'journal/new_entry.html', {'form': form})


@login_required
def edit_entry_view(request, entry_id):
    entry = get_object_or_404(JournalEntry, id=entry_id, user=request.user)
    if request.method == "POST":
        form = JournalEntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            return redirect('entry_detail', entry_id=entry.id)
    else:
        form = JournalEntryForm(instance=entry)
    return render(request, 'journal/edit_entry.html', {'form': form, 'entry': entry})


@login_required
def delete_entry_view(request, entry_id):
    entry = get_object_or_404(JournalEntry, id=entry_id, user=request.user)
    if request.method == "POST":
        entry.delete()
        return redirect('dashboard')
    return render(request, 'journal/delete_entry.html', {'entry': entry})


@login_required
def search_entries_view(request):
    query = request.GET.get('q', '')
    entries = JournalEntry.objects.filter(Q(title__icontains=query) | Q(
        content__icontain=query), user=request.user).order_by('-created_at')
    return render(request, 'journal/dashboard.html', {'entries': entries, 'query': query})


@login_required
def filter_by_mood_view(request, mood):
    entries = JournalEntry.objects.filter(
        user=request.user, mood=mood).order_by('-created_at')
    return render(request, 'journal/dashboard.html', {'entries': entries, 'mood_filter': mood})

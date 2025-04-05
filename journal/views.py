from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import JournalEntry
from .forms import JournalEntryForm
from django.db.models import Q
from datetime import datetime
import re


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

    # Calculate statistics
    current_year = datetime.now().year  # 2025
    entries_this_year = entries.filter(created_at__year=current_year).count()

    # Words Written: Count total words in title + content
    total_words = 0
    for entry in entries:
        title_words = len(re.findall(r'\w+', entry.title)
                          ) if entry.title else 0
        content_words = len(re.findall(r'\w+', entry.content)
                            ) if entry.content else 0
        total_words += title_words + content_words

    # Days Journaled: Count unique days with entries
    unique_days = len(set(entry.created_at.date() for entry in entries))

    return render(request, 'journal/dashboard.html', {
        'entries': entries,
        'entries_this_year': entries_this_year,
        'total_words': total_words,
        'days_journaled': unique_days,
    })


@login_required
def entry_view(request, entry_id=None):
    if entry_id:
        entry = get_object_or_404(JournalEntry, id=entry_id, user=request.user)
        initial_content = f"{entry.title}\n{entry.content or ''}"
        initial_mood = entry.mood
    else:
        entry = None
        initial_content = ""
        initial_mood = "Neutral"

    if request.method == "POST":
        content = request.POST.get('content', '')
        lines = content.split('\n', 1)
        title = lines[0].strip() if lines else "Untitled entry"
        content_body = lines[1].strip() if len(lines) > 1 else ""
        mood = request.POST.get('mood', 'neutral')

        if entry:  # Editing an existing entry
            entry.title = title
            entry.content = content_body
            entry.mood = mood
            entry.save()
            messages.success(request, "Entry saved successfully!")
        else:  # Creating a new entry
            entry = JournalEntry.objects.create(
                user=request.user,
                title=title,
                content=content_body,
                mood=mood
            )
            messages.success(request, "Entry created successfully!")
        return redirect('dashboard')

    return render(request, 'journal/entry.html', {
        'entry': entry,
        'initial_content': initial_content,
        'initial_mood': initial_mood,
    })


@login_required
def delete_entry_view(request, entry_id):
    entry = get_object_or_404(JournalEntry, id=entry_id, user=request.user)
    if request.method == "POST":
        entry.delete()
        messages.success(request, "Entry deleted successfully!")
        return redirect('dashboard')
    return redirect('dashboard')


@login_required
def search_entries_view(request):
    query = request.GET.get('q', '')
    entries = JournalEntry.objects.filter(
        Q(title__icontains=query) | Q(content__icontains=query),
        user=request.user
    ).order_by('-created_at')
    return render(request, 'journal/dashboard.html', {
        'entries': entries,
        'query': query,
        'search_active': True,  # Add flag to indicate search page
        'entries_this_year': entries.filter(created_at__year=datetime.now().year).count(),
        'total_words': sum(len(re.findall(r'\w+', entry.title)) + len(re.findall(r'\w+', entry.content or '')) for entry in entries),
        'days_journaled': len(set(entry.created_at.date() for entry in entries)),
    })


@login_required
def filter_by_mood_view(request, mood):
    entries = JournalEntry.objects.filter(
        user=request.user, mood=mood).order_by('-created_at')
    return render(request, 'journal/dashboard.html', {
        'entries': entries,
        'mood_filter': mood,
        'entries_this_year': entries.filter(created_at__year=datetime.now().year).count(),
        'total_words': sum(len(re.findall(r'\w+', entry.title)) + len(re.findall(r'\w+', entry.content or '')) for entry in entries),
        'days_journaled': len(set(entry.created_at.date() for entry in entries)),
    })

from django.db import models
from django.contrib.auth.models import User


class JournalEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, default="Untitled Entry")
    content = models.TextField(blank=True, null=True)
    mood = models.CharField(
        max_length=10,
        choices=[('Happy', 'Happy'), ('Sad', 'Sad'), ('Neutral', 'Neutral')]
    )
    created_at = models.DateTimeField(auto_now_add=True)


def __str__(self):
    return self.title

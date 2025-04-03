from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_entry_view, name="create_entry")
]

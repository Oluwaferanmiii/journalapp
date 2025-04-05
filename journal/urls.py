from django.urls import path
from . import views

urlpatterns = [
    # path('', views.create_entry_view, name="create_entry")
    # path('login/', views.login_user, name="login")
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('entry/', views.entry_view, name='entry'),
    path('entry/<int:entry_id>/', views.entry_view, name='entry'),
    path('delete/<int:entry_id>/', views.delete_entry_view, name='delete_entry'),
    path('search/', views.search_entries_view, name='search_entries'),
    path('filter/<str:mood>/', views.filter_by_mood_view, name='filter_by_mood'),
    path('', views.login_user, name='root'),
]

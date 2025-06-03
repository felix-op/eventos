from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    HomeView,
    EventListView,
    EventDetailView,
    UserDashboard,
)
from . import views

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("profile/", UserDashboard.as_view(), name="user_dashboard"),
    path("events/", EventListView.as_view(), name="events"),
    path("events/<int:pk>/", EventDetailView.as_view(), name="event_detail"),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='app/pages/login.html'), name='login'),
    path('components/notifications_preview.html', views.get_noti_preview_list, name='notifications_preview'),
]

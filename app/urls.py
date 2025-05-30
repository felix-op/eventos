from django.urls import path
from .views import (
    HomeView,
    EventListView,
    EventDetailView,
    UserDashboard,
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("profile/", UserDashboard.as_view(), name="user_dashboard"),
    path("events/", EventListView.as_view(), name="events"),
    path("events/<int:pk>/", EventDetailView.as_view(), name="event_detail"),
]

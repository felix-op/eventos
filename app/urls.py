from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import (
    HomeView,
    EventListView,
    EventDetailView,
    UserDashboard,
    RegisterView,
    NotificationListView,
    NotificationDetailView,
    #MarkNotificationReadView,
    CommentUpdateView,
    CommentDeleteView,
    RefundRequestCreateView,
    AccessDeniedView,
    CommentCreateView,
)


urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("profile/", UserDashboard.as_view(), name="user_dashboard"),
    path("events/", EventListView.as_view(), name="events"),
    path("events/<int:pk>/", EventDetailView.as_view(), name="event_detail"),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('login/', views.LoginManualView.as_view(), name="login"),
    path('register/',RegisterView.as_view(), name='register'),
    path('notifications/', NotificationListView.as_view(), name='notifications'),
    #path("notifications/<int:pk>/", NotificationDetailView.as_view(), name="notification_detail"),
    #path("notifications/<int:pk>/mark_read/", MarkNotificationReadView.as_view(), name="notification_mark_read"),
    path('comment/create/<int:event_id>/', CommentCreateView.as_view(), name='comment_create'),
    path('comment/update/<int:pk>/', CommentUpdateView.as_view(), name='comment_update'),
    path('comment/delete/<int:pk>/', CommentDeleteView.as_view(), name='comment_delete'),
    path('refund/create/<int:ticket_id>/', RefundRequestCreateView.as_view(), name='refund_create'),
    path('access-denied/', AccessDeniedView.as_view(), name='access-denied'),

]

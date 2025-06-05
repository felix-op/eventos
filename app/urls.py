from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import (
    HomeView,
    EventListView,
    EventDetailView,
    UserDashboard,
    RegisterView,
    CommentUpdateView,
    CommentDeleteView,
    RefundRequestCreateView
)


urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("profile/", UserDashboard.as_view(), name="user_dashboard"),
    path("events/", EventListView.as_view(), name="events"),
    path("events/<int:pk>/", EventDetailView.as_view(), name="event_detail"),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('login/', views.LoginManualView.as_view(), name="login"),
    path('register/',RegisterView.as_view(), name='register'),
    path('components/notifications_preview.html', views.get_noti_preview_list, name='notifications_preview'),
    path('comment/update/<int:pk>/', CommentUpdateView.as_view(), name='comment_update'),
    path('comment/delete/<int:pk>/', CommentDeleteView.as_view(), name='comment_delete'),
    path('refund/create/<int:ticket_id>/', RefundRequestCreateView.as_view(), name='refund_create'),

]

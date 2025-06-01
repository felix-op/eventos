from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, DetailView
from .models import Event, Notification, Ticket
from django.shortcuts import render


class HomeView(TemplateView):
    template_name = "home.html"

class NavView(TemplateView):
    template_name = "nav.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario_logueado'] = self.request.user.is_authenticated
        return context


class EventListView(ListView):
    model = Event
    template_name = "app/events.html"
    context_object_name = "events"

    def get_queryset(self):
        return Event.objects.all().order_by("date")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class UserDashboard(LoginRequiredMixin,TemplateView):
    template_name = "user_dashboard.html"

    def get_queryset(self):
        return Ticket.objects.all()
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tickets'] = Ticket.objects.all()
        return context


class EventDetailView(DetailView):
    model = Event
    template_name = "app/event_detail.html"
    context_object_name = "event"

class NotificationListView(ListView):
    model = Notification
    template_name = "app/notifications.html"
    context_object_name = "notifications"
    
    def get_queryset(self):
        return Notification.objects.all().order_by("create_at")
    
    def get_context_data(self, **kwargs):
        context = super(NotificationListView, self).get_context_data(**kwargs)
        return context
    
    def get_total(request):
        total = Notification.objects.count()
        return render(request, 'notifications.html', {'total_notifications':total})
    
    def mostrar_notifications(request):
        notis = Notification.objects.all()
        return render(request, 'notifications.html', {'personal_notis': notis})
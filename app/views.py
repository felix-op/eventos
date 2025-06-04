from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, DetailView,CreateView
from .models import Event, Notification, Ticket,User
from django.shortcuts import render
from django.db.models import Case, When
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.models import Group
from .models import PriorityLevel


class HomeView(TemplateView):
    template_name = "app/pages/home.html"

class NavView(TemplateView):
    template_name = "nav.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario_logueado'] = self.request.user.is_authenticated
        return context


class EventListView(ListView):
    model = Event
    template_name = "app/pages/events.html"
    context_object_name = "events"

    def get_queryset(self):
        return Event.objects.all().order_by("date")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class UserDashboard(LoginRequiredMixin,TemplateView):
    template_name = "app/pages/user_dashboard.html"

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
    template_name = "app/pages/notifications.html"
    context_object_name = "notifications"
    
    def get_queryset(self):
        return Notification.objects.all().order_by("created_at")
    
    def get_context_data(self, **kwargs):
        context = super(NotificationListView, self).get_context_data(**kwargs)
        return context
    
    def get_total(request):
        total = Notification.objects.count()
        return render(request, 'notifications.html', {'total_notifications':total})
    
def get_noti_preview_list(request):
    # Asignar valores de num de prioridad
    notis_preview = Notification.objects.annotate(
        priority_orden=Case(
            When(priority=PriorityLevel.HIGH, then=1),
            When(priority=PriorityLevel.MEDIUM, then=2),
            When(priority=PriorityLevel.LOW, then=3),
        )
    ).order_by('priority_orden', '-created_at')[:5]
    # Obtiene 5 notificaciones más recientes
    
    return render(request, 'app/components/notifications_preview.html', {'notis_preview': notis_preview})

# REGISTER
class RegistroForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class RegisterView(CreateView):
    form_class = RegistroForm
    template_name = 'app/pages/register.html'
    success_url = reverse_lazy('home')  

    def form_valid(self, form):
        # añado al usuairo a un grupo
        response = super().form_valid(form)
        user = self.object
        group = Group.objects.get(name='client')
        user.groups.add(group)
        user.save()
        # se logea
        login(self.request, self.object)
        return response
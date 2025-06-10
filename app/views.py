from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, DetailView,CreateView, FormView
from .models import Event, Notification, Ticket, User, Comment, PriorityLevel, RefundRequest, Notification_user
from django.shortcuts import render,redirect, get_object_or_404
from django.db.models import Case, When
from django.contrib.auth.forms import UserCreationForm
from django.views import View
from django.urls import reverse_lazy,reverse
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import Group
from .forms import LoginForm, CommentForm,RefundRequestForm
from django.contrib import messages
from django.http import HttpResponseRedirect


class HomeView(TemplateView):
    template_name = "app/pages/home.html"

class NavView(TemplateView):
    template_name = "nav.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['usuario_logueado'] = user.is_authenticated
        
        if user.is_authenticated:
            notis_preview = Notification_user.objects.filter(
                user=user
            ).select_related('notification').annotate(
                priority_orden=Case(
                    When(notification__priority=PriorityLevel.HIGH, then=1),
                    When(notification__priority=PriorityLevel.MEDIUM, then=2),
                    When(notification__priority=PriorityLevel.LOW, then=3),
                )
            ).order_by('priority_orden', '-notification__created_at')[:5]
        else:
            notis_preview = []
        
        context['notis_preview'] = notis_preview
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
    template_name = "app/components/user_dashboard.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tickets'] = Ticket.objects.filter(user=self.request.user)
        context['comments'] = Comment.objects.filter(user=self.request.user)
        context['refundChoices'] = RefundRequest.REASON_CHOICES
        context['refunds'] = RefundRequest.objects.filter(usuario=self.request.user)
        return context

class EventDetailView(DetailView):
    model = Event
    template_name = "app/pages/event_detail.html"
    context_object_name = "event"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        context['event'] = Event.objects.get(pk=pk)
        context['comments'] = Comment.objects.filter(event= context['event'])
        
        if self.request.user.is_authenticated:
            from .models.ticket import TicketState
            ticket = Ticket.objects.filter(
                user=self.request.user, 
                event=context['event'],
                state__in=[TicketState.VALID, TicketState.EXPIRED]
            )
            context['userPurchase'] = ticket.exists()
        else:
            context['userPurchase'] = False



        
        return context

# NOTIFICATIONS
class NotificationDetailView(LoginRequiredMixin, DetailView):
    model = Notification_user
    template_name = "app/pages/notification_detail.html"
    context_object_name = "notif"

    def get_object(self):
        notif_user = get_object_or_404(
            Notification_user.objects.select_related('notification'),
            id=self.kwargs['pk'],
            user=self.request.user
        )
        # Marcar como leída si aún no lo está
        if not notif_user.is_read:
            notif_user.mark_as_read()
        return notif_user
    
#class MarkNotificationReadView(LoginRequiredMixin, View):
#    def post(self, request, pk):
#        notif_user = get_object_or_404(Notification_user, pk=pk, user=request.user)
#        notif_user.mark_as_read()
#        return HttpResponseRedirect(reverse("notification_detail", args=[pk]))

class NotificationListView(LoginRequiredMixin, ListView):
    template_name = "app/pages/notifications.html"
    context_object_name = "notifications"

    def get_queryset(self):
        # Retorna la relación usuario-notificación
        return Notification_user.objects.filter(
            user=self.request.user
        ).select_related('notification').order_by(
            'is_read', '-notification__created_at'
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_unread'] = Notification_user.objects.filter(
            user=self.request.user,
            is_read=False
        ).count()
        return context


# REGISTER
class RegistroForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    # el metodo, añade clases de boostrap
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class RegisterView(CreateView):
    form_class = RegistroForm
    template_name = 'app/pages/register.html'
    success_url = reverse_lazy('home')  

    def form_valid(self, form):
        # añado al usuario a un grupo
        response = super().form_valid(form)
        user = self.object
        group = Group.objects.get(name='client')
        user.groups.add(group)
        user.save()
        # se logea
        login(self.request, self.object)
        return response
    
class LoginManualView(FormView):
    template_name = 'app/pages/login.html'
    form_class = LoginForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        login(self.request, form.user)
        messages.success(self.request, f"Bienvenido, {form.cleaned_data['usuario']}!")
        return super().form_valid(form)
    
#   COMMENT CLASSES

class CommentUpdateView(View):
    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk, user=request.user)
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
        messages.success(request, "Comentario actualizado correctamente.")
        return redirect(request.META.get('HTTP_REFERER', 'user_dashboard'))
        #Devuelvo al link anterior o al user dashboard

class CommentDeleteView(View):
    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk, user=request.user)
        comment.delete()
        messages.success(request, "Comentario eliminado correctamente.")
        return redirect(request.META.get('HTTP_REFERER', 'user_dashboard'))

class CommentCreateView(View):
    def post(self, request, event_id):
        event = get_object_or_404(Event, pk=event_id)
        form = CommentForm(request.POST)
        if form.is_valid():
            Comment.objects.create(
                user=request.user,
                event=event,
                title=form.cleaned_data['title'],
                text=form.cleaned_data['text']
            )
        messages.success(request, "Comentario creado correctamente.")
        return redirect(request.META.get('HTTP_REFERER', 'user_dashboard'))


# RefundRequest CLASSES
class RefundRequestCreateView(View):
    def post(self, request, ticket_id):
        ticket = get_object_or_404(Ticket, pk=ticket_id)
        form = RefundRequestForm(request.POST)
        if form.is_valid():
            RefundRequest.objects.create(
                usuario=request.user,
                ticket_code=ticket,
                reason=form.cleaned_data['reason'],
                reason_detail=form.cleaned_data['reason_detail']
            )
        messages.success(request, "Solicitud enviada correctamente.")
        return redirect('user_dashboard')  
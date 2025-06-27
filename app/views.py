from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, DetailView,CreateView, FormView, DeleteView, UpdateView
from .models import Event, Ticket, User, Comment, PriorityLevel, RefundRequest, Notification_user, Category, TicketState, Rating
from django.shortcuts import render,redirect, get_object_or_404
from django.db.models import Case, When
from django.contrib.auth.forms import UserCreationForm
from django.views import View
from django.urls import reverse_lazy,reverse
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import Group
from .forms import LoginForm, CommentForm, RefundRequestForm, TicketPurchaseForm, RatingForm
from django.contrib import messages
from django.http import Http404
from django.utils import timezone

class AccessDeniedView(TemplateView):
    template_name = "app/pages/access_denied.html"

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
        user = self.request.user
        category_filter = self.request.GET.get('category', '')
        search_filter = self.request.GET.get('search', '')
        # Filtrar eventos según la autenticación del usuario y tipo
        if user.is_staff:
            events = Event.objects.all()  # Mostrar todos los eventos
        else:
            events = Event.objects.filter(date__gt=timezone.now())  # Mostrar solo eventos futuros
        # Aplicar filtro por categoría si se seleccionó alguna
        if category_filter:
            events = events.filter(categories__id=category_filter)
        # Filtro por titulo y ciudad 
        if search_filter:
            events = events.filter(title__icontains=search_filter) | events.filter(venue__city__icontains=search_filter)


        return events.order_by("date")  # Ordenar por fecha

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        events = context['events']

        for event in events:
            promedio = event.average_rating
            rating = int(promedio % 5) if promedio else 0
            event.starts_marked = range(rating)
            event.starts_unmarked = range(5 - rating)
            print(event.starts_marked)
            print(event.starts_unmarked)

        
        context['categories'] = Category.objects.all()  # Pasar las categorías al template
        return context

class UserDashboard(LoginRequiredMixin,TemplateView):
    login_url = 'access-denied'
    template_name = "app/components/user_dashboard.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tickets'] = Ticket.objects.filter(user=self.request.user)
        context['comments'] = Comment.objects.filter(user=self.request.user)
        context['refundChoices'] = RefundRequest.REASON_CHOICES
        context['refunds'] = RefundRequest.objects.filter(usuario=self.request.user)
        context["now"] = timezone.now()
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

    def post(self, request):
        notification_user_id = request.POST.get('notification_user_id')
        notification_to_mark = get_object_or_404(
            Notification_user, 
            id=notification_user_id, 
            user=self.request.user
        )
        if notification_to_mark:
            notification_to_mark.is_read = True
            notification_to_mark.save()

        return redirect('notifications')

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

class CommentUpdateView(LoginRequiredMixin,View):
    login_url = 'access-denied'

    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk, user=request.user)
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
        messages.success(request, "Comentario actualizado correctamente.")
        return redirect(request.META.get('HTTP_REFERER', 'user_dashboard'))
        #Devuelvo al link anterior o al user dashboard

class CommentDeleteView(LoginRequiredMixin,View):
    login_url = 'access-denied'

    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk, user=request.user)
        comment.delete()
        messages.success(request, "Comentario eliminado correctamente.")
        return redirect(request.META.get('HTTP_REFERER', 'user_dashboard'))

class CommentCreateView(LoginRequiredMixin,View):
    login_url = 'access-denied'

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
class RefundRequestCreateView(LoginRequiredMixin,View):
    login_url = 'access-denied'
    
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

# Compra de Tickets 
class EventPurchaseView(LoginRequiredMixin, View):
    login_url = 'access-denied'
    form_class = TicketPurchaseForm
    template_name = 'app/pages/ticket_purchase.html'

    def get(self, request, **kwargs):
        """Muestra el formulario de compra."""
        event = get_object_or_404(Event, pk=kwargs.get('pk'))
        form = self.form_class()
        context = {'event': event, 'form': form}
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        """Procesa el formulario de compra."""
        event = get_object_or_404(Event, pk=kwargs.get('pk'))
        form = self.form_class(request.POST)

        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            ticket_type = int(form.cleaned_data['ticket_type'])
            
            # GENERACIÓN DE CODIGO Y CREACIÓN DEL TICKET
            import uuid
            ticket_code = f"EVT{event.pk}-{uuid.uuid4().hex[:8].upper()}"

            Ticket.objects.create(
                user=request.user,
                event=event,
                quantity=quantity,
                type=ticket_type,
                state=TicketState.VALID,
                ticket_code=ticket_code
            )

            messages.success(request, f"¡Has comprado {quantity} ticket(s) para '{event.title}' exitosamente!")
            return redirect('user_dashboard')

        messages.error(request, "Por favor, corrige los errores en el formulario.")
        context = {'event': event, 'form': form}
        return render(request, self.template_name, context)
    
class RatingCreateView(LoginRequiredMixin, CreateView):
    model = Rating
    form_class = RatingForm
    template_name = 'app/pages/rating_create.html'
    success_url = reverse_lazy('user_dashboard')

    def dispatch(self, request, *args, **kwargs):
        self.event = Event.objects.filter(pk=self.kwargs['event_id']).first()
        if self.event is None:
            raise Http404("El evento no existe.")

        # Comprueba si el usuario tiene un ticket expirado para este evento.
        has_permission = Ticket.objects.filter(
            user=request.user, 
            event=self.event, 
            state=TicketState.EXPIRED
        ).exists()

        already_rated = Rating.objects.filter(user=request.user, event=self.event).exists()

        if not has_permission or already_rated:
            raise Http404("No tienes permiso para calificar este evento.")
        
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event'] = self.event
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.event = self.event
        return super().form_valid(form)
    
class RatingDeleteView(LoginRequiredMixin, DeleteView):
    model = Rating
    template_name = 'app/pages/rating_delete.html' 
    success_url = reverse_lazy('user_dashboard') 

    def get_queryset(self):
        return Rating.objects.filter(user=self.request.user)

class RatingUpdateView(LoginRequiredMixin, UpdateView):
    model = Rating
    form_class = RatingForm
    template_name = 'app/pages/rating_create.html' 
    success_url = reverse_lazy('user_dashboard') 

    def get_queryset(self):
        return Rating.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event'] = self.object.event
        return context
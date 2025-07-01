from django.contrib import admin
from .models import Category, Comment, Event, Notification, Rating, RefundRequest, Ticket, User, Venue, Notification_user
from django import forms
from django.contrib import messages
from django.core.management import call_command
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin 

User = get_user_model()
class HiddenFromSellerAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return not request.user.groups.filter(name='seller').exists()
 
class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "email", "groups")  

class CustomUserAdmin(HiddenFromSellerAdmin,UserAdmin):
    add_form = CustomUserCreationForm
    model = User
    list_display = ("username", "date_joined", "is_active", "is_staff", "is_superuser")
    search_fields = ("username", )
    list_filter = ("date_joined", "is_active", "is_staff", "is_superuser")
    add_fieldsets = (
        (None, {
            'fields': ('username', 'email', 'groups'),
        }),
    )
    def save_model(self, request, obj, form, change):
        if not change:
            obj.set_password('123456')
        super().save_model(request, obj, form, change)
   
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = "__all__"
        widgets = {
            "categories": forms.CheckboxSelectMultiple
        }

class EventAdmin(admin.ModelAdmin):
    form = EventForm
    exclude = ['_tickets_updated'] # solo lo modifica el comando tickets_expirados
    list_display = ("title", "description", "date")
    search_fields = ("title", "date")
    list_filter = ("date",)

    def has_view_permission(self, request, obj=None):
        return True  

    def has_change_permission(self, request, obj=None):
        return True  

    def has_add_permission(self, request):
        return not request.user.groups.filter(name='seller').exists()

    def has_delete_permission(self, request, obj=None):
        return not request.user.groups.filter(name='seller').exists()

    def has_module_permission(self, request):
        return True

class CommentAdmin(admin.ModelAdmin):
    list_display = ("title", "create_at")
    search_fields = ("title", )
    list_filter = ("create_at",)

    def has_module_permission(self, request):
        return True

    def has_view_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request):
        return not request.user.groups.filter(name='seller').exists()

    def has_change_permission(self, request, obj=None):
        return not request.user.groups.filter(name='seller').exists()

    def has_delete_permission(self, request, obj=None):
        return True  

class RefundRequestAdmin(admin.ModelAdmin):
    list_display = ("usuario", "ticket_code", "reason", "approved", "approval_date", "reason_detail")
    search_fields = ("reason", )
    list_filter = ("approved", "approval_date")

    def has_module_permission(self, request):
        return True

    def has_view_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True  

    def has_add_permission(self, request):
        return not request.user.groups.filter(name='seller').exists()

    def has_delete_permission(self, request, obj=None):
        return not request.user.groups.filter(name='seller').exists()

class CategoryAdmin(HiddenFromSellerAdmin):
    list_display = ("name", "is_active")
    search_fields = ("name",)
    list_filter = ("is_active",)

class NotificationAdmin(HiddenFromSellerAdmin):
    list_display = ("title", "priority", "created_at")
    list_filter = ("priority", "recipients", "created_at")

class RatingAdmin(HiddenFromSellerAdmin):
    pass

def actualizar_tickets_expirados(modeladmin, request,queryset):
    call_command('tickets_expirados')
    modeladmin.message_user(request, "Tickets expirados actualizados correctamente.")

class TicketAdmin(HiddenFromSellerAdmin):
    list_display = ("user", "event", "buy_date", "quantity","type", "state", "ticket_code")
    actions = [actualizar_tickets_expirados]

class VenueAdmin(HiddenFromSellerAdmin):
    list_display = ("name", "address", "city", "capacity", "contact")
    search_fields = ("name", "address", "city", "contact")

class Notification_userAdmin(HiddenFromSellerAdmin):
    list_display = ("user", "notification", "is_read")
    list_filter = ("is_read", "read_at")

admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(RefundRequest, RefundRequestAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Venue, VenueAdmin)
admin.site.register(Notification_user, Notification_userAdmin)
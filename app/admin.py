from django.contrib import admin
from .models import Category, Comment, Event, Notification, Rating, RefundRequest, Ticket, User, Venue, Notification_user
from django import forms

class HiddenFromSellerAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return not request.user.groups.filter(name='seller').exists()

    def has_view_permission(self, request, obj=None):
        return not request.user.groups.filter(name='seller').exists()

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = "__all__"
        widgets = {
            "categories": forms.CheckboxSelectMultiple
        }

class EventAdmin(admin.ModelAdmin):
    form = EventForm
    list_display = ("title", "description", "date")
    search_fields = ("title", "date")
    list_filter = ("date",)

    def has_view_permission(self, request, obj=None):
        return True  # Todos pueden ver

    def has_change_permission(self, request, obj=None):
        return True  # Todos pueden modificar (opcional, podés restringir)

    def has_add_permission(self, request):
        return not request.user.groups.filter(name='seller').exists()

    def has_delete_permission(self, request, obj=None):
        return not request.user.groups.filter(name='seller').exists()

    def has_module_permission(self, request):
        return True

class CommentAdmin(admin.ModelAdmin):
    #list_display = ('user', 'event', 'created_at')

    def has_module_permission(self, request):
        return True

    def has_view_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request):
        return not request.user.groups.filter(name='seller').exists()

    def has_change_permission(self, request, obj=None):
        return not request.user.groups.filter(name='seller').exists()

    def has_delete_permission(self, request, obj=None):
        return True  # sellers pueden eliminar

class RefundRequestAdmin(admin.ModelAdmin):
    #list_display = ('user', 'ticket', 'status')

    def has_module_permission(self, request):
        return True

    def has_view_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True  # sellers pueden modificar

    def has_add_permission(self, request):
        return not request.user.groups.filter(name='seller').exists()

    def has_delete_permission(self, request, obj=None):
        return not request.user.groups.filter(name='seller').exists()

class CategoryAdmin(HiddenFromSellerAdmin):
    pass
class NotificationAdmin(HiddenFromSellerAdmin):
    pass
class RatingAdmin(HiddenFromSellerAdmin):
    pass
class TicketAdmin(HiddenFromSellerAdmin):
    pass
class UserAdmin(HiddenFromSellerAdmin):
    pass
class VenueAdmin(HiddenFromSellerAdmin):
    pass
class Notification_userAdmin(HiddenFromSellerAdmin):
    pass
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(RefundRequest, RefundRequestAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Venue, VenueAdmin)
admin.site.register(Notification_user, Notification_userAdmin)
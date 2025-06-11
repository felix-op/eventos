from django.contrib import admin
from .models import Category, Comment, Event, Notification, Rating, RefundRequest, Ticket, User, Venue, Notification_user
from django import forms


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


admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Event, EventAdmin)
admin.site.register(Notification)
admin.site.register(Rating)
admin.site.register(RefundRequest)
admin.site.register(Ticket)
admin.site.register(User)
admin.site.register(Venue)
admin.site.register(Notification_user)
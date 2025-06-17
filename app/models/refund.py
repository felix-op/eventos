from django.db import models
from .ticket import TicketState
from django.utils import timezone
# =======================
# Model: RefundRequest
# Description: User request for ticket refund with approval status and reason.
# =======================
class RefundRequest(models.Model):

    REASON_CHOICES = [
        ('event_cancelled', 'El evento fue cancelado'),
        ('could_not_attend', 'No pude asistir'),
        ('payment_error', 'Error en el pago'),
        ('other', 'Otro'),
    ]

    approved = models.BooleanField(default=False)
    approval_date = models.DateField(null=True, blank=True)
    reason = models.CharField(max_length=50, choices=REASON_CHOICES,blank=False)
    reason_detail = models.CharField(max_length=1000,  blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey("User", on_delete=models.CASCADE)
    ticket_code = models.ForeignKey("Ticket", on_delete=models.CASCADE, related_name='ticket_refund', blank = False)


    def __str__(self):
        return f"{self.ticket_code.ticket_code} - {self.usuario.username} - Approved: {self.approved}"

    # Modifico el save, por si cambia el estado Approved, desde panel admin
    def save(self, *args, **kwargs):
        if self.approved:
            self.ticket_code.state = TicketState.REFUNDED
            self.ticket_code.save()
            self.approval_date = timezone.now().date()
        super().save(*args, **kwargs)

    def update(self, approved, reason, approval_date,reason_detail):
        self.approved = approved or self.approved
        if approved:
            from .ticket import TicketState
            self.ticket_code.state = TicketState.REFUNDED
            self.ticket_code.save()
            self.approval_date = timezone.now().date()
        self.reason = reason or self.reason
        self.approval_date = approval_date or self.approval_date
        self.reason_detail = reason_detail or self.reason_detail
        self.save()
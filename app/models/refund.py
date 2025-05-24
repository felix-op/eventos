from django.db import models

# =======================
# Model: RefundRequest
# Description: User request for ticket refund with approval status and reason.
# =======================
class RefundRequest(models.Model):
    approved = models.BooleanField(default=False)
    approval_date = models.DateField(null=True, blank=True)
    ticket_code = models.CharField(max_length=100, blank=False)
    reason = models.CharField(max_length=1000, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey("User", on_delete=models.CASCADE)

    def __str__(self):
        return self.ticket_code

    def update(self, approved=None, reason=None, approval_date=None):
        if approved is not None:
            self.approved = approved
        if reason is not None:
            self.reason = reason
        if approval_date is not None:
            self.approval_date = approval_date
        self.save()
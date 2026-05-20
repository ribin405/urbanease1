from django.db import models


class VisitorRequest(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    visitor_name = models.CharField(max_length=100)

    phone_number = models.CharField(max_length=15)

    purpose = models.TextField()

    visit_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.visitor_name

from django.db import models

from django.db import models


class Patient(models.Model):
    identification = models.CharField(
        max_length=30,
        unique=True
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Treatment(models.Model):

    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    patient = models.ForeignKey(
        Patient,
        on_delete=models.PROTECT,
        related_name="treatments"
    )
    name = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(
        null=True,
        blank=True
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
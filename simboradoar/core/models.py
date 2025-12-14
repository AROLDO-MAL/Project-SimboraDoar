from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class User(AbstractUser):
    cpf = models.CharField(max_length=14, unique=True, verbose_name="CPF")
    phone = models.CharField(max_length=15, verbose_name="Telefone")

    def __str__(self):
        return self.username

class Donation(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pendente'),
        ('PAID', 'Pago / Confirmado'),
        ('DELIVERING', 'Em Entrega'),
        ('COMPLETED', 'Entregue'),
    ]

    TYPE_CHOICES = [
        ('PREMADE', 'Cesta Pronta'),
        ('CUSTOM', 'Cesta Customizada'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='donations')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    items = models.JSONField(default=list, verbose_name="Itens da Cesta")
    total_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Doação {self.id} - {self.user.username}"

class Tracking(models.Model):
    donation = models.OneToOneField(Donation, on_delete=models.CASCADE, related_name='tracking')
    latitude = models.FloatField()
    longitude = models.FloatField()
    current_status = models.CharField(max_length=100, default="Aguardando início")
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Rastreio {self.donation.id}"

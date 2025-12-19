from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class User(AbstractUser):
    cpf = models.CharField(max_length=14, unique=True, verbose_name="CPF")
    phone = models.CharField(max_length=15, verbose_name="Telefone")

    REQUIRED_FIELDS = ['email', 'cpf', 'phone']

    def __str__(self):
        return self.username

class Community(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nome da Comunidade")
    description = models.TextField(verbose_name="Descrição")
    latitude = models.FloatField(verbose_name="Latitude")
    longitude = models.FloatField(verbose_name="Longitude")
    photo_filename = models.CharField(
        max_length=255, 
        null=True, 
        blank=True, 
        verbose_name="Nome do Arquivo da Foto",
        help_text="Digite o nome exato do arquivo localizado em 'static/img/communities/' (ex: 'Vila Pedra Mansa (Patu - RN).jpg')."
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Comunidade"
        verbose_name_plural = "Comunidades"

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
    community = models.ForeignKey(Community, on_delete=models.SET_NULL, null=True, blank=True, related_name='donations', verbose_name="Comunidade Destino")
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    items = models.JSONField(default=list, verbose_name="Itens da Cesta")
    total_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Doação"
        verbose_name_plural = "Doações"

    def __str__(self):
        return f"Doação {self.id} - {self.user.username}"

class Tracking(models.Model):
    donation = models.OneToOneField(Donation, on_delete=models.CASCADE, related_name='tracking')
    latitude = models.FloatField()
    longitude = models.FloatField()
    current_status = models.CharField(max_length=100, default="Aguardando início")
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Rastreio"
        verbose_name_plural = "Rastreios"

    def __str__(self):
        return f"Rastreio {self.donation.id}"

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(verbose_name="Depoimento")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Depoimento"
        verbose_name_plural = "Depoimentos"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.created_at.strftime('%d/%m/%Y')}"

# models.py
from django.db import models
from django.conf import settings
from django.utils import timezone
from apps.orders.models import Order

User = settings.AUTH_USER_MODEL


class CourierProfile(models.Model):
    """Courier profili - ro'yxatdan o'tgandan keyin yaratiladi"""
    TRANSPORT_TYPES = (
        ('bike', 'Velosiped'),
        ('moped', 'Moped'),
        ('car', 'Mashina'),
        ('foot', 'Piyoda'),
    )

    STATUS_CHOICES = (
        ('pending', 'Kutilmoqda'),
        ('approved', 'Tasdiqlangan'),
        ('rejected', 'Rad etilgan'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="courier_profile")
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    passport_number = models.CharField(max_length=30, unique=True)
    passport_photo = models.ImageField(upload_to='courier_documents/', null=True, blank=True)
    transport_type = models.CharField(max_length=10, choices=TRANSPORT_TYPES)
    transport_number = models.CharField(max_length=20, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_active = models.BooleanField(default=False)
    is_online = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Courier: {self.full_name}"

    def total_deliveries(self):
        """Jami yetkazib berilgan buyurtmalar soni"""
        return self.deliveries.filter(status='delivered').count()

    def completed_today(self):
        """Bugun yetkazib berilgan buyurtmalar"""
        today = timezone.now().date()
        return self.deliveries.filter(
            status='delivered',
            delivered_at__date=today
        ).count()


class Delivery(models.Model):
    """Yetkazib berish ma'lumotlari"""
    STATUS_CHOICES = (
        ('pending', 'Kutilmoqda'),
        ('assigned', 'Courier tayinlangan'),
        ('picked_up', 'Olib ketilgan'),
        ('on_the_way', 'Yo\'lda'),
        ('delivered', 'Yetkazib berilgan'),
        ('cancelled', 'Bekor qilingan'),
    )

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="delivery")
    courier = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="deliveries"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    delivery_address = models.TextField()
    delivery_notes = models.TextField(blank=True, null=True)

    # Coordinates uchun
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    # Vaqt ma'lumotlari
    created_at = models.DateTimeField(auto_now_add=True)
    assigned_at = models.DateTimeField(null=True, blank=True)
    picked_up_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    # Qo'shimcha
    customer_phone = models.CharField(max_length=20)
    estimated_delivery_time = models.DateTimeField(null=True, blank=True)
    actual_delivery_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Yetkazib berish'
        verbose_name_plural = 'Yetkazib berishlar'

    def __str__(self):
        return f"Delivery #{self.id} - Order #{self.order.id}"

    def save(self, *args, **kwargs):
        # Status o'zgarganda vaqtlarni avtomatik yangilash
        if self.status == 'assigned' and not self.assigned_at:
            self.assigned_at = timezone.now()
        if self.status == 'picked_up' and not self.picked_up_at:
            self.picked_up_at = timezone.now()
        if self.status == 'delivered' and not self.delivered_at:
            self.delivered_at = timezone.now()
            self.actual_delivery_time = timezone.now()

        super().save(*args, **kwargs)


class DeliveryHistory(models.Model):
    """Yetkazib berish tarixi - har bir status o'zgarishi saqlanadi"""
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE, related_name='history')
    status = models.CharField(max_length=20)
    note = models.TextField(blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Yetkazish tarixi'
        verbose_name_plural = 'Yetkazish tarixi'

    def __str__(self):
        return f"{self.delivery.id} - {self.status} - {self.created_at}"
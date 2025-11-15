from django.db import models

class MenuItem(models.Model):
    MEASUREMENT_CHOICES = [
        ('GR', 'Gram'),
        ('ML', 'Milliliter'),
        ('PC', 'Piece')
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    measurement_type = models.CharField(max_length=2, choices=MEASUREMENT_CHOICES)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Menu Item'
        verbose_name_plural = 'Menu Items'

    def __str__(self):
        return self.title

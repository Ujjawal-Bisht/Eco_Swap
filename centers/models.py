from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator

class Center(models.Model):
    name = models.CharField(max_length=200, blank=False)
    address = models.TextField(blank=False)
    city = models.CharField(max_length=100, blank=False)
    contact_number = models.CharField(
    max_length=15,
    blank=True,  
    null=True,  
    validators=[RegexValidator(r'^\d{10}$', 'Contact number must be 10 digits')]
)
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        validators=[MinValueValidator(-90), MaxValueValidator(90)]
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        validators=[MinValueValidator(-180), MaxValueValidator(180)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['city', 'name']

    def __str__(self):
        return f"{self.name} ({self.city})"
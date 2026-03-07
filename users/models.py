from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('individual', 'Individual'),
        ('ngo', 'NGO Partner'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='individual')
    location = models.CharField(max_length=255, blank=True)
    sustainability_interests = models.TextField(blank=True)
    
    profile_image = models.ImageField(
        upload_to='profile_pics/', 
        default='profile_pics/default.jpg', 
        blank=True, 
        null=True
    )

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
from django.db import models
from django.conf import settings

class Item(models.Model):
    CATEGORY_CHOICES = [
        ('electronics', '📱 Electronics & Tech'),
        ('fashion', '👕 Fashion & Accessories'),
        ('home', '🏠 Home & Furniture'),
        ('fitness', '🏋️ Fitness & Sports'),
        ('books', '📚 Books & Media'),
        ('toys', '🎮 Toys & Games'),  
        ('other', '✨ Other Items'),
    ]

    LOCATION_CHOICES = [
        ('north', 'North Delhi'),
        ('south', 'South Delhi'),
        ('east', 'East Delhi'),
        ('west', 'West Delhi'),
        ('central', 'Central Delhi'),
        ('ne', 'North-East Delhi'),
        ('nw', 'North-West Delhi'),
        ('se', 'South-East Delhi'),
        ('sw', 'South-West Delhi'),
    ]

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    location = models.CharField(max_length=20, choices=LOCATION_CHOICES, default='central')
    address = models.CharField(max_length=255, blank=True, help_text="Specific area/street (optional)")
    created_at = models.DateTimeField(auto_now_add=True)
    is_swapped = models.BooleanField(default=False) 
    image = models.ImageField(upload_to='item_images/', blank=True, null=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['category', 'location']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return self.title

class SwapRequest(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='requests')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, default='pending') 
    created_at = models.DateTimeField(auto_now_add=True)
    meeting_center = models.ForeignKey('centers.Center', on_delete=models.SET_NULL, null=True, blank=True)
    
    owner_agreed_location = models.BooleanField(default=False)
    sender_agreed_location = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender.username} wants {self.item.title}"
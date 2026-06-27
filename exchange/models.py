# pyrefly: ignore [missing-import]
from django.db import models
# pyrefly: ignore [missing-import]
from django.conf import settings
# pyrefly: ignore [missing-import]
from django.core.exceptions import ValidationError


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

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='items'
    )
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
            models.Index(fields=['is_swapped']),
        ]

    def __str__(self):
        return self.title


class SwapRequest(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_ACCEPTED = 'accepted'
    STATUS_REJECTED = 'rejected'
    STATUS_COMPLETED = 'completed'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_ACCEPTED, 'Accepted'),
        (STATUS_REJECTED, 'Rejected'),
        (STATUS_COMPLETED, 'Completed'),
    ]

    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='requests')
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='swap_requests_sent'
    )
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    meeting_center = models.ForeignKey(
        'centers.Center', on_delete=models.SET_NULL, null=True, blank=True
    )

    owner_agreed_location = models.BooleanField(default=False)
    sender_agreed_location = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['-created_at']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['item', 'sender'],
                condition=models.Q(status='pending'),
                name='unique_pending_swap_request_per_item_sender'
            )
        ]

    def clean(self):
        if self.sender_id and self.item_id and self.sender_id == self.item.owner_id:
            raise ValidationError("You can't request to swap your own item.")

    def __str__(self):
        return f"{self.sender.username} wants {self.item.title}"
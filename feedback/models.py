from django.db import models

# Create your models here.

class CustomerFeedback(models.Model):
    PLATFORM_CHOICES = [
        ('twitter', 'Twitter'),
        ('instagram', 'Instagram'),
        ('facebook', 'Facebook'),
        ('manual', 'Manual Entry'),
    ]

    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    message = models.TextField()
    username = models.CharField(max_length=100)
    sentiment = models.CharField(max_length=10, blank=True, null=True)  # To be filled later
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.platform} - {self.message[:50]}"
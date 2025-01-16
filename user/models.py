import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    profile_picture = models.URLField(blank=True, null=True)
    coupon_code = models.CharField(max_length=8, unique=True, blank=True, null=True)
    coupon_used = models.BooleanField(default=False)

    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        if not self.coupon_code:
            self.coupon_code = str(uuid.uuid4()).replace("-", "")[:8].upper()
        super().save(*args, **kwargs)
    

class Visit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="visits")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.timestamp}"
from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveIntegerField()
    handedness = models.CharField(max_length=10, choices=[('left', 'Left'), ('right', 'Right')])
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    unique_id = models.CharField(max_length=120, unique=True)

class FilledForm(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    form_id = models.CharField(max_length=32)
    txt_path = models.CharField(max_length=255)
    assigned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"User: {self.user.username}, Form: {self.form_id}"

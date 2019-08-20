from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Income(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField(default=timezone.now)
    user = models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    rupees = models.FloatField(null=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title
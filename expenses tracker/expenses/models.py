from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from category.models import Category

# Create your models here.
class Expenses(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField(default=timezone.now)
    bill = models.FileField(upload_to='bill/',blank=True,null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    rupees = models.FloatField(null=True)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    def __str__(self):
        return self.title
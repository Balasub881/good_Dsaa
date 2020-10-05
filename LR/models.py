from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name

class Expense(models.Model):
    title = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    amount = models.FloatField()
    description = models.TextField()

    def __str__(self):
        return self.title
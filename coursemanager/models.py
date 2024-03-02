from django.db import models
from django.conf import settings


# Create your models here.
class Product(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    min_students = models.IntegerField(default=0)
    max_students = models.IntegerField(default=8)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    title = models.CharField(max_length=255)
    video_url = models.URLField(null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="lessons")

    def __str__(self):
        return self.title


class Group(models.Model):
    title = models.CharField(max_length=255)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="groups_product")
    students = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="students_in_group", blank=True)

    def __str__(self):
        return self.title


class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.product.title}"

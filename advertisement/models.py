from django.contrib.auth.models import User
from django.db import models

import posixpath
from uuid import uuid4


def main_pictures_path(_instance, filename):
    _, ext = posixpath.splitext(filename)
    safe_name = str(uuid4())
    return posixpath.join("main_pictures", "{}{}".format(safe_name, ext))


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.title


class Advertisement(models.Model):
    STATUS_CHOICES = (
        (1, "ACTIVE"),
        (2, "RESOLVED"),
        (3, "SOLD"),
    )

    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="advertisements")
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=19)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    main_picture = models.ImageField(upload_to=main_pictures_path)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="advertisements")

    def __str__(self):
        return f"{self.title} - ${self.price}"
class Report(models.Model):
    id = models.AutoField(primary_key=True)
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, related_name="reports")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reports")
    reason = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report by {self.user} on Ad {self.advertisement.id}"

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

import posixpath
from uuid import uuid4

from file.views import main_pictures_path, pictures_path


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.title

class Advertisement(models.Model):
    class Meta:
        verbose_name = _("advertisement")
        verbose_name_plural = _("advertisements")

    STATUS_CHOICES = (
        (1, "ACTIVE"),
        (2, "RESOLVED"),
        (3, "SOLD"),
    )

    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="advertisements")
    title = models.CharField(max_length=200, verbose_name=_("title"))
    description = models.TextField(blank=False, verbose_name=_("description"))
    price = models.DecimalField(decimal_places=2, max_digits=19, verbose_name=_("price"))
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name=_("status"))
    main_picture = models.ImageField(upload_to=main_pictures_path)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="advertisements", verbose_name=_("category"))

    def __str__(self):
        return f"{self.title} - {self.price}T"


class Report(models.Model):
    id = models.AutoField(primary_key=True)
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, related_name="reports")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reports")
    reason = models.TextField(blank=False, verbose_name=_("reason"))
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report by {self.user} on Ad {self.advertisement.id}"


class Picture(models.Model):
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, related_name="pictures")
    picture = models.ImageField(upload_to=pictures_path)
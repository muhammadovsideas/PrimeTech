from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser


# ------------------ Custom User (Admin & Manager) ------------------
class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", _("Admin")
        MANAGER = "MANAGER", _("Manager")

    role = models.CharField(max_length=20, choices=Role.choices)
    phone_number = models.CharField(_("Phone number"), max_length=13, unique=True, null=True, blank=True)
    description = models.TextField(_("Description"), null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} - {self.last_name} ({self.role})"

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")


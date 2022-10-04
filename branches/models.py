from django.db import models
from django.utils.translation import gettext_lazy as _

from django.utils import timezone


class Branch(models.Model):
    address = models.CharField(_("Адрес"), max_length=255)
    phone = models.CharField(_("Номер телефона"), max_length=255)
    picture = models.ImageField(_("Фото"), upload_to="media", blank=True)
    open_from = models.TimeField(_("Открыто с"), default=timezone.now)
    closed_from = models.TimeField(_("Закрыто с"), default=timezone.now)

    def __str__(self):
        return f"{self.address}"


class AboutUs(models.Model):
    name = models.CharField(_("Заголовок"), max_length=255)
    description = models.TextField(_("Описание"))
    picture = models.ImageField(_("Фото"), upload_to="Media", blank=True)

    def __str__(self):
        return f"{self.branches}"

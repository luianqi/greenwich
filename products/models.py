from django.db import models
from django.utils.translation import gettext_lazy as _

from users.models import Employee, Client


class Category(models.Model):
    name = models.CharField(_("Название"), max_length=255)
    picture = models.ImageField(_("Фото"), upload_to="Media", blank=True)

    def __str__(self):
        return f"{self.name}"


class ProductBase(models.Model):
    name = models.CharField(_("Название"), max_length=255)
    picture = models.ImageField(_("Фото"), upload_to="Media", blank=True)
    price = models.IntegerField(_("Цена"))
    quantity = models.IntegerField(_("Количество"))

    class Meta:
        abstract = True


class Product(ProductBase):
    florist = models.ForeignKey(Employee, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    watering = models.CharField(_("Полив"), max_length=255)
    temperature = models.CharField(_("Температура"), max_length=255)
    sun = models.CharField(_("Освещение"), max_length=255)
    total_sales = models.IntegerField(_("Общий объем продаж"), default=0)
    is_sold = models.BooleanField(_("Продано"), default=False)
    is_easy = models.BooleanField(_("Легко ухаживать"), default=False)
    discount = models.IntegerField(_("Скидка"), default=0)
    date_created = models.DateTimeField(_("Дата создания"), auto_now_add=True)

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        if self.quantity == 0:
            self.is_sold = True
        else:
            self.is_sold = False
        super().save(*args, **kwargs)


class PlantCare(ProductBase):
    FERTILIZER = "Удобрения"
    PROTECTION = "Средства защиты"
    PEAT = "Грунт"
    SOIL = "Почва"

    PLANT_CARE_CHOICES = (
        (FERTILIZER, "Удобрения"),
        (PROTECTION, "Средства защиты"),
        (PEAT, "Грунт"),
        (SOIL, "Почва"),
    )
    choice = models.CharField(
        _("Выбор"), max_length=20, choices=PLANT_CARE_CHOICES
    )
    description = models.CharField(_("Описание"), max_length=255)

    def __str__(self):
        return f"{self.choice}"


class Wishlist(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, blank=True, on_delete=models.CASCADE)
    plant_care = models.ForeignKey(
        PlantCare, blank=True, on_delete=models.CASCADE
    )

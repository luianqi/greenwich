import decimal

from django.db import models
from django.utils.translation import gettext_lazy as _

from products.models import Product, PlantCare
from users.models import Client, Employee


class CourierStatus(models.TextChoices):
    ACCEPTED = "Заказ принят"
    PICK_UP = "Еду за заказом"
    PICKED_UP = "Забрал заказ"
    DELIVERING = "Доставляю"
    DELIVERED = "Заказ доставлен"
    CANCEL = "Отменить заказ"
    CONFIRM = "Подтвердить"


class ClientStatus(models.TextChoices):
    PREPARING = "Готовим ваш заказ"
    READY = "Ваш заказ в пути"
    DELIVERED = "Заказ доставлен"


class Order(models.Model):
    client = models.ForeignKey(
        Client, null=True, blank=True, on_delete=models.CASCADE
    )
    courier = models.ForeignKey(Employee, null=True, blank=True, on_delete=models.CASCADE)
    first_name = models.CharField(_("Имя"), max_length=100)
    last_name = models.CharField(_("Фамилия"), max_length=100)
    phone_number = models.CharField(_("Номер телефона"), max_length=255)
    address = models.CharField(_("Адрес"), max_length=255)
    comment = models.CharField(
        _("Комментарий"), max_length=255, null=True, blank=True
    )
    client_status = models.CharField(
        _("Статусы клиента"), choices=ClientStatus.choices, max_length=255
    )
    courier_status = models.CharField(
        _("Статусы курьера"),
        choices=CourierStatus.choices,
        max_length=255,
        blank=True,
    )
    total_price = models.IntegerField(default=0)
    is_active = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)
    date_created = models.DateTimeField(_("Дата создания"), auto_now_add=True)

    def __str__(self):
        return f"Заказ {self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        if self.courier_status == "Еду за заказом":
            self.client_status = "Готовим ваш заказ"
        elif self.courier_status == "Доставляю":
            self.client_status = "Ваш заказ в пути"
        elif self.courier_status == "Заказ доставлен":
            self.client_status = "Заказ доставлен"
        elif self.courier_status == "Заказ принят":
            self.is_active = True
        elif self.courier_status == "Отменить заказ":
            self.is_cancelled = True
            products = self.products.filter(order=self.pk)
            for item in products:
                if item.product is not None:
                    item.product.quantity += item.quantity
                    item.product.total_sales -= item.quantity
                    item.product.save()
                else:
                    item.plant_care.quantity += item.quantity
                    item.plant_care.save()

        if self.is_cancelled is True:
            self.is_active = False

        if self.client_status == "Заказ доставлен":
            products = self.products.filter(order=self.pk)
            courier = self.courier
            self.is_active = False
            for item in products:
                if item.product:
                    courier.update_courier_allowance(
                        decimal.Decimal(item.product.price / 100 * 10)
                    )
                    florist = item.product.florist
                    florist.update_florist_allowance(
                        decimal.Decimal(item.product.price / 100 * 15)
                    )
                else:
                    courier.update_courier_allowance(
                        decimal.Decimal(item.plant_care.price / 100 * 10)
                    )
        super().save(*args, **kwargs)

    def calculate_total_price(self):
        self.total_price = 0
        products = self.products.filter(order=self.pk)
        for item in products:
            if item.product is not None:
                self.total_price += item.product.price * item.quantity
            elif item.plant_care is not None:
                self.total_price += item.plant_care.price * item.quantity
        return self.total_price

    @property
    def price_with_discount(self):
        self.total_price = 0
        products = self.products.filter(order=self.pk)
        for item in products:
            self.total_price += (
                item.product.price
                - (item.product.price * item.product.discount) / 100
            ) * item.quantity
        return self.total_price


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, null=True, blank=True, related_name="products", on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product, null=True, blank=True, on_delete=models.CASCADE
    )
    plant_care = models.ForeignKey(
        PlantCare,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    quantity = models.IntegerField(_("Количество"))
    date_created = models.DateTimeField(_("Дата создания"), auto_now_add=True)

from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.utils import timezone


class CustomAccountManager(BaseUserManager):
    def create_superuser(self, phone_number, password, **other_fields):

        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_active", True)
        other_fields.setdefault("role", "Админ")

        if other_fields.get("is_staff") is not True:
            raise ValueError("Superuser must be assigned to is_staff=True.")
        if other_fields.get("is_superuser") is not True:
            raise ValueError(
                "Superuser must be assigned to is_superuser=True."
            )
        if other_fields.get("is_active") is not True:
            raise ValueError("Superuser must be assigned to is_active=True.")

        return self.create_user(phone_number, password, **other_fields)

    def create_user(self, phone_number, password, **other_fields):
        if not phone_number:
            raise ValueError(_("You must provide your phone number"))

        phone_number = self.normalize_email(phone_number)
        user = self.model(phone_number=phone_number, **other_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class NewUser(AbstractBaseUser, PermissionsMixin):
    CLIENT = "Клиент"
    ADMIN = "Админ"
    COURIER = "Курьер"
    FLORIST = "Флорист"
    USER_TYPE_CHOICES = (
        (CLIENT, "Клиент"),
        (ADMIN, "Админ"),
        (COURIER, "Курьер"),
        (FLORIST, "Флорист"),
    )
    role = models.CharField(
        _("Роль"), max_length=20, choices=USER_TYPE_CHOICES, default=CLIENT
    )
    phone_number = models.CharField(
        _("Номер телефона"), max_length=17, unique=True
    )
    first_name = models.CharField(_("Имя"), max_length=255)
    last_name = models.CharField(_("Фамилия"), max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    new_password = models.CharField(max_length=255, null=True, blank=True)
    new_password2 = models.CharField(max_length=255, null=True, blank=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = "phone_number"

    def __str__(self):
        return f"{self.role}"


class Employee(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    courier_allowance = models.DecimalField(
        _("Надбавка курьера"), max_digits=9, decimal_places=2, default=0
    )
    florist_allowance = models.DecimalField(
        _("Надбавка флориста"), max_digits=9, decimal_places=2, default=0
    )
    florist_address = models.CharField(_("Адрес флориста"), max_length=250)
    salary = models.CharField(_("Зарплата"), max_length=255)
    created_at = models.DateTimeField(_("Дата создания"), auto_now_add=True)

    def __str__(self):
        return f"{self.user}"

    def update_courier_allowance(self, amount):
        self.courier_allowance += amount
        self.save()

    def update_florist_allowance(self, amount):
        self.florist_allowance += amount
        self.save()


class Client(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    address = models.CharField(_("Адрес"), max_length=255)
    last_name = models.CharField(_("Фамилия"), max_length=255)

    def __str__(self):
        return f"{self.user}"


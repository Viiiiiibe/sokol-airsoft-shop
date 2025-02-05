from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class CustomUser(AbstractUser):
    patronymic = models.CharField(blank=True, null=True, max_length=150, verbose_name='Отчество')
    email = models.EmailField(_('email address'), unique=True)
    phone_number = PhoneNumberField(blank=True, null=True, unique=True, verbose_name='Тлефон')
    vk = models.CharField(blank=True, null=True, max_length=150, verbose_name='VK')
    telegram = models.CharField(blank=True, null=True, max_length=150, verbose_name='Telegram')

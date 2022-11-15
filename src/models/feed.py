from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from src.intelhandler import constants
from src.models.indicator import Indicator
from src.models.abstract import TimeStampAbstractModel
from src.intelhandler.models import Source


class ParsingRule(TimeStampAbstractModel):
    """
    Модель правила для парсинга (CSV)
    """

    class Meta:
        verbose_name = "Правило парсинга"
        verbose_name_plural = "Правила парсинга"


class Feed(TimeStampAbstractModel):
    """
    Модель фида - источника данных.
    """

    type_of_feed = models.CharField(
        "Тип фида", max_length=4, choices=constants.TYPE_OF_FEED_CHOICES, default=constants.IP
    )
    format_of_feed = models.CharField(
        "Формат фида", max_length=15, choices=constants.FORMAT_OF_FEED_CHOICES, default=constants.TXT_FILE
    )
    auth_type = models.CharField(
        "Тип авторизации", max_length=3, choices=constants.TYPE_OF_AUTH_CHOICES, default=constants.NO_AUTH
    )
    polling_frequency = models.CharField(
        "Частота обновления фида",
        max_length=3,
        choices=constants.POLLING_FREQUENCY_CHOICES,
        default=constants.NEVER,
    )

    auth_login = models.CharField(
        "Логин для авторизации", max_length=32, blank=True, null=True
    )
    auth_password = models.CharField(
        "Пароль для авторизации", max_length=64, blank=True, null=True
    )
    ayth_querystring = models.CharField(
        "Строка для авторизации", max_length=128, blank=True, null=True
    )
    separator = models.CharField(
        "Разделитель для CSV формата", max_length=8, blank=True, null=True
    )
    parsing_rules = models.ManyToManyField(
        ParsingRule,
        verbose_name="Правила для парсинга",
        related_name="feed_parsing_rules",
        blank=True,
    )
    custom_field = models.CharField(
        "Кастомное поле", max_length=128, blank=True, null=True
    )
    sertificate = models.FileField("Файл сертификат", blank=True, null=True)
    vendor = models.CharField("Вендор", max_length=32)
    name = models.CharField("Название фида", max_length=32, unique=True)
    link = models.CharField("Ссылка на фид", max_length=255)
    confidence = models.IntegerField(
        "Достоверность", validators=[MaxValueValidator(100), MinValueValidator(0)], default=0
    )
    records_quantity = models.IntegerField("Количество записей", blank=True, null=True)
    indicators = models.ManyToManyField(
        Indicator, related_name="feeds", verbose_name="Индикатор", blank=True
    )

    update_status = models.CharField(max_length=15, choices=constants.TYPE_OF_STATUS_UPDATE, default=constants.ENABLED)

    ts = models.DateTimeField(auto_now_add=True)

    source = models.ForeignKey(Source, on_delete=models.SET_NULL, null=True, default=None)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"

    @classmethod
    def get_model_fields(cls):
        return [i.attname for i in cls._meta.fields]

    @classmethod
    def create_feed(cls, data: dict):
        fields = tuple(cls.get_model_fields())
        feed = {}
        for key in data:
            if key in fields:
                feed[key] = data[key]
        return Feed(**feed)

    class Meta:
        verbose_name = "Фид"
        verbose_name_plural = "Фиды"

from django.db import models

from src.models.abstract import TimeStampAbstractModel


class Tag(TimeStampAbstractModel):
    """
    Модель тега.
    """

    name = models.CharField("Название тега", max_length=30)
    colour = models.CharField("Название тега", max_length=30, blank=True, null=True)
    exportable = models.BooleanField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} | {self.colour}"

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

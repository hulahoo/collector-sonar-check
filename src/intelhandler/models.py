from django.db import models
from django.db.models import DateTimeField
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager, PermissionsMixin
from django.core.validators import MinValueValidator, MaxValueValidator

from src.intelhandler import constants
from src.models.indicator import Indicator
from src.models.tag import Tag


class CreationDateTimeField(DateTimeField):
    """
    CreationDateTimeField
    By default, sets editable=False, blank=True, auto_now_add=True
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("editable", False)
        kwargs.setdefault("blank", True)
        kwargs.setdefault("auto_now_add", True)
        DateTimeField.__init__(self, *args, **kwargs)

    def get_internal_type(self):
        return "DateTimeField"

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if self.editable is not False:
            kwargs["editable"] = True
        if self.blank is not True:
            kwargs["blank"] = False
        if self.auto_now_add is not False:
            kwargs["auto_now_add"] = True
        return name, path, args, kwargs


class ModificationDateTimeField(CreationDateTimeField):
    """
    ModificationDateTimeField
    By default, sets editable=False, blank=True, auto_now=True
    Sets value to now every time the object is saved.
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("auto_now", True)
        DateTimeField.__init__(self, *args, **kwargs)

    def get_internal_type(self):
        return "DateTimeField"

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if self.auto_now is not False:
            kwargs["auto_now"] = True
        return name, path, args, kwargs

    def pre_save(self, model_instance, add):
        if not getattr(model_instance, "update_modified", True):
            return getattr(model_instance, self.attname)
        return super().pre_save(model_instance, add)


class BaseModel(models.Model):
    """
    BaseModel
    An abstract base class model that provides self-managed
    "created" field and "modified" field.
    """

    created = CreationDateTimeField("создано")
    modified = ModificationDateTimeField("изменено")

    # origin = models.CharField("источник", max_length=128)

    class Meta:
        get_latest_by = "modified"
        abstract = True


class Role(BaseModel):
    name = models.CharField(max_length=255)
    level = models.IntegerField()


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    objects = UserManager()

    username = models.CharField(unique=True, max_length=255)

    role = models.ForeignKey('Role', on_delete=models.SET_NULL, null=True)

    @property
    def is_staff(self):
        return self.is_superuser

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []


class Source(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    is_instead_full = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    provider_name = models.CharField(max_length=255)
    path = models.TextField()
    certificate = models.FileField("Путь к сертификату", blank=True, null=True)
    authenticity = models.IntegerField(
        "Достоверность", validators=[MaxValueValidator(100), MinValueValidator(0)],
        default=0
    )
    format = models.CharField(
        "Формат", max_length=15, choices=constants.TYPE_OF_FORMAT, default=constants.CSV
    )

    auth_type = models.CharField(
        "Тип авторизации", max_length=3, choices=constants.TYPE_OF_AUTH_CHOICES, default=constants.NO_AUTH
    )
    auth_login = models.CharField(
        "Логин для авторизации", max_length=32, blank=True, null=True
    )
    auth_password = models.CharField(
        "Пароль для авторизации", max_length=64, blank=True, null=True
    )

    max_rows = models.IntegerField(default=None, null=True)
    raw_indicators = models.TextField(default=None, null=True)
    update_time_period = models.PositiveBigIntegerField(default=0)

    class Meta:
        verbose_name = 'Источник'
        verbose_name_plural = 'Источники'


class ActivityType(BaseModel):
    name = models.CharField(max_length=255)


class Activity(BaseModel):
    indicator = models.ForeignKey(Indicator, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.ForeignKey(ActivityType, on_delete=models.DO_NOTHING)
    comment = models.TextField(null=True, default=None)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=None)
    tag = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True, default=None)


class Task(BaseModel):
    source = models.ForeignKey('Source', on_delete=models.CASCADE)
    is_scheduled = models.BooleanField(default=False)


class Enrichment(BaseModel):
    type = models.CharField(
        "Тип индикатора", max_length=4, choices=constants.TYPE_OF_INDICATOR_CHOICES, default=constants.IP
    )
    link = models.TextField()  # www.google.com/?ip={}


class UserStatistic(BaseModel):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    method_name = models.CharField(max_length=100)


class Statistic(BaseModel):
    data = models.JSONField()


class LogStatistic(BaseModel):
    data = models.JSONField()


class PatternStorage(BaseModel):
    data = models.TextField()

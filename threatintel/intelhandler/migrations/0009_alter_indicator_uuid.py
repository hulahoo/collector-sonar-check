# Generated by Django 4.0.4 on 2022-08-03 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intelhandler', '0008_alter_feed_format_of_feed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='indicator',
            name='uuid',
            field=models.CharField(max_length=255, unique=True, verbose_name='Уникальный идентификатор индикатора'),
        ),
    ]

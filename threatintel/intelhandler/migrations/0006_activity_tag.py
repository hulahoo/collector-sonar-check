# Generated by Django 4.0.4 on 2022-08-12 12:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('intelhandler', '0005_enrichment_activity_tag_indicator_enrichment_context_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='tag',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='intelhandler.tag'),
        ),
    ]

# Generated by Django 5.0.6 on 2024-06-09 08:42

import catalog.models
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='manufactured_at',
            field=models.DateField(blank=True, null=True, verbose_name='Дата изготовления'),
        ),
        migrations.AlterField(
            model_name='product',
            name='created_at',
            field=models.DateField(default=django.utils.timezone.now, editable=False, verbose_name='Дата создания карточки'),
        ),
        migrations.AlterField(
            model_name='product',
            name='updated_at',
            field=catalog.models.AutoDateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Дата последнего изменения карточки'),
        ),
    ]

# Generated by Django 2.2.7 on 2019-12-04 18:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_auto_20191204_2309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='creationDate',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата создания заказа'),
        ),
        migrations.AlterField(
            model_name='temporder',
            name='creationDate',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата создания заказа'),
        ),
    ]

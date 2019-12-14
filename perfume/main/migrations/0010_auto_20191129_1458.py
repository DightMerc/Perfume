# Generated by Django 2.2.7 on 2019-11-29 09:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_auto_20191128_2221'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='priceforvolume',
            options={'verbose_name': 'Цена на объём', 'verbose_name_plural': 'Цены на объём'},
        ),
        migrations.RemoveField(
            model_name='product',
            name='volume',
        ),
        migrations.CreateModel(
            name='PriceForOption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.PositiveIntegerField(default='0', verbose_name='Цена')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Product', verbose_name='Продукт')),
                ('volume', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.FreeOptionGroup', verbose_name='Объём')),
            ],
            options={
                'verbose_name': 'Цена на опцию',
                'verbose_name_plural': 'Цены на опции',
            },
        ),
    ]

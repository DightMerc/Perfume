# Generated by Django 2.2.7 on 2019-12-06 10:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0022_auto_20191206_1523'),
    ]

    operations = [
        migrations.RenameField(
            model_name='groupcategory',
            old_name='categoies',
            new_name='categories',
        ),
    ]

# Generated by Django 4.1 on 2022-09-07 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_alter_productinfo_product_alter_productinfo_shop'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productinfo',
            name='model',
            field=models.CharField(max_length=80, verbose_name='Модель'),
        ),
    ]

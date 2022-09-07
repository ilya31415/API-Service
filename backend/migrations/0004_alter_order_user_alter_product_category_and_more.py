# Generated by Django 4.1 on 2022-09-07 15:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0003_alter_productinfo_model'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='backend.category', verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='productparameter',
            name='parameter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_parameters', to='backend.parameter', verbose_name='Параметр'),
        ),
        migrations.AlterField(
            model_name='productparameter',
            name='product_info',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_parameters', to='backend.productinfo', verbose_name='Информация о продукте'),
        ),
    ]
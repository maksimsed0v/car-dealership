# Generated by Django 2.2.7 on 2019-11-22 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_auto_20191122_1458'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='type',
            field=models.CharField(choices=[('1', 'покупка'), ('2', 'ремонт')], max_length=15, verbose_name='Тип заказа'),
        ),
    ]

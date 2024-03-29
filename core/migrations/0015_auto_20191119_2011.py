# Generated by Django 2.2.7 on 2019-11-19 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20191119_1954'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='carinorder',
            options={'verbose_name': 'Автомобиль', 'verbose_name_plural': 'Автомобили'},
        ),
        migrations.AlterModelOptions(
            name='repairinorder',
            options={'verbose_name': 'Ремонтная работа', 'verbose_name_plural': 'Ремонтные работы'},
        ),
        migrations.AlterModelOptions(
            name='sparepartinorder',
            options={'verbose_name': 'Запчасть', 'verbose_name_plural': 'Запчасти'},
        ),
        migrations.RenameField(
            model_name='repair',
            old_name='price',
            new_name='sales_price',
        ),
        migrations.AlterField(
            model_name='carinorder',
            name='number',
            field=models.PositiveIntegerField(default=1, verbose_name='Количество'),
        ),
        migrations.AlterField(
            model_name='carinorder',
            name='price_per_item',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Цена'),
        ),
        migrations.AlterField(
            model_name='carinorder',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Итого'),
        ),
        migrations.AlterField(
            model_name='repairinorder',
            name='number',
            field=models.PositiveIntegerField(default=1, verbose_name='Количество'),
        ),
        migrations.AlterField(
            model_name='repairinorder',
            name='price_per_item',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Цена'),
        ),
        migrations.AlterField(
            model_name='repairinorder',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Итого'),
        ),
        migrations.AlterField(
            model_name='sparepartinorder',
            name='number',
            field=models.PositiveIntegerField(default=1, verbose_name='Количество'),
        ),
        migrations.AlterField(
            model_name='sparepartinorder',
            name='price_per_item',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Цена'),
        ),
        migrations.AlterField(
            model_name='sparepartinorder',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Итого'),
        ),
    ]

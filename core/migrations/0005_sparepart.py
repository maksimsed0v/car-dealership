# Generated by Django 2.2.7 on 2019-11-16 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20191116_1038'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sparepart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='Название')),
                ('number', models.CharField(blank=True, max_length=20, null=True, verbose_name='Количество')),
                ('purchase_price', models.CharField(blank=True, max_length=20, null=True, verbose_name='Закупочная цена')),
                ('sales_price', models.CharField(blank=True, max_length=20, null=True, verbose_name='Продажная цена')),
                ('type', models.CharField(choices=[('1', 'в наличии'), ('2', 'не в наличии'), ('3', 'в ремонте')], default='в наличии', max_length=15, verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Запчасть',
                'verbose_name_plural': 'Запчасти',
            },
        ),
    ]
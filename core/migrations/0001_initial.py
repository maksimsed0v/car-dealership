# Generated by Django 2.2.7 on 2019-11-16 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mark', models.CharField(max_length=20, verbose_name='Модель')),
                ('color', models.CharField(max_length=20, verbose_name='Цвет')),
            ],
            options={
                'verbose_name': 'Автомобиль',
                'verbose_name_plural': 'Автомобили',
            },
        ),
    ]

# Generated by Django 2.2.7 on 2019-11-19 16:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_auto_20191118_1817'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='cars',
        ),
        migrations.RemoveField(
            model_name='order',
            name='price',
        ),
        migrations.RemoveField(
            model_name='order',
            name='repair',
        ),
        migrations.RemoveField(
            model_name='order',
            name='sparepart',
        ),
        migrations.AddField(
            model_name='order',
            name='total_price',
            field=models.PositiveIntegerField(blank=True, max_length=30, null=True, verbose_name='Итоговая стоимость'),
        ),
        migrations.AlterField(
            model_name='car',
            name='number',
            field=models.PositiveIntegerField(default=1, max_length=20, verbose_name='Количество'),
        ),
        migrations.AlterField(
            model_name='car',
            name='purchase_price',
            field=models.PositiveIntegerField(blank=True, max_length=20, null=True, verbose_name='Закупочная цена'),
        ),
        migrations.AlterField(
            model_name='car',
            name='sales_price',
            field=models.PositiveIntegerField(blank=True, max_length=20, null=True, verbose_name='Цена'),
        ),
        migrations.AlterField(
            model_name='car',
            name='type',
            field=models.CharField(choices=[('1', 'в наличии'), ('2', 'не в наличии')], default='1', max_length=15, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='car',
            name='year',
            field=models.PositiveIntegerField(blank=True, max_length=10, null=True, verbose_name='Год'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='employment_date',
            field=models.DateField(blank=True, max_length=15, null=True, verbose_name='Дата устройства'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='personal_account',
            field=models.PositiveIntegerField(blank=True, max_length=15, null=True, verbose_name='Лицевой счет'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='salary',
            field=models.PositiveIntegerField(blank=True, max_length=15, null=True, verbose_name='Зарплата'),
        ),
        migrations.AlterField(
            model_name='repair',
            name='price',
            field=models.PositiveIntegerField(max_length=20, verbose_name='Цена'),
        ),
        migrations.AlterField(
            model_name='sparepart',
            name='number',
            field=models.PositiveIntegerField(max_length=20, verbose_name='Количество'),
        ),
        migrations.AlterField(
            model_name='sparepart',
            name='purchase_price',
            field=models.PositiveIntegerField(blank=True, max_length=20, null=True, verbose_name='Закупочная цена'),
        ),
        migrations.AlterField(
            model_name='sparepart',
            name='sales_price',
            field=models.PositiveIntegerField(blank=True, max_length=20, null=True, verbose_name='Продажная цена'),
        ),
        migrations.CreateModel(
            name='SparepartInOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField(default=1)),
                ('price_per_item', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('total_price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('order', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.Order')),
                ('sparepart', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.Sparepart')),
            ],
            options={
                'verbose_name': 'Запчасть в заказе',
                'verbose_name_plural': 'Запчасти в заказе',
            },
        ),
        migrations.CreateModel(
            name='RepairInOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField(default=1)),
                ('price_per_item', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('total_price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('order', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.Order')),
                ('repair', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.Repair')),
            ],
            options={
                'verbose_name': 'Ремонтная работа в заказе',
                'verbose_name_plural': 'Ремонтные работы в заказе',
            },
        ),
        migrations.CreateModel(
            name='CarInOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField(default=1)),
                ('price_per_item', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('total_price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('car', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.Car')),
                ('order', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.Order')),
            ],
            options={
                'verbose_name': 'Автомобиль в заказе',
                'verbose_name_plural': 'Автомобили в заказе',
            },
        ),
    ]
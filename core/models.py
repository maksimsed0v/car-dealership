from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save, pre_delete
from django.dispatch import receiver
import datetime
from django.db import transaction
from utils.main import disable_for_loaddata
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.core.exceptions import ValidationError
from django.urls import reverse


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    TYPE_CHOICES = (
        ('1', "клиент"),
        ('2', "менеджер"),
        ('3', "администратор"),
    )
    type = models.CharField(max_length=15, verbose_name="Категория", choices=TYPE_CHOICES, default='клиент')
    SEX_CHOICES = (
        ('1', u"мужской"),
        ('2', u"женский"),
    )
    sex = models.CharField(max_length=15, verbose_name=u"пол", choices=SEX_CHOICES, null=True, blank=True)
    birth_date = models.DateField("Дата рождения", null=True, blank=True)
    location = models.CharField("Город", max_length=30, null=True, blank=True, default='')
    telephone = models.CharField("Телефон", max_length=15, null=True, blank=True)
    bio = models.TextField("О себе", max_length=500, null=True, blank=True)
    passport = models.CharField("Паспорт", max_length=15, null=True, blank=True, default='')
    positions = models.CharField("Должность", max_length=25, null=True, blank=True)
    salary = models.DecimalField("Зарплата", max_digits=15, decimal_places=2, default=0)
    personal_account = models.CharField("Лицевой счет", max_length=15, null=True, blank=True)
    employment_date = models.DateField("Дата устройства", null=True, blank=True)
    employment_record = models.CharField("Трудовая книжка", max_length=15, blank=True, null=True)

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Car(models.Model):
    mark = models.CharField("Модель", max_length=20)
    color = models.CharField("Цвет", max_length=20)
    year = models.PositiveIntegerField("Год", null=True, blank=True)
    TRANSMISSION_CHOICES = (
        ('1', u"автоматическая"),
        ('2', u"механическая"),
    )
    transmission = models.CharField(max_length=15, verbose_name=u"Коробка передач", choices=TRANSMISSION_CHOICES)
    number = models.PositiveIntegerField("Количество", default=1)
    purchase_price = models.DecimalField("Закупочная цена", max_digits=15, decimal_places=2, default=0)
    sales_price = models.DecimalField("Цена", max_digits=15, decimal_places=2, default=0)
    TYPE_CHOICES = (
        ('1', "в наличии"),
        ('2', "не в наличии"),
    )
    type = models.CharField(max_length=15, verbose_name="Статус", choices=TYPE_CHOICES, default='1')

    class Meta:
        verbose_name = "Автомобиль"
        verbose_name_plural = "Автомобили"
        ordering = ['mark']

    def __str__(self):
        return self.mark + " " + self.color

    def save(self, force_insert=False, force_update=False, **kwargs):
        if self.number == 0:
            self.type = 2
        if self.number != 0:
            self.type = 1
        super(Car, self).save(force_insert, force_update)


class Sparepart(models.Model):
    name = models.CharField("Название", max_length=20)
    number = models.PositiveIntegerField("Количество", default=1)
    purchase_price = models.DecimalField("Закупочная цена", max_digits=15, decimal_places=2, default=0)
    sales_price = models.DecimalField("Цена", max_digits=15, decimal_places=2, default=0)
    TYPE_CHOICES = (
        ('1', "в наличии"),
        ('2', "не в наличии"),
    )
    type = models.CharField(max_length=15, verbose_name="Статус", choices=TYPE_CHOICES, default='в наличии')

    class Meta:
        verbose_name = "Запчасть"
        verbose_name_plural = "Запчасти"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, **kwargs):
        if self.number == 0:
            self.type = 2
        if self.number != 0:
            self.type = 1
        super(Sparepart, self).save(force_insert, force_update)


class Repair(models.Model):
    name = models.CharField("Название", max_length=70)
    sales_price = models.DecimalField("Цена", max_digits=15, decimal_places=2, default=0)

    class Meta:
        verbose_name = "Ремонтная работа"
        verbose_name_plural = "Ремонтные работы"
        ordering = ['name']

    def __str__(self):
        return self.name


class Order(models.Model):
    client = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Клиент", related_name="client",
                               null=True, blank=True)
    employee = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Сотрудник", related_name="employee",
                                 null=True, blank=True)
    TYPE_CHOICES = (
        ('1', "покупка"),
        ('2', "ремонт"),
    )
    type = models.CharField(max_length=15, verbose_name="Тип заказа", choices=TYPE_CHOICES)
    STATUS_CHOICES = (
        ('1', u"заявка"),
        ('2', u"в процессе"),
        ('3', u"выполнен"),
    )
    status = models.CharField(max_length=15, verbose_name=u"Статус", choices=STATUS_CHOICES, default='1')
    date = models.DateField("Дата", default=datetime.date.today)
    total_price = models.DecimalField("Итоговая стоимость", max_digits=15, decimal_places=2, default=0)
    purchase_price = models.DecimalField("Закупочная стоимость", max_digits=15, decimal_places=2, default=0)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return "Заказ " + str(self.id)

    def get_absolute_url(self):
        if self.type == '1':
            return reverse('act_detail', args=[self.id])
        else:
            return reverse('attire_detail', args=[self.id])


class Report(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, verbose_name="Заказ", null=True, blank=True)
    date = models.DateField("Дата", default=datetime.date.today)
    purchase_price = models.DecimalField("Закупочная стоимость", max_digits=15, decimal_places=2, default=0)
    total_price = models.DecimalField("Итоговая стоимость", max_digits=15, decimal_places=2, default=0)
    price = models.DecimalField("Прибыль", max_digits=15, decimal_places=2, default=0)
    STATUS_CHOICES = (
        ('1', u"не выставлен"),
        ('2', u"выставлен"),
        ('3', u"оплачен"),
    )
    status = models.CharField(max_length=15, verbose_name=u"Статус", choices=STATUS_CHOICES, default='1')

    def save(self, *args, **kwargs):
        self.price = self.total_price - self.purchase_price
        super(Report, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Отчет"
        verbose_name_plural = "Отчеты"

    def __str__(self):
        return "Счет " + str(self.id)


@receiver(post_save, sender=Order)
def create_order_report(sender, instance, created, **kwargs):
    if created:
        Report.objects.create(order=instance, id=instance.id)


@receiver(post_save, sender=Order)
def save_order_report(sender, instance, **kwargs):
    if instance.status == '2':
        instance.report.status = '2'
    if instance.status == '3':
        instance.report.status = '3'
    instance.report.date = instance.date
    instance.report.purchase_price = instance.purchase_price
    instance.report.total_price = instance.total_price
    instance.report.price = (instance.report.total_price - instance.report.purchase_price)
    instance.report.save()


class CarInOrder(models.Model):
    car = models.ForeignKey(Car, verbose_name="Автомобиль", null=True, blank=True, default=None,
                            on_delete=models.CASCADE)
    order = models.ForeignKey(Order, null=True, blank=True, default=None, on_delete=models.CASCADE)
    number = models.PositiveIntegerField("Количество", default=1)
    price_per_item = models.DecimalField("Цена", max_digits=15, decimal_places=2, default=0)
    purchase_price = models.DecimalField("Закупочная стоимость", max_digits=15, decimal_places=2, default=0)
    total_price = models.DecimalField("Итого", max_digits=15, decimal_places=2, default=0)

    def __str__(self):
        return "%s" % self.car.mark

    class Meta:
        verbose_name = 'Автомобиль'
        verbose_name_plural = 'Автомобили'

    def save(self, *args, **kwargs):
        price_per_item = self.car.sales_price
        self.price_per_item = price_per_item
        purchase_price = self.car.purchase_price
        self.purchase_price = int(self.number) * purchase_price
        self.total_price = int(self.number) * price_per_item

        super(CarInOrder, self).save(*args, **kwargs)

    def clean(self):
        super(CarInOrder, self).clean()
        if self.pk is None:
            if self.number > self.car.number:
                raise ValidationError('Введите верное значение. Количество %s' % self + ' %s' % self.car.color +
                                      ' на складе, равняется %s' % self.car.number)
        else:
            car_in_order = CarInOrder.objects.filter(order=self.order, car=self.car)
            for item1 in car_in_order:
                if self.number > self.car.number + item1.number:
                    raise ValidationError('Введите верное значение. Количество %s' % self + ' %s' % self.car.color +
                                          ' на складе, равняется %s' % (self.car.number + item1.number))


class SparepartInOrder(models.Model):
    sparepart = models.ForeignKey(Sparepart, verbose_name="Запчасть", null=True, blank=True, default=None,
                                  on_delete=models.CASCADE)
    order = models.ForeignKey(Order, null=True, blank=True, default=None, on_delete=models.CASCADE)
    number = models.PositiveIntegerField("Количество", default=1)
    price_per_item = models.DecimalField("Цена", max_digits=15, decimal_places=2, default=0)
    purchase_price = models.DecimalField("Закупочная стоимость", max_digits=15, decimal_places=2, default=0)
    total_price = models.DecimalField("Итого", max_digits=15, decimal_places=2, default=0)

    def __str__(self):
        return "%s" % self.sparepart.name

    class Meta:
        verbose_name = 'Запчасть'
        verbose_name_plural = 'Запчасти'

    def save(self, *args, **kwargs):
        price_per_item = self.sparepart.sales_price
        self.price_per_item = price_per_item
        purchase_price = self.sparepart.purchase_price
        self.purchase_price = int(self.number) * purchase_price
        self.total_price = int(self.number) * price_per_item

        super(SparepartInOrder, self).save(*args, **kwargs)

    def clean(self):
        super(SparepartInOrder, self).clean()
        if self.pk is None:
            if self.number > self.sparepart.number:
                raise ValidationError('Введите верное значение. Количество %s' % self +
                                      ' на складе, равняется %s' % self.sparepart.number)
        else:
            sparepart_in_order = SparepartInOrder.objects.filter(order=self.order, sparepart=self.sparepart)
            for item1 in sparepart_in_order:
                if self.number > self.sparepart.number + item1.number:
                    raise ValidationError('Введите верное значение. Количество %s' % self +
                                          ' на складе, равняется %s' % (self.sparepart.number + item1.number))


class RepairInOrder(models.Model):
    repair = models.ForeignKey(Repair, verbose_name="Ремонтная работа", null=True, blank=True, default=None,
                               on_delete=models.CASCADE)
    order = models.ForeignKey(Order, null=True, blank=True, default=None, on_delete=models.CASCADE)
    number = models.PositiveIntegerField("Количество", default=1)
    price_per_item = models.DecimalField("Цена", max_digits=15, decimal_places=2, default=0)
    total_price = models.DecimalField("Итого", max_digits=15, decimal_places=2, default=0)

    def __str__(self):
        return "%s" % self.repair.name

    class Meta:
        verbose_name = 'Ремонтная работа'
        verbose_name_plural = 'Ремонтные работы'

    def save(self, *args, **kwargs):
        price_per_item = self.repair.sales_price
        self.price_per_item = price_per_item

        self.total_price = int(self.number) * price_per_item

        super(RepairInOrder, self).save(*args, **kwargs)


@disable_for_loaddata
def product_in_order_post_save(sender, instance, created, **kwargs):
    order = instance.order
    order_purchase_price = 0
    order_total_price = 0
    all_cars_in_order = CarInOrder.objects.filter(order=order)
    for item1 in all_cars_in_order:
        order_total_price += item1.total_price
        order_purchase_price += item1.purchase_price
        for car in Car.objects.filter(mark=item1, id=item1.car.id):
            car.number -= item1.number
            car.save()
    all_sparepart_in_order = SparepartInOrder.objects.filter(order=order)
    for item2 in all_sparepart_in_order:
        order_total_price += item2.total_price
        order_purchase_price += item2.purchase_price
        for sparepart in Sparepart.objects.filter(name=item2, id=item2.sparepart.id):
            sparepart.number -= item2.number
            sparepart.save()

    all_repair_in_order = RepairInOrder.objects.filter(order=order)
    for item3 in all_repair_in_order:
        order_total_price += item3.total_price

    instance.order.purchase_price = order_purchase_price
    instance.order.total_price = order_total_price
    instance.order.save(force_update=True)


# @disable_for_loaddata
def product_in_order_pre_save(sender, instance, **kwargs):
    order = instance.order

    all_cars_in_order = CarInOrder.objects.filter(order=order)
    for item1 in all_cars_in_order:
        for car in Car.objects.filter(mark=item1, id=item1.car.id):
            car.number += item1.number
            car.save()
    all_sparepart_in_order = SparepartInOrder.objects.filter(order=order)
    for item2 in all_sparepart_in_order:
        for sparepart in Sparepart.objects.filter(name=item2, id=item2.sparepart.id):
            sparepart.number += item2.number
            sparepart.save()

    instance.order.save(force_update=True)


# @disable_for_loaddata
def product_in_order_pre_delete(sender, instance, **kwargs):
    order = instance.order
    all_cars_in_order = CarInOrder.objects.filter(order=order)
    for item1 in all_cars_in_order:
        for car in Car.objects.filter(mark=item1, id=item1.car.id):
            car.number += item1.number
            car.save()
    all_sparepart_in_order = SparepartInOrder.objects.filter(order=order)
    for item2 in all_sparepart_in_order:
        for sparepart in Sparepart.objects.filter(name=item2, id=item2.sparepart.id):
            sparepart.number += item2.number
            sparepart.save()

    instance.order.save(force_update=True)


pre_delete.connect(product_in_order_pre_delete, sender=CarInOrder)
pre_delete.connect(product_in_order_pre_delete, sender=SparepartInOrder)
pre_delete.connect(product_in_order_pre_delete, sender=RepairInOrder)
pre_save.connect(product_in_order_pre_save, sender=CarInOrder)
pre_save.connect(product_in_order_pre_save, sender=SparepartInOrder)
pre_save.connect(product_in_order_pre_save, sender=RepairInOrder)
post_save.connect(product_in_order_post_save, sender=CarInOrder)
post_save.connect(product_in_order_post_save, sender=SparepartInOrder)
post_save.connect(product_in_order_post_save, sender=RepairInOrder)

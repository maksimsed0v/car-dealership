from django.shortcuts import render, get_object_or_404
from .models import *


def act_detail(request, self_id):
    act = get_object_or_404(Order.objects.filter(type='1', id=self_id))

    car_item = None
    cars = CarInOrder.objects.filter(order=act)
    for item1 in cars:
        car_item = item1

    sparepart_item = None
    spareparts = SparepartInOrder.objects.filter(order=act)
    for item2 in spareparts:
        sparepart_item = item2

    repair_item = None
    repairs = RepairInOrder.objects.filter(order=act)
    for item3 in repairs:
        repair_item = item3

    return render(request, 'core/order/act.html', {'act': act, 'cars': cars, 'car_item': car_item,
                                                   'spareparts': spareparts, 'sparepart_item': sparepart_item,
                                                   'repairs': repairs, 'repair_item': repair_item})


def attire_detail(request, self_id):
    attire = get_object_or_404(Order.objects.filter(type='2', id=self_id))

    car_item = None
    cars = CarInOrder.objects.filter(order=attire)
    for item1 in cars:
        car_item = item1

    sparepart_item = None
    spareparts = SparepartInOrder.objects.filter(order=attire)
    for item2 in spareparts:
        sparepart_item = item2

    repair_item = None
    repairs = RepairInOrder.objects.filter(order=attire)
    for item3 in repairs:
        repair_item = item3

    return render(request, 'core/order/attire.html', {'attire': attire, 'cars': cars, 'car_item': car_item,
                                                      'spareparts': spareparts, 'sparepart_item': sparepart_item,
                                                      'repairs': repairs, 'repair_item': repair_item})

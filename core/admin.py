from django.contrib import admin
from .models import *
from django.contrib import messages
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponseRedirect
from admin_interface.models import Theme


admin.site.unregister(Theme)

admin.site.site_header = 'Автосалон'
admin.site.site_title = 'Автосалон'
admin.site.index_title = 'Главная страница'


class CarInOrderInline(admin.TabularInline):
    model = CarInOrder
    extra = 0

    def get_readonly_fields(self, request, obj=None):
        fields = super().get_readonly_fields(self)
        if not getattr(obj, 'client', None) is None:
            if obj.status == '3':
                return ['car', 'number', 'price_per_item', 'purchase_price', 'total_price']
        return fields

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not (request.user.profile.type == '2') | (request.user.profile.type == '3'):
            if db_field.name == "car":
                kwargs["queryset"] = Car.objects.filter(type__in=[1])
            return super(CarInOrderInline, self).formfield_for_foreignkey(db_field, request, **kwargs)
        return super(CarInOrderInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_fields(self, request, obj=None):
        if not (request.user.profile.type == '2') | (request.user.profile.type == '3'):
            self.exclude = ('purchase_price',)
        if (request.user.profile.type == '2') | (request.user.profile.type == '3'):
            self.exclude = ()
        return super(CarInOrderInline, self).get_fields(request, obj)


class SparepartInOrderInline(admin.TabularInline):
    model = SparepartInOrder
    extra = 0

    def get_readonly_fields(self, request, obj=None):
        fields = super().get_readonly_fields(self)
        if not getattr(obj, 'client', None) is None:
            if obj.status == '3':
                return ['sparepart', 'number', 'price_per_item', 'purchase_price', 'total_price']
        return fields

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not (request.user.profile.type == '2') | (request.user.profile.type == '3'):
            if db_field.name == "sparepart":
                kwargs["queryset"] = Sparepart.objects.filter(type__in=[1])
            return super(SparepartInOrderInline, self).formfield_for_foreignkey(db_field, request, **kwargs)
        return super(SparepartInOrderInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_fields(self, request, obj=None):
        if not (request.user.profile.type == '2') | (request.user.profile.type == '3'):
            self.exclude = ('purchase_price',)
        if (request.user.profile.type == '2') | (request.user.profile.type == '3'):
            self.exclude = ()
        return super(SparepartInOrderInline, self).get_fields(request, obj)


class RepairInOrderInline(admin.TabularInline):
    model = RepairInOrder
    extra = 0

    def get_readonly_fields(self, request, obj=None):
        fields = super().get_readonly_fields(self)
        if not getattr(obj, 'client', None) is None:
            if obj.status == '3':
                return ['repair', 'number', 'price_per_item', 'total_price']
        return fields


# @admin.register(CarInOrder)
class CarInOrderAdmin(admin.ModelAdmin):

    list_display = [field.name for field in CarInOrder._meta.fields]

    class Meta:
        model = CarInOrder




# @admin.register(SparepartInOrder)
class SparepartInOrderAdmin(admin.ModelAdmin):
    list_display = [field.name for field in SparepartInOrder._meta.fields]

    class Meta:
        model = SparepartInOrder


# @admin.register(RepairInOrder)
class RepairInOrderAdmin(admin.ModelAdmin):
    list_display = [field.name for field in RepairInOrder._meta.fields]

    class Meta:
        model = RepairInOrder


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['mark', 'color', 'transmission', 'type', 'sales_price']
    list_filter = ('mark', 'color', 'transmission', 'type')

    def get_readonly_fields(self, request, obj=None):
        fields = super().get_readonly_fields(self)
        if not (request.user.profile.type == '2') | (request.user.profile.type == '3'):
            return ['sales_price']
        if request.user.profile.type == '2':
            return ['purchase_price']
        return fields

    def get_fields(self, request, obj=None):
        if not (request.user.profile.type == '2') | (request.user.profile.type == '3'):
            self.exclude = ('purchase_price', 'type', 'number')
        if (request.user.profile.type == '2') | (request.user.profile.type == '3'):
            self.exclude = ()
        return super(CarAdmin, self).get_fields(request, obj)

    def get_queryset(self, request):
        qs = super(CarAdmin, self).get_queryset(request)
        if (request.user.profile.type == '2') | (request.user.profile.type == '3'):
            return qs
        return qs.filter(type=1)

    class Meta:
        form = Car


@admin.register(Sparepart)
class SparepartAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'sales_price']
    list_filter = ('type',)

    def get_fields(self, request, obj=None):
        if not (request.user.profile.type == '2') | (request.user.profile.type == '3'):
            self.exclude = ('purchase_price', 'type', 'number')
        if (request.user.profile.type == '2') | (request.user.profile.type == '3'):
            self.exclude = ()
        return super(SparepartAdmin, self).get_fields(request, obj)

    def get_readonly_fields(self, request, obj=None):
        fields = super().get_readonly_fields(self)
        if not (request.user.profile.type == '2') | (request.user.profile.type == '3'):
            return ['sales_price']
        if request.user.profile.type == '2':
            return ['purchase_price']
        return fields


@admin.register(Repair)
class RepairAdmin(admin.ModelAdmin):
    list_display = ['name', 'sales_price']


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Report._meta.fields]
    list_filter = ('date', 'status')

    def get_readonly_fields(self, request, obj=None):
        fields = super().get_readonly_fields(self)
        return ['order', 'date', 'purchase_price', 'total_price', 'price', 'status']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'type']
    list_filter = ('type',)

    def get_fields(self, request, obj=None):
        if not request.user.profile.type == '3':
            self.exclude = ('user', 'type', 'passport', 'positions', 'salary', 'personal_account', 'employment_date',
                            'employment_record')
        if request.user.profile.type == '3':
            self.exclude = ()
        return super(ProfileAdmin, self).get_fields(request, obj)

    def get_queryset(self, request):
        qs = super(ProfileAdmin, self).get_queryset(request)
        if request.user.profile.type == '3':
            return qs
        elif request.user.profile.type == '2':
            return qs.filter(type__in=[1, 2])
        return qs.filter(user=request.user)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'client', 'employee', 'type', 'status', 'date', 'total_price']
    inlines = [CarInOrderInline, SparepartInOrderInline, RepairInOrderInline]
    list_filter = ('type', 'status', 'date')

    def get_readonly_fields(self, request, obj=None):
        fields = super().get_readonly_fields(self)
        if not (request.user.profile.type == '2') | (request.user.profile.type == '3'):
            return ['total_price', ]
        if not getattr(obj, 'client', None) is None:
            if obj.status == '3':
                return ['client', 'employee', 'type', 'status', 'date', 'total_price', 'purchase_price']
        return fields

    def get_fields(self, request, obj=None):
        if not (request.user.profile.type == '2') | (request.user.profile.type == '3'):
            self.exclude = ('client', 'employee', 'status', 'date', 'purchase_price')
        if (request.user.profile.type == '2') | (request.user.profile.type == '3'):
            self.exclude = ()
        return super(OrderAdmin, self).get_fields(request, obj)

    def get_queryset(self, request):
        qs = super(OrderAdmin, self).get_queryset(request)
        if (request.user.profile.type == '2') | (request.user.profile.type == '3'):
            return qs
        return qs.filter(client=request.user)

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'client', None) is None:
            obj.client = request.user
        obj.save()

    def response_change(self, request, obj):
        if "_attire" in request.POST:
            return HttpResponseRedirect("/documents/attire/%s" % obj.id)
        if "_act" in request.POST:
            return HttpResponseRedirect("act %s" % obj.id)
        return super().response_change(request, obj)

import logging

from django.contrib import admin
from django.db.models import Q

from .models import PurchaseOrder, PurchaseOrderHistory, PurchaseOrderItem, Vendor
from .validators import is_smartavi, is_vendor

logger = logging.getLogger()


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = [
        "name",
    ]


class PurchaseOrderItemInline(admin.StackedInline):
    model = PurchaseOrderItem
    extra = 0
    min_num = 1


class PurchaseOrderHistoryInline(admin.StackedInline):
    model = PurchaseOrderHistory
    extra = 0
    min_num = 0
    readonly_fields = ["created_by", "created_at"]
    verbose_name_plural = "purchase order history"


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    search_fields = ["order_number"]
    list_display = [
        "order_number",
        "vendor",
        "status",
        "supplier_ack",
        "eta",
        "updated_at",
        "created_by",
        "created_at",
    ]
    inlines = [
        PurchaseOrderItemInline,
        PurchaseOrderHistoryInline,
    ]
    readonly_fields = ["created_by", "created_at", "updated_at"]

    def get_list_filter(self, request):
        list_filter = ["status"]
        if is_vendor(request.user):
            return list_filter
        list_filter += ["vendor__name"]
        return list_filter

    def get_queryset(self, request):
        if is_vendor(request.user):
            qs = self.model._default_manager.get_queryset_for_vendor(request.user)
        else:
            qs = self.model._default_manager.get_queryset()
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        super().save_model(request, obj, form, change)

    def save_related(self, request, form, formsets, change):
        purchase_order_history_formset = formsets[1]
        for f in purchase_order_history_formset.forms:
            f.instance.created_by = request.user
        super().save_related(request, form, formsets, change)

    def get_form(self, request, obj=None, **kwargs):
        if is_vendor(request.user):
            self.readonly_fields += ["order_number", "description", "vendor"]
        if is_smartavi(request.user):
            self.readonly_fields += ["supplier_ack", "eta"]
        form = super().get_form(request, obj, **kwargs)
        return form

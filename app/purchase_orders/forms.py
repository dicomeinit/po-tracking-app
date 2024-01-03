from django import forms

from app.purchase_orders.models import PurchaseOrder, PurchaseOrderItem


class PurchaseOrderForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = [
            # 'part_number',
            "description",
            # 'quantity',
            "order_number",
            "comments",
            "vendor",
        ]
        exclude = ["created_by", "updated_at", "created_at"]


class PartForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrderItem
        fields = [
            "part_number",
            "quantity",
        ]


class PurchaseOrderAdminForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = "__all__"
        exclude = ["created_by", "updated_at", "created_at"]

from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand

from app.purchase_orders.constants import GROUP_NAME_COMPANY, GROUP_NAME_VENDOR


class Command(BaseCommand):
    help = "Creates the specified groups for admin site"

    groups = {
        GROUP_NAME_VENDOR: [
            "change_purchaseorder",
            "view_purchaseorder",
            "view_purchaseorderitem",
            "add_purchaseorderhistory",
            "view_purchaseorderhistory",
        ],
        GROUP_NAME_COMPANY: [
            "add_purchaseorder",
            "change_purchaseorder",
            "view_purchaseorder",
            "view_purchaseorderitem",
            "add_purchaseorderitem",
            "change_purchaseorderitem",
            "view_purchaseorderhistory",
        ],
    }

    def handle(self, *args, **options):
        for group_name, group_rules in self.groups.items():
            group, _ = Group.objects.get_or_create(name=group_name)
            permissions = Permission.objects.filter(codename__in=group_rules).all()
            for permission in permissions:
                group.permissions.add(permission)
            group.save()
            self.stdout.write(
                self.style.SUCCESS(
                    'Successfully created group "%s" with permissions' % group_name
                )
            )

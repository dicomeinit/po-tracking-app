from typing import TYPE_CHECKING

from app.purchase_orders.constants import GROUP_NAME_COMPANY, GROUP_NAME_VENDOR

if TYPE_CHECKING:
    from django.contrib.auth.models import User


def is_vendor(user: "User") -> bool:
    return user.groups.filter(name=GROUP_NAME_VENDOR).exists()


def is_smartavi(user: "User") -> bool:
    return user.groups.filter(name=GROUP_NAME_COMPANY).exists()

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from app.views import robots_txt

urlpatterns = [
    path("robots.txt/", robots_txt),
    path("admin/", admin.site.urls),
    path(
        "orders/",
        include(
            ("purchase_orders.urls", "purchase_orders"), namespace="purchase_orders"
        ),
    ),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

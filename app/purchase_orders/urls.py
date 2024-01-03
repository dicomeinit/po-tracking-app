from django.urls import path

from .views import UploadOrdersView

urlpatterns = [path("upload/", UploadOrdersView.as_view(), name="upload")]

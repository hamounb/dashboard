from django.urls import path
from .views import *


app_name = "store"

urlpatterns = [
    path("file/upload/", FileUploadView.as_view(), name="file-upload"),
    path("customer/list/", CustomerListView.as_view(), name="customer-list"),
    path("customer/list/<int:cid>/", CustomerDetailsView.as_view(), name="customer-details"),
    path("date/list/", DateListView.as_view(), name="date-list"),
    path("sale/<int:did>/", SaleView.as_view(), name="sale"),
]
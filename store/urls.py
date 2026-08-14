from django.urls import path
from .views import *


app_name = "store"

urlpatterns = [
    path("index/", IndexView.as_view(), name="index"),
    path("file/upload/", FileUploadView.as_view(), name="file-upload"),
    path("customer/list/", CustomerListView.as_view(), name="customer-list"),
    path("customer/list/<int:cid>/", CustomerDetailsView.as_view(), name="customer-details"),
    path("date/list/", DateListView.as_view(), name="date-list"),
    path("date/duration/<str:ddn>/", DateDurationView.as_view(), name="date-duration"),
    path("sale/details/<int:did>/", SaleDetailsView.as_view(), name="sale-details"),
    path("product/list/", ProductListView.as_view(), name="product-list"),
    path("product/details/<int:pid>/", ProductDetailsView.as_view(), name="product-details"),
]
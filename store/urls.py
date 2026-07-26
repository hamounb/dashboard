from django.urls import path
from .views import *


app_name = "store"

urlpatterns = [
    path("file/upload/", FileUploadView.as_view(), name="file-upload"),
    path("file/open/<int:fid>/", FileOpenView.as_view(), name="file-open"),
    path("customer/list/", CustomerListView.as_view(), name="customer-list"),
    path("customer/list/<int:cid>/", CustomerDetailsView.as_view(), name="customer-details"),
    path("date/list/", DateListView.as_view(), name="date-list"),
]
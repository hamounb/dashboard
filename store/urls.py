from django.urls import path
from .views import *


app_name = "store"

urlpatterns = [
    path("file/upload/", FileUploadView.as_view(), name="file-upload"),
    path("file/open/<int:fid>/", FileOpenView.as_view(), name="file-open"),
]
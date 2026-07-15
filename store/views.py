from django.shortcuts import render, redirect, get_object_or_404
from django import views
from django.contrib.auth.models import User
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Q
from django.contrib import messages
from .models import *
from .forms import *

# Create your views here.

class Test(PermissionRequiredMixin, views.View):
    login_url = 'accounts:signin'
    permission_required = ['crm.add_customermodel', 'crm.add_requestmodel']

    def get(self, request):
        return render(request, 'staff/test.html')


class CustomerListView(PermissionRequiredMixin, views.View):
    login_url = "accounts:signin"
    permission_required = ["store.view_customermodel"]

    def get(self, request):
        customer = CustomerModel.objects.all()
        context = {
            "customer":customer,
        }
        return render(request, "store/customer-list.html", context)
    

class DateListView(PermissionRequiredMixin, views.View):
    login_url = "accounts:login"
    permission_required = ["store.view_datemodel"]

    def get(self, request):
        date = DateModel.objects.all()
        context = {
            "date":date,
        }
        return render(request, "store/date-list.html", context)
    

class ProductListView(PermissionRequiredMixin, views.View):
    login_url = "accounts:login"
    permission_required = ["store.view_productmodel"]

    def get(self, request):
        product = ProductModel.objects.all()
        context = {
            "product":product,
        }
        return render(request, "store/product-list.html")
    

class FileUploadView(PermissionRequiredMixin, views.View):
    login_url = "accounts:login"
    permission_required = ["store.add_filemodel"]

    def get(self, request):
        form = FileUploadForm()
        context = {
            "form":form,
        }
        return render(request, "store/file-upload.html")
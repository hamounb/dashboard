from django.shortcuts import render, redirect, get_object_or_404
from django import views
from django.contrib.auth.models import User
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Q
from django.contrib import messages
from .models import *
from .forms import *
import openpyxl
import pandas as pd


# Create your views here.

COLUMN_MAP = {
    "code": ["کد مشتری", "customer_code", "کد مشتریان"],
    "name": ["نام مشتری", "customer_name", "نام و نام خانوادگی"],
    "count": ["متراژ", "مقدار", "count"],
    "price_total": ["مبلغ فروش", "مبلغ کل", "price_total"],
}

def find_column(df, possible_names):
    for col in df.columns:
        col_clean = str(col).strip().replace("\n", "").replace("\r", "")
        if col_clean in possible_names:
            return col_clean
    return None


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
    

class FileUploadView(views.View):
    login_url = ""
    permission_required = ["store.add_filemodel"]

    def get(self, request):
        form = FileUploadForm()
        context = {
            "form":form,
        }
        return render(request, "store/file-upload.html", context)
    
    def post(self, request):
        form = FileUploadForm(request.POST, request.FILES)
        context = {
            "form":form,
        }
        if form.is_valid():
            instance = form.save()
            return redirect("store:file-open", fid=instance.pk)
        else:
            return render(request, "store/file-upload.html", context)


class FileOpenView(views.View):

    def get(self, request, fid):
        file = get_object_or_404(FileModel, pk=fid)
        # source = file.file.url
        # wb = openpyxl.load_workbook(f"/home/uif/Documents/Projects/Project Management Dashboard/dashboard/{source}")
        excel_path = file.file.path
        df = pd.read_excel(excel_path)
        col_code = find_column(df, COLUMN_MAP["code"])
        col_name = find_column(df, COLUMN_MAP["name"])
        col_count = find_column(df, COLUMN_MAP["count"])
        col_price_total = find_column(df, COLUMN_MAP["price_total"])
        # اگر ستونی پیدا نشد، خطا بده
        if not all([col_code, col_name, col_count, col_price_total]):
            raise ValueError("ستون‌های لازم در فایل اکسل پیدا نشدند")
        for _, row in df.iterrows():
            code = str(row[col_code]).strip()
            name = str(row[col_name]).strip()
            count = str(row[col_count]).strip()
            price_total = str(row[col_price_total]).strip()
            customer, _ = CustomerModel.objects.get_or_create(
                code=code,
                defaults={"name": name, "user_created": request.user}
            )
            SaleModel.objects.create(
                customer=customer,
                product=None,
                count=count,
                price="0",
                price_total=price_total,
                user_created=request.user
            )
        return render(request, "store/file-open.html")
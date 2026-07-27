from django.shortcuts import render, redirect, get_object_or_404
from django import views
from django.contrib.auth.models import User
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Q
from django.db import IntegrityError
from django.contrib import messages
from .models import *
from .forms import *
import pandas as pd


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
        count = customer.count()
        customer_total_price = 0
        total_count = 0
        total_price = 0
        sales = {}
        for i in customer:
            sale = SaleModel.objects.filter(customer=i)
            total_count = 0
            total_price = 0
            for j in sale:
                if j.count:
                    total_count += float(j.count)
                    total_count = round(total_count, 4)
                else:
                    pass
                if j.price_total.isnumeric():
                    total_price += float(j.price_total)
                else:
                    pass
            customer_total_price += total_price
            sales[i.code] = {"count":total_count, "price":total_price}
        context = {
            "customer":customer,
            "sales":sales,
            "count":count,
            "customer_total_price":customer_total_price,
        }
        return render(request, "store/customer-list.html", context)


class CustomerDetailsView(PermissionRequiredMixin, views.View):
    login_url = "accounts:signin"
    permission_required = ["store.view_customermodel"]

    def get(self, request, cid):
        customer = get_object_or_404(CustomerModel, pk=cid)
        sale = SaleModel.objects.filter(customer=customer)
        total_count = 0
        total_price = 0
        for i in sale:
            if i.count:
                total_count += float(i.count)
                total_count = round(total_count, 4)
            else:
                pass
            if i.price_total.isnumeric():
                total_price += float(i.price_total)
            else:
                pass
        context = {
            "customer":customer,
            "sale":sale,
            "total_count":total_count,
            "total_price":total_price,
        }
        return render(request, "store/customer-details.html", context)
    

class DateListView(PermissionRequiredMixin, views.View):
    login_url = "accounts:login"
    permission_required = ["store.view_datemodel"]

    def get(self, request):
        date = DateModel.objects.all().order_by("day")
        form = DurationForm()
        context = {
            "date":date,
            "form":form,
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


COLUMN_MAP = {
    "code": ["کد مشتری", "customer_code", "کد مشتریان"],
    "code_p": ["کد محصولات", "کد محصول", "کد کالا", "کد خدمت", "product_code"],
    "name": ["نام مشتری", "customer_name", "نام و نام خانوادگی"],
    "name_p": ["نام محصول", "مشخصات", "مشخصات محصول", "نام محصولات", "نام کالا", "کالا", "خدمت", "product_name"],
    "count": ["متراژ", "مقدار", "count"],
    "price": ["فی", "قیمت", "مبلغ", "price"],
    "price_total": ["مبلغ فروش", "مبلغ کل", "price_total"],
}

def find_column(df, possible_names):
    for col in df.columns:
        col_clean = str(col).strip().replace("\n", "").replace("\r", "")
        if col_clean in possible_names:
            return col_clean
    return None
    

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
            day = form.cleaned_data.get("day")
            month = form.cleaned_data.get("month")
            year = form.cleaned_data.get("year")
            category = form.cleaned_data.get("category")
            file = form.cleaned_data.get("file")
            if str(category) == "sale":
                print("mm")
                try:
                    date = DateModel.objects.get(day=day, month=month, year=year)
                    print("yes")
                except DateModel.DoesNotExist:
                    date = DateModel(day=day, month=month, year=year)
                    date.save()
                    print("no")
                upload = FileModel.objects.create(date=date, category=category, file=file)
                upload.save()
                excel_path = upload.file.path
                df = pd.read_excel(excel_path)
                col_code = find_column(df, COLUMN_MAP["code"])
                col_name = find_column(df, COLUMN_MAP["name"])
                col_code_p = find_column(df, COLUMN_MAP["code_p"])
                col_name_p = find_column(df, COLUMN_MAP["name_p"])
                col_count = find_column(df, COLUMN_MAP["count"])
                col_price = find_column(df, COLUMN_MAP["price"])
                col_price_total = find_column(df, COLUMN_MAP["price_total"])
                if not all([col_code, col_name, col_count, col_price_total]):
                    raise ValueError("ستون‌های لازم در فایل اکسل پیدا نشدند!")
                for row in df.iterrows():
                    customer_code = str(row[col_code])
                    customer_name = str(row[col_name])
                    product_code = str(row[col_code_p])
                    product_name = str(row[col_name_p])
                    count = str(row[col_count])
                    price = str(row[col_price])
                    price_total = str(row[col_price_total])
                    try:
                        customer = CustomerModel.objects.get(code=customer_code)
                    except CustomerModel.DoesNotExist:
                        customer = CustomerModel.objects.create(code=customer_code, name=customer_name, user_created=request.user)
                        customer.save()
                    try:
                        product = ProductModel.objects.get(code=product_code)
                    except ProductModel.DoesNotExist:
                        product = ProductModel.objects.create(code=product_code, name=product_name, user_created=request.user)
                        product.save()
                    try:
                        sale = SaleModel.objects.create(
                            date=date,
                            product=product,
                            customer=customer,
                            count=count,
                            price=price,
                            price_total=price_total,
                        )
                        sale.save()
                    except IntegrityError:
                        pass
            else:
                print("false")
            return render(request, "store/file-upload.html", context)
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
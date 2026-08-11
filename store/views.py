from django.shortcuts import render, redirect, get_object_or_404
from django import views
from django.contrib.auth.models import User
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Q, Sum
from django.db.models.functions import Cast
from django.db import IntegrityError
from django.contrib import messages
from .models import *
from .forms import *
import pandas as pd
from django.core.paginator import Paginator


# Create your views here.


class Test(PermissionRequiredMixin, views.View):
    login_url = "login"
    permission_required = ['crm.add_customermodel', 'crm.add_requestmodel']

    def get(self, request):
        return render(request, 'staff/test.html')


class IndexView(PermissionRequiredMixin, views.View):
    login_url = "login"
    permission_required = []

    def get(self, request):
        date = DateModel.objects.order_by("-year", "-month", "-day")
        last_date = date.first()
        duration = DateModel.objects.order_by("-year", "-month", "-day")[:6]
        duration_result = {}
        for i in duration:
            sales = SaleModel.objects.filter(date=i)
            for j in sales:
                if f"{j.date.year}/{j.date.month}/{j.date.day}" in duration_result:
                    duration_result[f"{j.date.year}/{j.date.month}/{j.date.day}"]["count"] += float(j.count)
                    duration_result[f"{j.date.year}/{j.date.month}/{j.date.day}"]["count"] = round(duration_result[f"{j.date.year}/{j.date.month}/{j.date.day}"]["count"], 4)
                    duration_result[f"{j.date.year}/{j.date.month}/{j.date.day}"]["total_price"] += int(j.price_total)
                else:
                    duration_result[f"{j.date.year}/{j.date.month}/{j.date.day}"] = {"count":0, "total_price":0}
                    duration_result[f"{j.date.year}/{j.date.month}/{j.date.day}"]["count"] = float(j.count)
                    duration_result[f"{j.date.year}/{j.date.month}/{j.date.day}"]["count"] = round(duration_result[f"{j.date.year}/{j.date.month}/{j.date.day}"]["count"], 4)
                    duration_result[f"{j.date.year}/{j.date.month}/{j.date.day}"]["total_price"] = int(j.price_total)
        top_products = (
            SaleModel.objects
            .filter(date__in=duration)
            .annotate(count_int=Cast('count', models.IntegerField()))
            .values('product__id', 'product__name')
            .annotate(total_count=Sum('count_int'))
            .order_by('-total_count')[:10]
        )
        top_customers = (
                    SaleModel.objects
                    .filter(date__in=duration)
                    .annotate(count_int=Cast('price_total', models.IntegerField()))
                    .values('customer__id', 'customer__name')
                    .annotate(total_price=Sum('count_int'))
                    .order_by('-total_price')[:10]
                )
        sale = SaleModel.objects.filter(date=last_date)
        total_price = 0
        total_count = 0
        for i in sale:
            total_price += int(i.price_total)
            total_count += float(i.count)
        total_count = round(total_count, 4)
        product = sale.annotate(my_int_field=Cast("count", output_field=models.IntegerField())).order_by("-my_int_field").first()
        customer = sale.annotate(my_int_field=Cast("price_total", output_field=models.IntegerField())).order_by("-my_int_field").first()
        context = {
            "date":date,
            "sale":sale,
            "product":product,
            "customer":customer,
            "total_price":total_price,
            "total_count":total_count,
            "duration_result":duration_result,
            "top_products":top_products,
            "top_customers":top_customers,
        }
        return render(request, "store/index.html", context)


class CustomerListView(PermissionRequiredMixin, views.View):
    login_url = "login"
    permission_required = ["store.view_customermodel"]

    def get(self, request):
        customers = CustomerModel.objects.all()
        count = customers.count()
        customer_total_price = 0
        total_count = 0
        total_price = 0
        sales = {}
        for i in customers:
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
                    total_price += int(j.price_total)
                else:
                    pass
            customer_total_price += total_price
            sales[i.code] = {"count":total_count, "price":total_price}
        paginator = Paginator(customers, 24)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        offset = (page_obj.number - 1) * paginator.per_page
        context = {
            "page_obj":page_obj,
            "offset":offset,
            "sales":sales,
            "count":count,
            "customer_total_price":customer_total_price,
        }
        return render(request, "store/customer-list.html", context)


class CustomerDetailsView(PermissionRequiredMixin, views.View):
    login_url = "login"
    permission_required = ["store.view_customermodel"]

    def get(self, request, cid):
        customer = get_object_or_404(CustomerModel, pk=cid)
        sales = SaleModel.objects.filter(customer=customer)
        top_count = (
            sales
            .annotate(count_int=Cast('count', models.IntegerField()))
            .values('product__code', 'product__name')
            .annotate(total_count=Sum('count_int'))
            .order_by('-total_count')[:10]
        )
        total_count = (
            sales
            .annotate(count_int=Cast('count', models.IntegerField()))
            .aggregate(total_count=Sum('count_int'))['total_count']
        )
        top_price = (
            sales
            .annotate(price_int=Cast('price_total', models.IntegerField()))
            .values('product__code', 'product__name')
            .annotate(total_price=Sum('price_int'))
            .order_by('-total_price')[:10]
        )
        total_price = (
            sales
            .annotate(count_int=Cast('price_total', models.IntegerField()))
            .aggregate(total_price=Sum('count_int'))['total_price']
        )
        sales = sales.order_by("date")
        paginator = Paginator(sales, 24)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        offset = (page_obj.number - 1) * paginator.per_page
        context = {
            "page_obj":page_obj,
            "offset":offset,
            "customer":customer,
            "top_count":top_count,
            "total_count":total_count,
            "total_price":total_price,
            "top_price":top_price,
        }
        return render(request, "store/customer-details.html", context)
    

class DateListView(PermissionRequiredMixin, views.View):
    login_url = "login"
    permission_required = []

    def get(self, request):
        date = DateModel.objects.all().order_by("day")
        form = DurationForm()
        context = {
            "date":date,
            "form":form,
        }
        return render(request, "store/date-list.html", context)


class DateDurationView(PermissionRequiredMixin, views.View):
    login_url = "login"
    permission_required = []

    def get(self, request, ddn):
        if ddn == "3":
            date = DateModel.objects.order_by("-year", "-month", "-day")[:3]
        elif ddn == "7":
            date = DateModel.objects.order_by("-year", "-month", "-day")[:7]
        elif ddn == "30":
            date = DateModel.objects.order_by("-year", "-month", "-day")[:30]
        elif ddn == "90":
            date = DateModel.objects.order_by("-year", "-month", "-day")[:90]
        else:
            pass
        sales = SaleModel.objects.filter(date__in=date)
        top_count = (
            sales
            .annotate(count_int=Cast('count', models.IntegerField()))
            .values('product__code', 'product__name')
            .annotate(total_count=Sum('count_int'))
            .order_by('-total_count')[:10]
        )
        top_price = (
            sales
            .annotate(price_int=Cast('price_total', models.IntegerField()))
            .values('customer__code', 'customer__name')
            .annotate(total_price=Sum('price_int'))
            .order_by('-total_price')[:10]
        )
        sales = sales.order_by("date")
        paginator = Paginator(sales, 24)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        offset = (page_obj.number - 1) * paginator.per_page
        context = {
            "ddn":ddn,
            "page_obj":page_obj,
            "offset":offset,
            "top_count":top_count,
            "top_price":top_price,
        }
        return render(request, "store/date-duration.html", context)


class SaleDetailsView(PermissionRequiredMixin, views.View):
    login_url = "login"
    permission_required = []

    def get(self, request, did):
        date = get_object_or_404(DateModel, pk=did)
        sale = SaleModel.objects.filter(date__pk=did)
        top_count = (
            sale
            .annotate(count_int=Cast('count', models.IntegerField()))
            .values('product__code', 'product__name')
            .annotate(total_count=Sum('count_int'))
            .order_by('-total_count')[:5]
        )
        top_price = (
            sale
            .annotate(price_int=Cast('price_total', models.IntegerField()))
            .values('customer__code', 'customer__name')
            .annotate(total_price=Sum('price_int'))
            .order_by('-total_price')[:5]
        )
        paginator = Paginator(sale, 24)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        offset = (page_obj.number - 1) * paginator.per_page
        context = {
            "page_obj":page_obj,
            "sale":sale,
            "date":date,
            "top_count":top_count,
            "top_price":top_price,
            "offset":offset,
        }
        return render(request, "store/sale-details.html", context)
    

class ProductListView(PermissionRequiredMixin, views.View):
    login_url = "login"
    permission_required = ["store.view_productmodel"]

    def get(self, request):
        product = ProductModel.objects.all()
        context = {
            "product":product,
        }
        return render(request, "store/product-list.html", context)


class ProductDetailsView(PermissionRequiredMixin, views.View):
    login_url = "signin"
    permission_required = []

    def get(self, request, pid):
        product = get_object_or_404(ProductModel, pk=pid)
        date = DateModel.objects.order_by("-year", "-month", "-day")
        d_3 = date[:3]
        d_7 = date[:7]
        d_30 = date[:30]
        sales_3 = SaleModel.objects.filter(product__pk=pid).filter(date__in=d_3)
        sales_7 = SaleModel.objects.filter(product__pk=pid).filter(date__in=d_7)
        sales_30 = SaleModel.objects.filter(product__pk=pid).filter(date__in=d_30)
        top_count_3 = (
            sales_3
            .annotate(count_int=Cast('count', models.IntegerField()))
            .values('date__year', 'date__month', 'date__day')
            .annotate(total_count=Sum('count_int'))
            .order_by('-total_count')[:10]
        )
        top_price_3 = (
            sales_3
            .annotate(price_int=Cast('price_total', models.IntegerField()))
            .values('customer__code', 'customer__name')
            .annotate(total_price=Sum('price_int'))
            .order_by('-total_price')[:10]
        )
        top_count_7 = (
            sales_7
            .annotate(count_int=Cast('count', models.IntegerField()))
            .values('date__year', 'date__month', 'date__day')
            .annotate(total_count=Sum('count_int'))
            .order_by('-total_count')[:10]
        )
        top_price_7 = (
            sales_7
            .annotate(price_int=Cast('price_total', models.IntegerField()))
            .values('customer__code', 'customer__name')
            .annotate(total_price=Sum('price_int'))
            .order_by('-total_price')[:10]
        )
        top_count_30 = (
            sales_30
            .annotate(count_int=Cast('count', models.IntegerField()))
            .values('date__year', 'date__month', 'date__day')
            .annotate(total_count=Sum('count_int'))
            .order_by('-total_count')[:10]
        )
        top_price_30 = (
            sales_30
            .annotate(price_int=Cast('price_total', models.IntegerField()))
            .values('customer__code', 'customer__name')
            .annotate(total_price=Sum('price_int'))
            .order_by('-total_price')[:10]
        )
        context = {
            "product":product,
            "top_count_3":top_count_3,
            "top_price_3":top_price_3,
            "top_count_7":top_count_7,
            "top_price_7":top_price_7,
            "top_count_30":top_count_30,
            "top_price_30":top_price_30,
        }
        print(top_count_30, top_price_30, sales_30)
        return render(request, "store/product-details.html", context)


COLUMN_MAP = {
    "code": ["كد مشتري", "customer_code", "کد مشتریان"],
    "code_p": ["کد محصولات", "کد محصول", "كد كالا", "کد خدمت", "product_code"],
    "name": ["نام مشتري", "customer_name", "نام و نام خانوادگی"],
    "name_p": ["نام محصول", "مشخصات", "مشخصات محصول", "نام محصولات", "نام کالا", "كالا", "خدمت", "product_name"],
    "count": ["متراژ", "مقدار", "count"],
    "price": ["في", "قیمت", "مبلغ", "price"],
    "price_total": ["مبلغ فروش", "مبلغ کل", "price_total"],
}

def find_column(df, possible_names):
    for col in df.columns:
        col_clean = str(col).strip().replace("\n", "").replace("\r", "")
        if col_clean in possible_names:
            return col_clean
    

class FileUploadView(views.View):
    login_url = ""
    permission_required = []

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
            if str(category) == "sale" or str(category) == "فروش":
                try:
                    date = DateModel.objects.get(day=day, month=month, year=year)
                except DateModel.DoesNotExist:
                    date = DateModel(day=day, month=month, year=year)
                    date.save()
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
                    messages.error(request, "ستون‌های مورد نظر در این فایل پیدا نشدند!")
                    return render(request, "store/file-upload.html", context)
                for _,row in df.iterrows():
                    customer_code = str(int(row[col_code]))
                    customer_name = str(row[col_name])
                    product_code = str(int(row[col_code_p]))
                    product_name = str(row[col_name_p])
                    count = str(row[col_count])
                    price = str(int(row[col_price]))
                    price_total = str(int(row[col_price_total]))
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
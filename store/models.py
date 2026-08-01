from django.db import models
from django.contrib.auth.models import User
from persiantools.jdatetime import JalaliDate

# Create your models here.

def file_directory_path(instance, filename):
    t = t = JalaliDate.today().strftime("%Y/%m/%d/")
    return f"{t}{filename}"


class BaseModel(models.Model):
    user_modified = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='%(class)s_user_modified',
        null=True,
        blank=True,
        verbose_name='کاربر ویرایش'
        )
    user_created = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='%(class)s_user_created',
        null=True,
        blank=True,
        verbose_name='کاربر ایجاد'
        )
    created_date = models.DateTimeField(verbose_name='تاریخ ایجاد', auto_now_add=True)
    modified_date = models.DateTimeField(verbose_name='تاریخ تغییرات', auto_now=True)

    class Meta:
        abstract = True


class DateModel(BaseModel):
    YEAR_ITEMS = {
        "1405":"1405"
    }
    MONTH_ITEMS = {
        "01":"فروردین",
        "02":"اردیبهشت",
        "03":"خرداد",
        "04":"تیر",
        "05":"مرداد",
        "06":"شهریور",
        "07":"مهر",
        "08":"آبان",
        "09":"آذر",
        "10":"دی",
        "11":"بهمن",
        "12":"اسفند",
    }
    DAY_ITEMS = {
        "01":"01",
        "02":"02",
        "03":"03",
        "04":"04",
        "05":"05",
        "06":"06",
        "07":"07",
        "08":"08",
        "09":"09",
        "10":"10",
        "11":"11",
        "12":"12",
        "13":"13",
        "14":"14",
        "15":"15",
        "16":"16",
        "17":"17",
        "18":"18",
        "19":"19",
        "20":"20",
        "21":"21",
        "22":"22",
        "23":"23",
        "24":"24",
        "25":"25",
        "26":"26",
        "27":"27",
        "28":"28",
        "29":"29",
        "30":"30",
        "31":"31",
    }
    year = models.CharField(verbose_name="سال", max_length=4, choices=YEAR_ITEMS)
    month = models.CharField(verbose_name="ماه", max_length=2, choices=MONTH_ITEMS)
    day = models.CharField(verbose_name="روز", max_length=2, choices=DAY_ITEMS)

    def __str__(self):
        return f"{self.year}-{self.month}-{self.day}"
    
    class Meta:
        unique_together = ("year", "month", "day")
        ordering = ["-year", "-month", "-day"]
        verbose_name = "تاریخ"
        verbose_name_plural = "تاریخ‌ها"


class CustomerModel(BaseModel):
    code = models.CharField(verbose_name="کد مشتری", max_length=50, unique=True)
    name = models.CharField(verbose_name="نام و نام خانوادگی", max_length=100)

    def __str__(self):
        return f"{self.code}-{self.name}"
    
    class Meta:
        ordering = ["code"]
        verbose_name = "مشتری"
        verbose_name_plural = "مشتری‌ها"


class ProductModel(BaseModel):
    code = models.CharField(verbose_name="کد محصول", max_length=50, unique=True)
    name = models.CharField(verbose_name="نام محصول", max_length=100)

    def __str__(self):
        return f"{self.code}-{self.name}"
    
    class Meta:
        ordering = ["code"]
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"


class SaleModel(BaseModel):
    date = models.ForeignKey(DateModel, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="تاریخ")
    customer = models.ForeignKey(CustomerModel, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="مشتری")
    product = models.ForeignKey(ProductModel, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="محصول")
    price = models.CharField(verbose_name="قیمت", max_length=18)
    count = models.CharField(verbose_name="مقدار", max_length=18)
    price_total = models.CharField(verbose_name="قیمت", max_length=18)

    def __str__(self):
        if self.date and self.customer and self.product:
            return f"{self.date.year}-{self.date.month}-{self.date.day}-{self.customer.name}-{self.product.name}"
        else:
            return f"{self.pk}"
    
    class Meta:
        unique_together = ("date", "customer", "product", "count", "price")
        ordering = ["-date", "customer"]
        verbose_name = "فروش"
        verbose_name_plural = "فروش‌ها"


class StoreModel(BaseModel):
    date = models.ForeignKey(DateModel, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="تاریخ")
    product = models.ForeignKey(ProductModel, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="محصول")
    sale_group = models.CharField(verbose_name="گروه فروش", max_length=250)
    stock = models.CharField(verbose_name="موجودی", max_length=250)
    in_p = models.CharField(verbose_name="ورودی", max_length=250)
    out_p = models.CharField(verbose_name="خروجی", max_length=250)

    def __str__(self):
        if self.date and self.product:
            return f"{self.date.year}-{self.date.month}-{self.date.day}-{self.product.code}"
        else:
            return f"{self.pk}"
    
    class Meta:
        ordering = ["-date"]
        verbose_name = "انبار"
        verbose_name_plural = "انبارها"


class CategoryFileModel(BaseModel):
    name = models.CharField(verbose_name="عنوان", max_length=250)

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        ordering = ["-created_date"]
        verbose_name = "دسته‌بندی فایل"
        verbose_name_plural = "دسته‌بندی‌های فایل"


class FileModel(BaseModel):
    date = models.ForeignKey(DateModel, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="تاریخ")
    category = models.ForeignKey(CategoryFileModel, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="عنوان")
    file = models.FileField(verbose_name="فایل", upload_to=file_directory_path)

    def __str__(self):
        if self.date and self.category:
            return f"{self.date.year}-{self.date.month}-{self.date.day}--{self.category.name}"
        else:
            return f"{self.pk}"
    
    class Meta:
        ordering = ["-date"]
        verbose_name = "فایل"
        verbose_name_plural = "‌فایل‌ها"
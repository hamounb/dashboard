from django.db import models
from django.contrib.auth.models import User

# Create your models here.

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
    year = models.CharField(verbose_name="سال", max_length=4)
    month = models.CharField(verbose_name="ماه", max_length=2)
    day = models.CharField(verbose_name="روز", max_length=2)

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
        ordering = ["-date"]
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
    file = models.FileField(verbose_name="فایل",)

    def __str__(self):
        if self.date and self.category:
            return f"{self.date.year}-{self.date.month}-{self.date.day}--{self.category.name}"
        else:
            return f"{self.pk}"
    
    class Meta:
        ordering = ["-date"]
        verbose_name = "فایل"
        verbose_name_plural = "‌فایل‌ها"
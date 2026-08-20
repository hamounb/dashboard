from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(DateModel)
class DateAdmin(admin.ModelAdmin):
    readonly_fields = ("user_created", "user_modified", "created_date", "modified_date")
    search_fields = ("year", "month", "day")
    
    def save_model(self, request, obj, form, change):
        if change:
            obj.user_modified = request.user
        else:
            obj.user_created = request.user
            obj.user_modified = request.user
        return super().save_model(request, obj, form, change)
    

@admin.register(CustomerModel)
class CustomerAdmin(admin.ModelAdmin):
    readonly_fields = ("user_created", "user_modified", "created_date", "modified_date")
    search_fields = ("pk", "code", "name")
    list_display = ("pk", "code", "name")
    
    def save_model(self, request, obj, form, change):
        if change:
            obj.user_modified = request.user
        else:
            obj.user_created = request.user
            obj.user_modified = request.user
        return super().save_model(request, obj, form, change)
    

@admin.register(ProductModel)
class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ("user_created", "user_modified", "created_date", "modified_date")
    search_fields = ("code", "name")
    
    def save_model(self, request, obj, form, change):
        if change:
            obj.user_modified = request.user
        else:
            obj.user_created = request.user
            obj.user_modified = request.user
        return super().save_model(request, obj, form, change)
    

@admin.register(SaleModel)
class SaleAdmin(admin.ModelAdmin):
    readonly_fields = ("user_created", "user_modified", "created_date", "modified_date")
    search_fields = ("date__year", "date__month", "date__day", "customer__code", "product__code", "price_total")
    list_display = ("pk", "date", "customer", "product")
    
    def save_model(self, request, obj, form, change):
        if change:
            obj.user_modified = request.user
        else:
            obj.user_created = request.user
            obj.user_modified = request.user
        return super().save_model(request, obj, form, change)
    

@admin.register(StoreModel)
class StoreAdmin(admin.ModelAdmin):
    readonly_fields = ("user_created", "user_modified", "created_date", "modified_date")
    search_fields = ("date", "product", "sale_group")
    
    def save_model(self, request, obj, form, change):
        if change:
            obj.user_modified = request.user
        else:
            obj.user_created = request.user
            obj.user_modified = request.user
        return super().save_model(request, obj, form, change)
    

@admin.register(CategoryFileModel)
class CategoryFileAdmin(admin.ModelAdmin):
    readonly_fields = ("user_created", "user_modified", "created_date", "modified_date")
    search_fields = ("name", )
    
    def save_model(self, request, obj, form, change):
        if change:
            obj.user_modified = request.user
        else:
            obj.user_created = request.user
            obj.user_modified = request.user
        return super().save_model(request, obj, form, change)
    

@admin.register(FileModel)
class FileAdmin(admin.ModelAdmin):
    readonly_fields = ("user_created", "user_modified", "created_date", "modified_date")
    search_fields = ("date", "category")
    list_display = ("pk", "date", "category")
    
    def save_model(self, request, obj, form, change):
        if change:
            obj.user_modified = request.user
        else:
            obj.user_created = request.user
            obj.user_modified = request.user
        return super().save_model(request, obj, form, change)
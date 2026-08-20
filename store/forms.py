from django import forms
from .models import CategoryFileModel, DateModel
from persiantools import jdatetime


class FileUploadForm(forms.Form):
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
    day = forms.CharField(label="روز", widget=forms.Select(attrs={"class":"form-select", "placeholder":"selected"}, choices=DAY_ITEMS))
    month = forms.CharField(label="ماه", widget=forms.Select(attrs={"class":"form-select"}, choices=MONTH_ITEMS))
    year = forms.CharField(label="سال", widget=forms.Select(attrs={"class":"form-select"}, choices=YEAR_ITEMS))
    category = forms.ModelChoiceField(label="عنوان فایل", widget=forms.Select(attrs={"class":"form-select"}), queryset=CategoryFileModel.objects.all())
    file = forms.FileField(label="فایل", widget=forms.FileInput(attrs={"class":"form-control"}))


class DateSelectForm(forms.Form):
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
    day = forms.CharField(label="روز", widget=forms.Select(attrs={"class":"form-select", "placeholder":"selected"}, choices=DAY_ITEMS))
    month = forms.CharField(label="ماه", widget=forms.Select(attrs={"class":"form-select"}, choices=MONTH_ITEMS))
    year = forms.CharField(label="سال", widget=forms.Select(attrs={"class":"form-select"}, choices=YEAR_ITEMS))


class ProductSearchForm(forms.Form):
    text = forms.CharField(label="کالا", widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"نام یا کد کالا"}), required=False)
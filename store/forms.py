from django import forms
from .models import *


class FileUploadForm(forms.ModelForm):

    class Meta:
        model = FileModel
        fields = ["date", "category", "file"]


class DurationForm(forms.Form):
    YEAR_ITEMS = {
        "1405":"1405"
    }
    MONTH_ITEMS = {
        "1":"فروردین",
        "2":"اردیبهشت",
        "3":"خرداد",
        "4":"تیر",
        "5":"مرداد",
        "6":"شهریور",
        "7":"مهر",
        "8":"آبان",
        "9":"آذر",
        "10":"دی",
        "11":"بهمن",
        "12":"اسفند",
    }
    DAY_ITEMS = {
        "1":"1",
        "2":"2",
        "3":"3",
        "4":"4",
        "5":"5",
        "6":"6",
        "7":"7",
        "8":"8",
        "9":"9",
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
    start_day = forms.CharField(label="روز", widget=forms.Select(attrs={"class":"form-select"}, choices=DAY_ITEMS))
    start_month = forms.CharField(label="ماه", widget=forms.Select(attrs={"class":"form-select"}, choices=MONTH_ITEMS))
    start_year = forms.CharField(label="سال", widget=forms.Select(attrs={"class":"form-select"}, choices=YEAR_ITEMS))
    end_day = forms.CharField(label="روز", widget=forms.Select(attrs={"class":"form-select"}, choices=DAY_ITEMS))
    end_month = forms.CharField(label="ماه", widget=forms.Select(attrs={"class":"form-select"}, choices=MONTH_ITEMS))
    end_year = forms.CharField(label="سال", widget=forms.Select(attrs={"class":"form-select"}, choices=YEAR_ITEMS))
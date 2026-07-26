from django.shortcuts import render
from django import views

# Create your views here.

class MainView(views.View):

    def get(self, request):
        return render(request, "main/main.html")
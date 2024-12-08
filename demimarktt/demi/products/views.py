from django.shortcuts import render
from django.http import HttpResponse

def homepage(request):
    return HttpResponse("Anasayfa")

def about(request):
    return  HttpResponse("Hakkımızda")

def contact(request):
    return HttpResponse("İletişim")


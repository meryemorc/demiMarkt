from django.shortcuts import render # type: ignore
from django.http import HttpResponse # type: ignore

def homepage(request):
  return render(request, 'homepage/homepage.html')

def about(request):
    return  HttpResponse("Hakkımızda")

def contact(request):
    return HttpResponse("İletişim")

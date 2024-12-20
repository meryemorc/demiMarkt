from django.urls import path # type: ignore
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('about/', views.about, name='about'),
    path('contact/',views.contact,name='contact'),
    path('profile/', views.profile_view, name='profile'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_file, name='upload_file'),
    path('', views.home, name='home'),
    path('certificates/', views.certificate_list, name='certificate_list'),
]
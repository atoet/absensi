from django.urls import path
from . import views

urlpatterns = [
    path('', views.cek_login, name='cek_login'),
    path('home', views.home, name='home'),    
    path('data_absensi', views.data_absensi, name='data_absensi'),  
    path('detail/<id_karyawan>', views.detail, name='detail'),    
    path('delete/<id>/<id_karyawan>/<status>', views.delete, name='delete'), 
]
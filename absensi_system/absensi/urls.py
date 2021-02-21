from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('absensi/', include('absensi_app.urls')),
    path('', auth_views.LoginView.as_view(template_name='absensi_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='absensi_app/login.html'), name='logout'),
]
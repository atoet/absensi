from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from datetime import date, datetime 
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from .models import Level, HakAkses, StatusAbsen, Karyawan, Absensi


def cek_login(request):
    send_email = request.POST.get('email')
    send_password = request.POST.get('password')
    user = authenticate(email=send_email, password=send_password)

    if user is not None:
        login(request, user)
        return redirect('home')
    else:
        messages.error(request, 'Username atau password yang Anda input, Salah' )
        return render(request, 'absensi_app/login.html')    


    

@login_required
def home(request):

    akses = HakAkses.objects.get(user_id=request.user.id)
    level = akses.level_id
    tgl = datetime.now()

    if level == 1:
        
        karyawan = Karyawan.objects.all()

        data = {
            'nama' : 'Admin',
            'level': level,
            'karyawan' : karyawan,
            'tgl' : tgl,
        }
    else:
        try:
            karyawan = Karyawan.objects.get(user_id=request.user.id)
            absensi = Absensi.objects.filter(karyawan_id=karyawan.id)

            count_absensi = Absensi.objects.filter(karyawan_id=karyawan.id).count()

            data = {
                'id' : karyawan.id,
                'nama' : karyawan.nama,
                'data_absen' : absensi,
                'count' : count_absensi,
                'level' : level,
                'tgl' : tgl,
            }
        except ObjectDoesNotExist:
            pass    
    
    return render(request, 'absensi_app/home.html', data)


@login_required
def data_absensi(request):

    id_karyawan = request.POST.get('karyawan')
    data_status = request.POST.get('status')
    hari_ini = date.today()

    karyawan = Karyawan.objects.get(id=id_karyawan)
    status = StatusAbsen.objects.get(id=data_status)

    absen_today = Absensi.objects.filter(karyawan=karyawan, date=hari_ini, status=status).count()

    print(data_status)

    if absen_today >= 1:
        if data_status == "1":
            messages.error(request, 'Anda telah melakukan absen masuk hari ini.' )
        else:
            messages.error(request, 'Anda telah melakukan absen keluar hari ini.' )
    else:

        data_absen = Absensi(
            karyawan = karyawan,
            status = status,            
        )
        
        data_absen.save()
    return redirect('home')    


@login_required
def detail(request, id_karyawan):

    akses = HakAkses.objects.get(user_id=request.user.id)
    level = akses.level_id
    tgl = datetime.now()
    

    if level == 1:
        karyawan = Karyawan.objects.get(id=id_karyawan)
        absensi = Absensi.objects.filter(karyawan_id=karyawan.id)

        count_absensi = Absensi.objects.filter(karyawan_id=karyawan.id).count()

        data = {
            'user' : 'Admin',
            'nama' : karyawan.nama,
            'data_absen' : absensi,
            'count' : count_absensi,
            'level' : level,
            'tgl' : tgl,
        }
    else:
        return redirect('home')    
    
    return render(request, 'absensi_app/detail.html', data)


@login_required
def delete(request, id, id_karyawan, status):

    absensi = Absensi.objects.get(id=id)
    tanggal = absensi.date
    
    if status == '1':
        data_absensi = Absensi.objects.filter(karyawan_id=id_karyawan, date=tanggal)
        data_absensi.delete()
    else:
        data_absensi = Absensi.objects.get(id=id)
        data_absensi.delete()

    return redirect('detail', id_karyawan=id_karyawan)
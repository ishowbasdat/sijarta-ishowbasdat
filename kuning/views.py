from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection
from datetime import date, datetime
from decimal import Decimal
import uuid

# Create your views here.
def landing(request):
    return render(request, 'landing.html')

def login(request):
    if request.method == 'POST':
        no_hp = request.POST.get('no_hp')
        pwd = request.POST.get('pwd')
        
        with connection.cursor() as cursor:
            cursor.execute("""
                            SELECT U.*,
                            CASE
                                WHEN EXISTS (SELECT 1 FROM SIJARTA.PELANGGAN WHERE id = U.id) THEN 'PELANGGAN'
                                WHEN EXISTS (SELECT 1 FROM SIJARTA.PEKERJA WHERE id = U.id) THEN 'PEKERJA'
                            END AS role
                            FROM SIJARTA."USER" AS U
                            WHERE U.no_hp = %s
                           """, [no_hp])
            
            row = cursor.fetchone()
            if row:
                user = dict(zip([column[0] for column in cursor.description], row))
                
                for key, value in user.items():
                    if isinstance(value, (date, datetime)):
                        user[key] = value.isoformat()
                    elif isinstance(value, uuid.UUID):
                        user[key] = str(value)
                    elif isinstance(value, Decimal):
                        user[key] = float(value)    
            else:
                user = None
            
            if user and pwd == user.get('pwd'):
                request.session['user'] = user
                if user.get('role') == 'PEKERJA':
                    cursor.execute("""
                                   SELECT * FROM SIJARTA.PEKERJA WHERE id = %s
                                   """, [user.get('id')])
                    row = cursor.fetchone()
                    pekerja = dict(zip([column[0] for column in cursor.description], row))
                    request.session['user']['nama_bank'] = pekerja.get('nama_bank')
                    request.session['user']['nomor_rekening'] = pekerja.get('nomor_rekening')
                    request.session['user']['npwp'] = pekerja.get('npwp')
                    request.session['user']['link_foto'] = pekerja.get('link_foto')
                    request.session['user']['rating'] = pekerja.get('rating')
                    request.session['user']['jml_pesanan_selesai'] = pekerja.get('jml_pesanan_selesai')
                    
                request.session.save()
                print(request.session['user'].get('role'))
                return redirect('kuning:landing')
            else:
                messages.error(request, 'No HP atau Password salah')
                return redirect('kuning:login')
                # TODO: Tunggu chris, redirect ke homepage
                
            # TODO: Kalau ga ketemu, tunjukin error msg
            
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        id = uuid.uuid4()
        nama = request.POST.get('nama')
        jenis_kelamin = request.POST.get('jenis_kelamin')
        no_hp = request.POST.get('no_hp')
        pwd = request.POST.get('pwd')
        tgl_lahir = request.POST.get('tgl_lahir')
        alamat = request.POST.get('alamat')
        role = request.POST.get('role')
        
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 1 FROM SIJARTA."USER" WHERE no_hp = %s
            """, [no_hp])
            
            if cursor.fetchone():
                messages.error(request, 'Nomor HP telah terdaftar')
                return redirect('kuning:login')
            
            cursor.execute("""
                           INSERT INTO SIJARTA."USER" (id, nama, jenis_kelamin, no_hp, pwd, tgl_lahir, alamat)
                           VALUES (%s, %s, %s, %s, %s, %s, %s)
                           """, [id, nama, jenis_kelamin, no_hp, pwd, tgl_lahir, alamat])
            
            if role == 'PELANGGAN':
                cursor.execute("""
                               INSERT INTO SIJARTA.PELANGGAN (id, level)
                               VALUES (%s, 'Basic')
                               """, [id])
                
            elif role == 'PEKERJA':
                nama_bank = request.POST.get('nama_bank')
                nomor_rekening = request.POST.get('nomor_rekening')
                npwp = request.POST.get('npwp')
                link_foto = request.POST.get('link_foto')
                cursor.execute("""
                               INSERT INTO SIJARTA.PEKERJA (id, nama_bank, nomor_rekening, npwp, link_foto)
                                 VALUES (%s, %s, %s, %s, %s)
                               """, [id, nama_bank, nomor_rekening, npwp, link_foto])
        return redirect('kuning:login')
    return render(request, 'register.html')

def profile(request):
    if 'user' not in request.session:
        return redirect('kuning:login')
    
    id = request.session['user'].get('id')
    role = request.session['user'].get('role')
    
    if request.method == 'POST':
        nama = request.POST.get('nama')
        jenis_kelamin = request.POST.get('jenis_kelamin')
        no_hp = request.POST.get('no_hp')
        tanggal_lahir = request.POST.get('tanggal_lahir')
        alamat = request.POST.get('alamat')
        
        with connection.cursor() as cursor:
            cursor.execute("""
                           UPDATE SIJARTA."USER"
                           SET nama = %s, jenis_kelamin = %s, no_hp = %s, tanggal_lahir = %s, alamat = %s
                           where id = %s
                           """, [nama, jenis_kelamin, no_hp, tanggal_lahir, alamat, id])
            
            if role == 'PEKERJA':
                nama_bank = request.POST.get('nama_bank')
                nomor_rekening = request.POST.get('nomor_rekening')
                npwp = request.POST.get('npwp')
                link_foto = request.POST.get('link_foto')
                cursor.execute("""
                               UPDATE SIJARTA.PEKERJA
                               SET nama_bank = %s, nomor_rekening = %s, npwp = %s, link_foto = %s
                               WHERE id = %s
                               """, [nama_bank, nomor_rekening, npwp, link_foto, id])
                
        return redirect('kuning:profile')              
    return render(request, 'profile.html')

def logout(request):
    request.session.flush()
    return redirect('kuning:login')
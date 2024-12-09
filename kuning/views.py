from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection, transaction
from datetime import date, datetime
from decimal import Decimal
import uuid
import django

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
                request.session.save()
                print(request.session['user'].get('role'))
                return redirect('kuning:landing')
            else:
                print('Error')
                # TODO: Tunggu chris, redirect ke homepage
                
            # TODO: Kalau ga ketemu, tunjukin error msg
            
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        try:
            with transaction.atomic():
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
                                INSERT INTO SIJARTA."USER" (id, nama, jenis_kelamin, no_hp, pwd, tgl_lahir, alamat, saldo_mypay)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, 0)
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
                                    INSERT INTO SIJARTA.PEKERJA (id, nama_bank, nomor_rekening, npwp, link_foto, rating, jml_pesanan_selesai)
                                        VALUES (%s, %s, %s, %s, %s, 0, 0)
                                    """, [id, nama_bank, nomor_rekening, npwp, link_foto])
                                    
        except django.db.utils.InternalError as e:
            if "Nomor HP" in str(e):
                messages.error(request, 'No HP sudah terdaftar')
                return redirect('kuning:login')
            else:
                messages.error(request, 'Terjadi kesalahan')
                return redirect('kuning:register')
        
        except Exception as e:
            messages.error(request, f'Terjadi kesalahan')
            return redirect('kuning:register')
        
        messages.success(request, 'Pendaftaran berhasil!')
        return redirect('kuning:login')
        
    return render(request, 'register.html')

def profile(request):
    if 'id' not in request.session:
        return redirect('login')
    
    id = request.session.user.get('id')
    role = request.session.user.get('role')
    
    if request.method == 'POST':
        nama = request.POST.get('nama')
        jenis_kelamin = request.POST.get('jenis_kelamin')
        no_hp = request.POST.get('no_hp')
        tanggal_lahir = request.POST.get('tanggal_lahir')
        alamat = request.POST.get('alamat')
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                            UPDATE SIJARTA."USER"
                            SET nama = %s, jenis_kelamin = %s, no_hp = %s, tgl_lahir = %s, alamat = %s
                            where id = %s
                            """, [nama, jenis_kelamin, no_hp, tgl_lahir, alamat, id])
                
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
                    
        except django.db.utils.InternalError as e:
            if "Nomor HP" in str(e):
                messages.error(request, 'No HP sudah terdaftar')
                return redirect('kuning:profile')
            else:
                messages.error(request, 'Terjadi kesalahan')
                return redirect('kuning:profile')
        
        except Exception as e:
            messages.error(request, f'Terjadi kesalahan')
            return redirect('kuning:profile')
        
        request.session['user']['nama'] = nama
        request.session.save()
        return redirect('kuning:profile') 
    return render(request, 'profile.html', {'user_data': user_data})

def logout(request):
    request.session.flush()
    return redirect('kuning:login')
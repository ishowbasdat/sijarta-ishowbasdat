from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection
from datetime import date, datetime
from decimal import Decimal
import uuid

# Create your views here.
def landing(request):
    if 'user' in request.session:
        return redirect('hijau:homepage')
    
    return render(request, 'landing.html')

def login(request):
    if 'user' in request.session:
        return redirect('hijau:homepage')
    
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
                user_data = dict(zip([column[0] for column in cursor.description], row))
                user = {
                    key: user_data[key] for key in user_data.keys() if key in ['id', 'nama', 'role', 'saldo_mypay']
                }
                
                if isinstance(user.get('id'), uuid.UUID):
                    user['id'] = str(user.get('id'))
                if isinstance(user.get('saldo_mypay'), Decimal):
                    user['saldo_mypay'] = float(user.get('saldo_mypay'))
            else:
                user = None

            if user and pwd == user_data.get('pwd'):
                request.session['user'] = user
                request.session.save()
                return redirect('hijau:homepage')
            else:
                messages.error(request, 'No HP atau Password salah')
                return redirect('kuning:login')
                
    return render(request, 'login.html')

def register(request):
    if 'user' in request.session:
        return redirect('hijau:homepage')
    
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
            
            # TODO: Cek kombinasi nama_bank dan nomor rekening, serta NPWP unik - perlu dihandle ga?
            
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
        return redirect('kuning:login')
    return render(request, 'register.html')

# TODO: Cehck butuh ga tombol update, handle corner case juga
def profile(request):
    if 'user' not in request.session:
        return redirect('kuning:login')
    
    id = request.session['user'].get('id')
    role = request.session['user'].get('role')
    
    with connection.cursor() as cursor:
        cursor.execute("""
                       SELECT U.* FROM SIJARTA."USER" AS U WHERE U.id = %s
                       """, [id])
        row = cursor.fetchone()
        
        if row:
            user_data = dict(zip([column[0] for column in cursor.description], row))
            if isinstance(user_data.get('tgl_lahir'), (date, datetime)):
                user_data['tgl_lahir'] = user_data.get('tgl_lahir').strftime('%d-%m-%Y')
                
            if role == 'PELANGGAN':
                cursor.execute("""
                               SELECT * FROM SIJARTA.PELANGGAN WHERE id = %s
                               """, [id])
                row = cursor.fetchone()
                pelanggan_data = dict(zip([column[0] for column in cursor.description], row))
                pelanggan_data.pop('id', None)
                user_data.update(pelanggan_data)
                
            elif role == 'PEKERJA':
                cursor.execute("""
                               SELECT * FROM SIJARTA.PEKERJA WHERE id = %s
                               """, [id])
                row = cursor.fetchone()
                pekerja_data = dict(zip([column[0] for column in cursor.description], row))
                pekerja_data.pop('id', None)
                user_data.update(pekerja_data)
                
                cursor.execute("""
                               SELECT KJ.nama_kategori
                               FROM SIJARTA.KATEGORI_JASA AS KJ
                               JOIN SIJARTA.PEKERJA_KATEGORI_JASA AS PKJ
                               ON KJ.id = PKJ.kategori_jasa_id
                               WHERE PKJ.pekerja_id = %s
                               """, [id])
                rows = cursor.fetchall()
                user_data['kategori_jasa'] = [
                    {
                        'nama_kategori': row[0]
                    }
                    
                    for row in rows
                ]
           
    if request.method == 'POST':
        nama = request.POST.get('nama')
        jenis_kelamin = request.POST.get('jenis_kelamin')
        no_hp = request.POST.get('no_hp')
        tgl_lahir = request.POST.get('tgl_lahir')
        alamat = request.POST.get('alamat')
        
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
        
        request.session['user']['nama'] = nama
        request.session.save()
        return redirect('kuning:profile') 
    return render(request, 'profile.html', {'user_data': user_data})

def logout(request):
    request.session.flush()
    return redirect('kuning:landing')
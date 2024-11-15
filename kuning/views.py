from django.shortcuts import render, redirect
from django.db import connection
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
                           SELECT U.id, U.pwd,
                           CASE
                                WHEN P.level IS NOT NULL THEN 'PELANGGAN'
                                WHEN PEL.id IS NOT NULL THEN 'PEKERJA'
                            END AS role
                            FROM SIJARTA."USER" AS U
                            LEFT JOIN SIJARTA.PELANGGAN AS PEL ON U.id = P.id
                            LEFT JOIN SIJARTA.PEKERJA AS PEK ON U.id = PEK.id
                            WHERE U.no_hp = %s
                           """, [no_hp])
            user = cursor.fetchone()
            
            if user and pwd == user[1]:
                request.session['id'] = str(user[0])
                request.session['role'] = user[2]
                return redirect('profile')
            
    return render(request, 'login.html')

def register_role(request):
    if request.method == 'POST':
        role = request.POST.get('role')
        return redirect('register', role = role)
    return render(request, 'register_role.html')

def register(request, role):
    if request.method == 'POST':
        id = uuid.uuid4()
        nama = request.POST.get('nama')
        jenis_kelamin = request.POST.get('jenis_kelamin')
        no_hp = request.POST.get('no_hp')
        pwd = request.POST.get('pwd')
        tgl_lahir = request.POST.get('tgl_lahir')
        alamat = request.POST.get('alamat')
        
        with connection.cursor() as cursor:
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
        return redirect('login')
    return render(request, 'register.html', {'role': role})

def profile(request):
    if 'id' not in request.session:
        return redirect('login')
    
    id = request.session.get('id')
    role = request.session.get('role')
    
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
    # TODO: Jangan lupa implement fetch data untuk user
    # Tambah juga parameter pada render                     
    return render(request, 'profile.html')

def logout(request):
    request.session.flush()
    return redirect('login')
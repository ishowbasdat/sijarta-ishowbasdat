from django.shortcuts import render
from django.db import connection
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, HttpResponseBadRequest
import json

@require_http_methods(["GET", "POST"])
def homepage(request):
    category = request.GET.get('category')
    subcategory = request.GET.get('subcategory')
    if category == None or category == "":
        category = None
    if subcategory == None or subcategory == "":
        subcategory = '%'
    else:
        subcategory = f"%{subcategory}%"
    
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT *
            FROM SIJARTA.KATEGORI_JASA, SIJARTA.SUBKATEGORI_JASA
            WHERE SIJARTA.KATEGORI_JASA.id = SIJARTA.SUBKATEGORI_JASA.kategori_jasa_id
            AND (%s is NULL OR SIJARTA.KATEGORI_JASA.nama_kategori = %s)
            AND LOWER(SIJARTA.SUBKATEGORI_JASA.nama_subkategori) LIKE LOWER(%s)
        """, [category, category, subcategory])
        
        data = [dict(zip([ column[0] for column in cursor.description ], row)) for row in cursor.fetchall()]
        cursor.execute("SELECT * FROM SIJARTA.KATEGORI_JASA")
        categories = [dict(zip([ column[0] for column in cursor.description ], row)) for row in cursor.fetchall()]
    
    context = {
        'data': data,
        'categories': categories
    }
    return render(request, 'homepage.html', context)

@require_http_methods(["GET"])
def subkategori(request, id):
    
    # Dummy session
    request.session['user'] = {
        'id': 'ce820534-45af-4871-9d91-4da9e52dc988',
        'nama': 'Christian Raphael Heryanto',
        'jenis_kelamin': 'L',
        'no_hp': '081213151719',
        'pwd': 'ThisIsMyPasswordDontHackMePls',
        'tgl_lahir': '2005-01-01',
        'alamat': 'Jalan Haji Kukusan',
        'saldo_mypay': 200000.00,
        'role': 'PEKERJA'
    }
    
    if request.session['user'] is None:
        return redirect('homepage')
    
    with connection.cursor() as cursor:
        cursor.execute("""
                       SELECT * 
                       FROM SIJARTA.SUBKATEGORI_JASA, SIJARTA.SESI_LAYANAN, SIJARTA.KATEGORI_JASA
                       WHERE SIJARTA.SUBKATEGORI_JASA.id = %s
                       AND SIJARTA.KATEGORI_JASA.id = SIJARTA.SUBKATEGORI_JASA.kategori_jasa_id
                       AND SIJARTA.SUBKATEGORI_JASA.id = SIJARTA.SESI_LAYANAN.subkategori_id
                       """, [id])
        subcategory = [dict(zip([ column[0] for column in cursor.description ], row)) for row in cursor.fetchall()]
        
        cursor.execute("""
                       SELECT * 
                       FROM SIJARTA.PEKERJA, SIJARTA.PEKERJA_KATEGORI_JASA, SIJARTA.SUBKATEGORI_JASA, SIJARTA.KATEGORI_JASA, SIJARTA."USER"
                       WHERE SIJARTA.SUBKATEGORI_JASA.id = %s
                       AND SIJARTA.SUBKATEGORI_JASA.kategori_jasa_id = SIJARTA.KATEGORI_JASA.id
                       AND SIJARTA.PEKERJA_KATEGORI_JASA.kategori_jasa_id = SIJARTA.KATEGORI_JASA.id
                       AND SIJARTA.PEKERJA_KATEGORI_JASA.pekerja_id = SIJARTA.PEKERJA.id
                       AND SIJARTA.PEKERJA.id = SIJARTA."USER".id
                       """, [id])
        pekerja = [dict(zip([ column[0] for column in cursor.description ], row)) for row in cursor.fetchall()]
        
    if subcategory is None:
        return redirect('homepage')
    
    context = {'subkategori' : subcategory, 'pekerja' : pekerja}
    return render(request, 'subkategori.html', context)

@require_http_methods(["GET"])
def get_metode_pembayaran(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM SIJARTA.METODE_BAYAR")
        data = [dict(zip([ column[0] for column in cursor.description ], row)) for row in cursor.fetchall()]
    return JsonResponse(data, safe=False)

@require_http_methods(["POST"])
def validate_discount(request):
    data = json.loads(request.body)
    kode = data['kode']
    transaksi = data['transaksi']
    with connection.cursor() as cursor:
        cursor.execute("""SELECT * 
                       FROM SIJARTA.DISKON d
                       LEFT JOIN SIJARTA.VOUCHER v ON d.kode = v.kode
                       LEFT JOIN SIJARTA.PROMO p ON d.kode = p.kode
                       WHERE d.kode = %s AND
                       d.potongan >= 0 AND
                       d.min_tr_pemesanan <= %s AND
                       (v.kuota_PELANGGANan IS NULL OR v.kuota_PELANGGANan > 0) AND
                       (v.jml_hari_berlaku IS NULL OR v.jml_hari_berlaku > 0) AND
                       (p.tgl_akhir_berlaku IS NULL OR p.tgl_akhir_berlaku >= CURRENT_DATE)
                       """, [kode, transaksi])
        row = cursor.fetchone()
        data = dict(zip([column[0] for column in cursor.description], row)) if row else None

    if len(data) == 0:
        return JsonResponse({'valid': False})
    return JsonResponse({'valid': True, 'potongan': data['potongan']})

@require_http_methods(["POST"])
def create_order(request):
    if request.session['user']['role'] != 'PELANGGAN':
        return HttpResponseBadRequest()
    # TODO: implement this function with raw query
    json.loads(request.body)
    return JsonResponse({'success': True})

@require_http_methods(["GET"])
def pesanan(request):
    
    # Dummy session
    request.session['user'] = {
        'id': 'ce820534-45af-4871-9d91-4da9e52dc988',
        'nama': 'Christian Raphael Heryanto',
        'jenis_kelamin': 'L',
        'no_hp': '081213151719',
        'pwd': 'ThisIsMyPasswordDontHackMePls',
        'tgl_lahir': '2005-01-01',
        'alamat': 'Jalan Haji Kukusan',
        'saldo_mypay': 200000.00,
        'role': 'PELANGGAN'
    }
    
    if request.session['user']['role'] != 'PELANGGAN':
        return HttpResponseBadRequest()

    with connection.cursor() as cursor:
        cursor.execute("""
                        SELECT *
                        FROM SIJARTA.TR_PEMESANAN_JASA tpj
                        LEFT JOIN SIJARTA.TR_PEMESANAN_STATUS tps ON tpj.id = tps.id_tr_pemesanan
                        LEFT JOIN SIJARTA.STATUS_PESANAN sp ON tps.id_status = sp.id
                        LEFT JOIN SIJARTA.SESI_LAYANAN sl ON (tpj.id_kategori_jasa, tpj.sesi) = (sl.subkategori_id, sl.sesi)
                        LEFT JOIN SIJARTA.SUBKATEGORI_JASA sj ON sl.subkategori_id = sj.id
                        LEFT JOIN SIJARTA.PEKERJA p ON tpj.id_pekerja = p.id
                        LEFT JOIN SIJARTA."USER" u ON p.id = u.id
                        WHERE tpj.id_pelanggan = %s;
                       """, [request.session['user']['id']])
        data = [dict(zip([ column[0] for column in cursor.description ], row)) for row in cursor.fetchall()]
        
        cursor.execute("""
                       SELECT * FROM SIJARTA.SUBKATEGORI_JASA
                       """)
        subcategories = [dict(zip([ column[0] for column in cursor.description ], row)) for row in cursor.fetchall()]
        
        cursor.execute("""
                       SELECT * FROM SIJARTA.STATUS_PESANAN
                       """)
        status = [dict(zip([ column[0] for column in cursor.description ], row)) for row in cursor.fetchall()]
    return render(request, 'pesanan.html', {'data': data, 'subcategories': subcategories, 'status': status})
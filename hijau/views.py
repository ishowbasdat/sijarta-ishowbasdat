from datetime import datetime
from decimal import Decimal, InvalidOperation
from django.shortcuts import render
from django.db import connection, DatabaseError
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, HttpResponseBadRequest
from kuning.views import landing
from django.contrib import messages
import json
import uuid

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

@require_http_methods(["GET", "POST"])
def subkategori(request, id):
    
    landing(request) #redirect back to profile if not logged in 
    
    if request.method == 'POST':
        if request.session['user']['role'] != 'PEKERJA':
            return HttpResponseForbidden("Only workers can join categories")
        try:
            data = json.loads(request.body)
            kategori_jasa_id = data.get('kategori')
            
            if not kategori_jasa_id:
                return HttpResponseBadRequest("Invalid data: 'kategori' is required")
            
            pekerja_id = request.session['user']['id']
            
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO pekerja_kategori_jasa (pekerja_id, kategori_jasa_id)
                    VALUES (%s, %s)
                """, [pekerja_id, kategori_jasa_id])
            return JsonResponse({'status': 'success'})
        
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON data")
        
        except Exception as e:
            return HttpResponseBadRequest(f"An error occurred: {str(e)}")

    elif request.method == "GET":
        with connection.cursor() as cursor:
            # Get all details required regarding the subcategory
            cursor.execute("""
                        SELECT * 
                        FROM SIJARTA.SUBKATEGORI_JASA, SIJARTA.SESI_LAYANAN, SIJARTA.KATEGORI_JASA
                        WHERE SIJARTA.SUBKATEGORI_JASA.id = %s
                        AND SIJARTA.KATEGORI_JASA.id = SIJARTA.SUBKATEGORI_JASA.kategori_jasa_id
                        AND SIJARTA.SUBKATEGORI_JASA.id = SIJARTA.SESI_LAYANAN.subkategori_id
                        """, [id])
            subcategory = [dict(zip([ column[0] for column in cursor.description ], row)) for row in cursor.fetchall()]
            
            # Get all pekerja that can do the job (I'll create another endpoint for this for fetch)
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
            
            
            cursor.execute("""
                        SELECT 
                                CASE 
                                    WHEN COUNT(*) = 0 THEN false 
                                    ELSE true 
                                END AS has_joined 
                            FROM pekerja_kategori_jasa 
                            WHERE pekerja_id = %s 
                            AND kategori_jasa_id = %s
                        """, [request.session['user']['id'], subcategory[0]['kategori_jasa_id']])
            
            is_joined = cursor.fetchone()[0]
            
        if subcategory is None:
            return redirect('homepage')
        #print role
        context = {'subkategori' : subcategory, 'pekerja' : pekerja, 'is_joined' : is_joined}
        return render(request, 'subkategori.html', context)

@require_http_methods(["GET"])
def get_metode_pembayaran(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM SIJARTA.METODE_BAYAR")
        data = [dict(zip([ column[0] for column in cursor.description ], row)) for row in cursor.fetchall()]
    return JsonResponse(data, safe=False)

@require_http_methods(["POST"])
def create_order(request):
    
    if request.session['user']['role'] != 'PELANGGAN':
        return HttpResponseBadRequest("Only 'PELANGGAN' role can create an order.")
   
    data = json.loads(request.body)

    try:
        # Validate required fields
        required_fields = ['orderDate', 'kategori_jasa_id', 'sesi', 'totalPayment', 'paymentMethod']
        for field in required_fields:
            if not data.get(field):
                return JsonResponse({'success': False, 'error': f'Missing required field: {field}'}, status=400)

        # Convert total payment to decimal
        total_biaya = Decimal(data.get('totalPayment').replace('Rp ', '').replace('.', '').replace(',', ''))

        # check whether the date is in the future
        if datetime.strptime(data.get('orderDate'), '%Y-%m-%d') < datetime.now():
            return JsonResponse({'success': False, 'error': 'Order date must be in the future'}, status=400)
        
        # Prepare discount code (convert empty string to None)
        discount_code = data.get('discountCode') or None

        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO SIJARTA.TR_PEMESANAN_JASA
                (id, tgl_pemesanan, tgl_pekerjaan, waktu_pekerjaan, total_biaya, 
                id_pelanggan, id_pekerja, id_kategori_jasa, sesi, id_diskon, id_metode_bayar)
                VALUES (%s, %s, NULL, NULL, %s, %s, NULL, %s, %s, %s, %s)
                """, [
                    uuid.uuid4(),
                    data.get('orderDate'),  # tgl_pemesanan
                    total_biaya,  # total_biaya
                    request.session['user']['id'],  # id_pelanggan
                    data.get('kategori_jasa_id'),  # id_kategori_jasa
                    int(data.get('sesi')),  # sesi (converted to integer)
                    discount_code,  # id_diskon
                    data.get('paymentMethod')  # id_metode_bayar
                ])
            
            cursor.execute("""
                INSERT INTO SIJARTA.TR_PEMESANAN_STATUS
                (id_tr_pemesanan, id_status, tgl_waktu)
                VALUES ((SELECT id FROM SIJARTA.TR_PEMESANAN_JASA WHERE id_pelanggan = %s ORDER BY tgl_pemesanan DESC LIMIT 1), 
                        (SELECT id FROM SIJARTA.STATUS_PESANAN WHERE status = 'Menunggu Pembayaran'), %s)
                """, [request.session['user']['id'], datetime.now()])
        return JsonResponse({'success': True})
    except (DatabaseError, InvalidOperation, ValueError) as e:
        # Log the error for debugging
        print(f"Error creating order: {e}")
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

@require_http_methods(["GET"])
def pesanan(request):   
    subcategory = request.GET.get('subcategory')
    status = request.GET.get('status')
    if subcategory == None or subcategory == "":
        subcategory = '%'
    else:
        subcategory = f"%{subcategory}%"
    if status == None or status == "":
        status = '%'
    else:
        status = f"%{status}%"
        
    if request.session['user']['role'] != 'PELANGGAN':
        return redirect('homepage')

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
                        WHERE tpj.id_pelanggan = %s
                        AND LOWER(sj.nama_subkategori) LIKE LOWER(%s)
                        AND LOWER(sp.status) LIKE LOWER(%s)
                        AND tps.tgl_waktu = (
                            SELECT MAX(tps2.tgl_waktu)
                            FROM SIJARTA.TR_PEMESANAN_STATUS tps2
                            WHERE tps2.id_tr_pemesanan = tps.id_tr_pemesanan
                        );
                       """, [request.session['user']['id'], subcategory, status])
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

@require_http_methods(["POST"])
def cancel_pesanan(request, id):
    if request.session['user']['role'] != 'PELANGGAN':
        messages.error(request, 'Only \'PELANGGAN\' role can delete an order.')
        return redirect(cancel_pesanan)
    
    # check whether the order belongs to the user
    with connection.cursor() as cursor:
        cursor.execute("""
                        SELECT * FROM SIJARTA.TR_PEMESANAN_JASA
                        WHERE id = %s
                        AND id_pelanggan = %s
                       """, [id, request.session['user']['id']])
        
        if cursor.fetchone() is None:
            messages.error(request, 'The order does not belong to you.')
            return redirect(cancel_pesanan)
    
    current_date = datetime.now()
    with connection.cursor() as cursor:
        #alter table change status to cancelled
        cursor.execute("""
                        INSERT INTO SIJARTA.TR_PEMESANAN_STATUS
                        (id_tr_pemesanan, id_status, tgl_waktu)
                        VALUES (%s, (SELECT id FROM SIJARTA.STATUS_PESANAN WHERE status = 'Pesanan Dibatalkan'), %s)
                        """, [id, current_date])
    return JsonResponse({"success": True, "message": "Order canceled successfully."})
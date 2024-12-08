from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
import json
import logging
import uuid
from datetime import datetime, timezone, timedelta

logger = logging.getLogger(__name__)
jakarta_offset = timezone(timedelta(hours=7)) # WIB timezone

def discount(request):
    if 'user' not in request.session:
        return redirect('kuning:login')
    user_id = request.session['user'].get('id')
    user_balance = request.session['user'].get('saldo_mypay', 0)
    return render(request, 'discount.html', {'user_balance': user_balance})

def button_testi(request):
    return render(request, 'pesanan.html')

@require_http_methods(["GET"])
def get_discounts(request):
    with connection.cursor() as cursor:

        cursor.execute("""
            SELECT 
                v.kode,
                d.potongan,
                d.min_tr_pemesanan,
                v.jml_hari_berlaku,
                v.kuota_penggunaan,
                v.harga
            FROM SIJARTA.VOUCHER v
            JOIN SIJARTA.DISKON d ON v.kode = d.kode
            WHERE v.kuota_penggunaan > 0
            ORDER BY v.kode
        """)
        voucher_data = cursor.fetchall()

        cursor.execute("""
            SELECT
                p.kode,
                p.tgl_akhir_berlaku
            FROM SIJARTA.PROMO p
            JOIN SIJARTA.DISKON d ON p.kode = d.kode
            WHERE p.tgl_akhir_berlaku >= CURRENT_DATE
            ORDER BY p.tgl_akhir_berlaku
        """)
        promo_data = cursor.fetchall()

        return JsonResponse({
            'voucher_data': [list(v) for v in voucher_data],
            'promo_data': [list(p) for p in promo_data]
        })
    
@require_http_methods(["GET"])
@csrf_exempt
def get_metode_bayar(request):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT id, nama FROM SIJARTA.METODE_BAYAR 
            """
        )
        metode_bayar = cursor.fetchall()

        return JsonResponse({
            'metode_bayar': [list(m) for m in metode_bayar]
        })

@require_http_methods(["POST"])
@csrf_exempt
def buy_voucher(request):
    try:        
        user_id = request.session['user'].get('id')
        user_balance = request.session['user'].get('saldo_mypay', 0)

        data = json.loads(request.body)
        voucher_code = data.get('kode')
        payment_method_id = data.get('metode_bayar')

        if payment_method_id == 'a3c14e6e-1d39-458c-8323-8e70671817fb':        
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT harga, jml_hari_berlaku, kuota_penggunaan 
                    FROM SIJARTA.VOUCHER 
                    WHERE kode = %s AND kuota_penggunaan > 0
                """, [voucher_code])
                voucher_info = cursor.fetchone()

                voucher_price, days, voucher_quota = voucher_info

                if user_balance < voucher_price:
                    return JsonResponse({'error': 'Saldo tidak mencukupi.'}, status=400)
            
                purchase_id = uuid.uuid4()

                current_date = datetime.now(jakarta_offset).date()
                expiry_date = current_date + timedelta(days)
                
                cursor.execute("""
                    INSERT INTO SIJARTA.TR_PEMBELIAN_VOUCHER 
                    (id, tgl_awal, tgl_akhir, telah_digunakan, id_pelanggan, id_voucher, id_metode_bayar)
                    VALUES (%s, %s, %s, 0, %s, %s, %s)
                """, [
                    purchase_id, 
                    current_date, 
                    expiry_date, 
                    user_id, 
                    voucher_code, 
                    payment_method_id
                ])

                cursor.execute("""
                    SELECT id FROM SIJARTA.KATEGORI_TR_MYPAY 
                    WHERE id = 'd516d5f5-3142-44a5-8f36-b91b38147c36'
                """, [])
                kategori_id = cursor.fetchone()[0]

                tr_mypay_id = str(uuid.uuid4())
                cursor.execute("""
                    INSERT INTO SIJARTA.TR_MYPAY 
                    (id, user_id, tgl, nominal, kategori_id)
                    VALUES (%s, %s, %s, %s, %s)
                """, [
                    tr_mypay_id,
                    user_id, 
                    current_date, 
                    voucher_price,
                    kategori_id
                ])

                cursor.execute("""
                    UPDATE SIJARTA."USER" 
                    SET saldo_mypay = saldo_mypay - %s 
                    WHERE id = %s
                """, [voucher_price, user_id])

                request.session['user']['saldo_mypay'] -= float(voucher_price)
                request.session.save()
            
        return JsonResponse({
            'message': 'Voucher berhasil dibeli!',
            'new_balance': request.session['user']['saldo_mypay']
        })
    
    except Exception as e:
        logger.error(f"Error in buy_voucher: {str(e)}")
        return JsonResponse({
            'error': 'Terjadi kesalahan saat membeli voucher.'
        }, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def get_testimoni(request, subkategori_id, worker_id):
    if 'user' not in request.session:
        return JsonResponse({'error': 'Silakan login terlebih dahulu.'}, status=401)
    
    current_user_id = request.session['user'].get('id', None)

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                t.rating, 
                t.teks AS comment, 
                u.nama AS customer_name,
                t.tgl AS testimonial_date,
                sj.nama_subkategori AS service_subcategory,
                tpj.id AS order_id,
                CASE WHEN tpj.id_pelanggan = %s THEN TRUE ELSE FALSE END AS is_own_testimonial
            FROM SIJARTA.TESTIMONI t
            JOIN SIJARTA.TR_PEMESANAN_JASA tpj ON t.id_tr_pemesanan = tpj.id
            JOIN SIJARTA.PELANGGAN p ON tpj.id_pelanggan = p.id
            JOIN SIJARTA."USER" u ON p.id = u.id
            JOIN SIJARTA.SUBKATEGORI_JASA sj ON tpj.id_kategori_jasa = sj.id
            WHERE 
                tpj.id_pekerja = %s AND 
                tpj.id_kategori_jasa = %s
            ORDER BY t.tgl DESC
        """, [current_user_id, worker_id, subkategori_id])
        
        testimonials = cursor.fetchall()

        testimonial_list = [
            {
                'rating': row[0],
                'comment': row[1],
                'author': row[2],
                'date': row[3].strftime("%Y-%m-%d") if row[3] else None,
                'service_subcategory': row[4],
                'order_id': row[5],
                'is_own_testimonial': row[6],
            } for row in testimonials
        ]
        
        return JsonResponse({
            'testimonials': testimonial_list
        })

@require_http_methods(["POST"])
@csrf_exempt
def submit_testimonial(request):
    try:
        if 'user' not in request.session:
            return JsonResponse({'error': 'Silakan login terlebih dahulu.'}, status=401)

        data = json.loads(request.body)
        worker_id = data.get('order_id')
        rating = data.get('rating')
        comment = data.get('comment')

        logger.error(data)

        if not worker_id or not rating or not comment:
            return JsonResponse({'error': 'Data tidak lengkap.'}, status=400)

        user_id = request.session['user'].get('id')

        logger.error(worker_id)
        logger.error(user_id)

        with connection.cursor() as cursor:

            cursor.execute("""
                SELECT id
                FROM SIJARTA.TR_PEMESANAN_JASA 
                WHERE id_pekerja = %s AND id_pelanggan = %s
            """, [worker_id, user_id])

            order_info = cursor.fetchone()
            order_id = order_info[0]

            logger.error(order_id)

            current_date = datetime.now(jakarta_offset)
            cursor.execute("""
                INSERT INTO SIJARTA.TESTIMONI 
                (id_tr_pemesanan, tgl, teks, rating) 
                VALUES (%s, %s, %s, %s)
            """, [order_id, current_date, comment, rating])

            cursor.execute("""
                WITH worker_testimonials AS (
                    SELECT t.rating
                    FROM SIJARTA.TESTIMONI t
                    JOIN SIJARTA.TR_PEMESANAN_JASA tpj ON t.id_tr_pemesanan = tpj.id
                    WHERE tpj.id_pekerja = %s
                )
                UPDATE SIJARTA.PEKERJA 
                SET rating = (
                    SELECT AVG(rating) 
                    FROM worker_testimonials
                )
                WHERE id = %s
            """, [worker_id, worker_id])

            return JsonResponse({
                'message': 'Testimoni berhasil disimpan!',
                'status': 'success'
            })

    except Exception as e:
        logger.error(f"Error in submit_testimonial: {str(e)}")
        return JsonResponse({
            'error': 'Terjadi kesalahan saat menyimpan testimoni.',
            'details': str(e)
        }, status=500)

@require_http_methods(["DELETE"])
@csrf_exempt
def delete_testimoni(request):

    data = json.loads(request.body)
    order_id = data.get('order_id')
    testimonial_date = data.get('testimonial_date')

    user_id = request.session['user'].get('id')

    logger.error(user_id)

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT tpj.id_pekerja 
            FROM SIJARTA.TESTIMONI t
            JOIN SIJARTA.TR_PEMESANAN_JASA tpj ON t.id_tr_pemesanan = tpj.id
            WHERE t.id_tr_pemesanan = %s AND tpj.id_pelanggan = %s
        """, [order_id, user_id])

        worker_info = cursor.fetchone()

        worker_id = worker_info[0]

        cursor.execute("""
            DELETE FROM SIJARTA.TESTIMONI 
            WHERE id_tr_pemesanan = %s AND tgl = %s
        """, [order_id, testimonial_date])

        cursor.execute("""
            WITH worker_testimonials AS (
                SELECT t.rating
                FROM SIJARTA.TESTIMONI t
                JOIN SIJARTA.TR_PEMESANAN_JASA tpj ON t.id_tr_pemesanan = tpj.id
                WHERE tpj.id_pekerja = %s
            )
            UPDATE SIJARTA.PEKERJA 
            SET rating = COALESCE((
                SELECT AVG(rating) 
                FROM worker_testimonials
            ), 0)
            WHERE id = %s
        """, [worker_id, worker_id])

        return JsonResponse({
            'message': 'Testimoni berhasil dihapus!',
            'status': 'success'
        })
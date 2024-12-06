from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
import json
import logging
import uuid
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

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

        # todo: handle metode bayar selain mypay (kl perlu)
        
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT harga, kuota_penggunaan 
                FROM SIJARTA.VOUCHER 
                WHERE kode = %s AND kuota_penggunaan > 0
            """, [voucher_code])
            voucher_info = cursor.fetchone()
            voucher_price, voucher_quota = voucher_info

            if user_balance < voucher_price:
                return JsonResponse({'error': 'Saldo tidak mencukupi.'}, status=400)
        
            purchase_id = uuid.uuid4()
            current_date = datetime.now().date() # todo: set to indo timezone
            expiry_date = current_date + timedelta(days=int(voucher_info[0])) # todo: fix expired date (masih salah)
            
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
                WHERE id = '546fa422-0eca-4da0-90d2-2cb106bccea4'
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
def get_testimoni(request, worker_id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                t.rating, 
                t.teks, 
                u.nama AS customer_name,
                t.tgl AS testimonial_date
            FROM SIJARTA.TESTIMONI t
            JOIN SIJARTA.TR_PEMESANAN_JASA tpj ON t.id_tr_pemesanan = tpj.id
            JOIN SIJARTA.PELANGGAN p ON tpj.id_pelanggan = p.id
            JOIN SIJARTA."USER" u ON p.id = u.id
            WHERE tpj.id_pekerja = %s
            ORDER BY t.tgl DESC
            LIMIT 10
        """, [worker_id])
        
        testimonials = cursor.fetchall()
        
        testimonial_list = [
            {
                'rating': row[0],
                'comment': row[1],
                'author': row[2],
                'date': row[3].strftime("%Y-%m-%d")
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
        order_id = data.get('order_id')
        rating = data.get('rating')
        comment = data.get('comment')
        
        if not all([order_id, rating, comment]):
            return JsonResponse({'error': 'Data tidak lengkap.'}, status=400)
        
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id_pekerja 
                FROM SIJARTA.TR_PEMESANAN_JASA tpj
                JOIN SIJARTA.TR_PEMESANAN_STATUS tps ON tpj.id = tps.id_tr_pemesanan
                JOIN SIJARTA.STATUS_PESANAN sp ON tps.id_status = sp.id
                WHERE tpj.id = %s AND sp.status = 'Pesanan Selesai'
            """, [order_id])
            
            order_info = cursor.fetchone()
            
            if not order_info:
                return JsonResponse({'error': 'Pesanan tidak valid atau belum selesai.'}, status=400)
            
            worker_id = order_info[0]

            cursor.execute("""
                INSERT INTO SIJARTA.TESTIMONI 
                (id_tr_pemesanan, tgl, teks, rating) 
                VALUES (%s, CURRENT_DATE, %s, %s)
            """, [order_id, comment, rating])
            
            return JsonResponse({
                'message': 'Testimoni berhasil disimpan!',
                'worker_id': str(worker_id)
            })
    
    except Exception as e:
        logger.error(f"Error in submit_testimonial: {str(e)}")
        return JsonResponse({
            'error': 'Terjadi kesalahan saat menyimpan testimoni.'
        }, status=500)
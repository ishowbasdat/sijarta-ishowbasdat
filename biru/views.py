from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
import json
import logging

logger = logging.getLogger(__name__)

def discount(request):
    return render(request, 'discount.html')

@require_http_methods(["GET"])
def get_discounts(request):
    try:
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
                WHERE v.kuota_penggunaan > 0  -- Only show available vouchers
                ORDER BY v.kode
            """)
            voucher_data = cursor.fetchall()

            cursor.execute("""
                SELECT
                    p.kode,
                    p.tgl_akhir_berlaku
                FROM SIJARTA.PROMO p
                JOIN SIJARTA.DISKON d ON p.kode = d.kode
                WHERE p.tgl_akhir_berlaku >= CURRENT_DATE  -- Only show active promos
                ORDER BY p.tgl_akhir_berlaku
            """)
            promo_data = cursor.fetchall()

            logger.info(f"Retrieved {len(voucher_data)} vouchers and {len(promo_data)} promos")
            
            return JsonResponse({
                'voucher_data': [list(v) for v in voucher_data],
                'promo_data': [list(p) for p in promo_data]
            })
    except Exception as e:
        logger.error(f"Error in get_discounts: {str(e)}")
        return JsonResponse({
            'error': 'Terjadi kesalahan saat mengambil data diskon.'
        }, status=500)

@require_http_methods(["POST"])
@csrf_exempt 
def buy_voucher(request):
    try:
        data = json.loads(request.body)
        voucher_code = data.get('kode')
        
        if not voucher_code:
            return JsonResponse({
                'error': 'Kode voucher tidak valid.'
            }, status=400)

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT kuota_penggunaan, harga 
                FROM SIJARTA.VOUCHER 
                WHERE kode = %s
            """, [voucher_code])
            
            result = cursor.fetchone()
            if not result:
                return JsonResponse({
                    'error': 'Voucher tidak ditemukan.'
                }, status=404)
            
            kuota, harga = result
            
            if kuota <= 0:
                return JsonResponse({
                    'error': 'Voucher sudah habis.'
                }, status=400)

            cursor.execute("""
                UPDATE SIJARTA.VOUCHER 
                SET kuota_penggunaan = kuota_penggunaan - 1 
                WHERE kode = %s
            """, [voucher_code])

            return JsonResponse({
                'message': 'Voucher berhasil dibeli!',
                'harga': harga
            })
            
    except Exception as e:
        logger.error(f"Error in buy_voucher: {str(e)}")
        return JsonResponse({
            'error': 'Terjadi kesalahan saat membeli voucher.'
        }, status=500)
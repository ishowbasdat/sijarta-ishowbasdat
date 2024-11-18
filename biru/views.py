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
    voucher_data = [
        ["DISC10", 10000, 100000, 30, 100, 5000],  # [kode, potongan, min_tr, hari_berlaku, kuota, harga]
        ["DISC20", 20000, 200000, 15, 50, 10000],
        ["DISC30", 30000, 300000, 45, 50, 90000],
        ["DISC40", 40000, 400000, 20, 50, 40000]
    ]
    
    promo_data = [
        ["PROMO1", "2024-12-31"],
        ["PROMO2", "2024-12-31"],
    ]
    
    return JsonResponse({
        'voucher_data': voucher_data,
        'promo_data': promo_data
    })

#@require_http_methods(["POST"])
@csrf_exempt 
def buy_voucher(request):
    data = json.loads(request.body)
    voucher_code = data.get('kode')

    voucher_data = {
        "DISC10": {"kuota": 100, "harga": 5000},
        "DISC20": {"kuota": 50, "harga": 10000}
    }

    voucher = voucher_data[voucher_code]
    
    return JsonResponse({
        'message': 'Voucher berhasil dibeli!',
        'data': {
            'voucher_code': voucher_code,
            'harga': voucher['harga'],
            'kuota': voucher['kuota']
        }
    }, status=200)

def button_testi(request):
    return render(request, 'pesanan.html')

# @require_http_methods(["GET"])
# def get_discounts(request):
#     try:
#         with connection.cursor() as cursor:

#             cursor.execute("""
#                 SELECT 
#                     v.kode,
#                     d.potongan,
#                     d.min_tr_pemesanan,
#                     v.jml_hari_berlaku,
#                     v.kuota_penggunaan,
#                     v.harga
#                 FROM SIJARTA.VOUCHER v
#                 JOIN SIJARTA.DISKON d ON v.kode = d.kode
#                 WHERE v.kuota_penggunaan > 0  -- Only show available vouchers
#                 ORDER BY v.kode
#             """)
#             voucher_data = cursor.fetchall()

#             cursor.execute("""
#                 SELECT
#                     p.kode,
#                     p.tgl_akhir_berlaku
#                 FROM SIJARTA.PROMO p
#                 JOIN SIJARTA.DISKON d ON p.kode = d.kode
#                 WHERE p.tgl_akhir_berlaku >= CURRENT_DATE  -- Only show active promos
#                 ORDER BY p.tgl_akhir_berlaku
#             """)
#             promo_data = cursor.fetchall()

#             logger.info(f"Retrieved {len(voucher_data)} vouchers and {len(promo_data)} promos")
            
#             return JsonResponse({
#                 'voucher_data': [list(v) for v in voucher_data],
#                 'promo_data': [list(p) for p in promo_data]
#             })
#     except Exception as e:
#         logger.error(f"Error in get_discounts: {str(e)}")
#         return JsonResponse({
#             'error': 'Terjadi kesalahan saat mengambil data diskon.'
#         }, status=500)

# @require_http_methods(["POST"])
# @csrf_exempt 
# def buy_voucher(request):
#     try:
#         data = json.loads(request.body)
#         voucher_code = data.get('kode')
        
#         if not voucher_code:
#             return JsonResponse({
#                 'error': 'Kode voucher tidak valid.'
#             }, status=400)

#         with connection.cursor() as cursor:
#             cursor.execute("""
#                 SELECT kuota_penggunaan, harga 
#                 FROM SIJARTA.VOUCHER 
#                 WHERE kode = %s
#             """, [voucher_code])
            
#             result = cursor.fetchone()
#             if not result:
#                 return JsonResponse({
#                     'error': 'Voucher tidak ditemukan.'
#                 }, status=404)
            
#             kuota, harga = result
            
#             if kuota <= 0:
#                 return JsonResponse({
#                     'error': 'Voucher sudah habis.'
#                 }, status=400)

#             cursor.execute("""
#                 UPDATE SIJARTA.VOUCHER 
#                 SET kuota_penggunaan = kuota_penggunaan - 1 
#                 WHERE kode = %s
#             """, [voucher_code])

#             return JsonResponse({
#                 'message': 'Voucher berhasil dibeli!',
#                 'harga': harga
#             })
            
#     except Exception as e:
#         logger.error(f"Error in buy_voucher: {str(e)}")
#         return JsonResponse({
#             'error': 'Terjadi kesalahan saat membeli voucher.'
#         }, status=500)
from django.shortcuts import render
from django.db import connection
from django.http import JsonResponse

def show_main(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                *
            FROM SIJARTA.DISKON d
            JOIN SIJARTA.VOUCHER v ON d.kode = v.kode
        """)
        voucher_data = cursor.fetchall()
        print(voucher_data)
        cursor.execute("""
            SELECT
                *
            FROM SIJARTA.PROMO p
            JOIN SIJARTA.DISKON v ON p.kode = v.kode
        """)
        promo_data = cursor.fetchall()

    context = {
        'voucher_data': voucher_data,
        'promo_data': promo_data
    }
    return render(request, 'main.html', context)


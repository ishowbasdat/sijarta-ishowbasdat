from django.shortcuts import render

def show_main(request):
    context = {
        'vouchers': [
            {'code': 'DISCOUNT10', 'potongan': 0.1, 'min_transaction': 50000, 'valid_days': 30, 'usage_quota': 100, 'price': 10000},
            {'code': 'DISCOUNT20', 'potongan': 0.2, 'min_transaction': 100000, 'valid_days': 60, 'usage_quota': 50, 'price': 20000},
            {'code': 'DISCOUNT30', 'potongan': 0.3, 'min_transaction': 150000, 'valid_days': 90, 'usage_quota': 25, 'price': 30000}
        ],
        'promos': [
            {'code': 'SUMMER_SALE', 'valid_until': '2023-07-31'},
            {'code': 'ANJAY_MABAR', 'valid_until': '2024-04-01'},
            {'code': 'FREE_FIRE', 'valid_until': '2024-12-14'}
        ],
        'testimonies': [
            {'rating': 5, 'comment': 'Layanan sangat memuaskan!'},
            {'rating': 4, 'comment': 'Produk sesuai dengan harapan'},
            {'rating': 3, 'comment': 'Layanan buruk tetapi murah'},
        ]
    }
    return render(request, 'main.html', context)

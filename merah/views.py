from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def mypay_info(request):
    return render(request, 'mypay_info.html')

def mypay_transaction(request):
    # Menentukan tipe user (misalnya berdasarkan role atau langsung dari request.user)
    user_type = 'pengguna'  # Anda bisa sesuaikan ini dengan logika berdasarkan user yang login
    
    context = {
        'user_type': user_type,
    }
    
    return render(request, 'mypay_transaction.html', context)

def pekerjaan_jasa(request):
    return render(request, 'pekerjaan_jasa.html')

def status_pekerjaan_jasa(request):
    return render(request, 'status_pekerjaan_jasa.html')
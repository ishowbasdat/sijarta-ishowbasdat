from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

def mypay_info(request):
    return render(request, 'mypay_info.html')

def mypay_transaction(request):    
    return render(request, 'mypay_transaction.html')

def pekerjaan_jasa(request):
    return render(request, 'pekerjaan_jasa.html')

def status_pekerjaan_jasa(request):
    return render(request, 'status_pekerjaan_jasa.html')
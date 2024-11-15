from django.shortcuts import render
from django.db import connection
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, HttpResponseBadRequest

@require_http_methods(["GET"])
def homepage(request):
    category = request.GET.get('category')
    subcategory = request.GET.get('subcategory')
    
    if category is None:
        category = None
    if subcategory is None:
        subcategory = '%'
    else:
        subcategory = f"%{subcategory}%"
    
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT *
            FROM SIJARTA.KATEGORI_JASA, SIJARTA.SUBKATEGORI_JASA
            WHERE SIJARTA.KATEGORI_JASA.id = SIJARTA.SUBKATEGORI_JASA.kategori_jasa_id
            AND (%s IS NULL OR SIJARTA.KATEGORI_JASA.id = %s)
            AND SIJARTA.SUBKATEGORI_JASA.nama_subkategori LIKE %s
        """, [category, category, subcategory])
        
        data = [dict(zip([ column[0] for column in cursor.description ], row)) for row in cursor.fetchall()]
        print(data)
    context = {'data': data}
    return render(request, 'homepage.html', context)

@require_http_methods(["GET"])
def subkategori(request, id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM SIJARTA.SUBKATEGORI_JASA WHERE id = %s", [id])
        data = cursor.fetchone()
        
    if data is None:
        return redirect('homepage')
    
    context = {'data' : data, 'role' : request.user.role}
    return render(request, 'subkategori.html', context)

@require_http_methods(["GET", "POST", "PUT"])
def pesan(request):
    pass

@require_http_methods(["GET"])
def get_json_from_query(request, query):
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)  # This is insecure as written
            data = cursor.fetchall()

        # Convert data to JSON format for response
        return JsonResponse({'data': data}, safe=False)
    except Exception as e:
        return HttpResponseBadRequest(f"Invalid query or server error: {str(e)}")
from datetime import timedelta
import uuid
from django.db import connection
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from django.utils import timezone

def mypay_info(request):
    if 'user' not in request.session:
        return redirect('kuning:login')
    
    id = request.session['user'].get('id')

    with connection.cursor() as cursor:
        cursor.execute("""
                       SELECT no_hp, saldo_mypay FROM SIJARTA."USER" AS U WHERE U.id = %s
                       """, [id])
        row = cursor.fetchone()

        if row is None:
            messages.error(request, 'User not found')
            return redirect('kuning:login')

        user_data = dict(zip([column[0] for column in cursor.description], row))

        # Fetch transaction history data
        cursor.execute("""
                       SELECT TR.nominal, K.nama, TR.tgl
                       FROM SIJARTA."USER" AS U 
                       JOIN SIJARTA.TR_MYPAY AS TR ON U.id = TR.user_id
                       JOIN SIJARTA.KATEGORI_TR_MYPAY AS K ON K.id = TR.kategori_id
                       WHERE U.id = %s
                       """, [id])
        
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        tr_data = [dict(zip(columns, row)) for row in rows]

        plus_saldo = ['Topup MyPay', 'Menerima honor transaksi jasa', 'Transfer MyPay dari pengguna lain']

        return render(request, 'mypay_info.html', {'user': user_data, 'transaksi': tr_data, 'plus_saldo': plus_saldo})

        
    return render(request, 'mypay_info.html')

def mypay_transaction(request):
    if 'user' not in request.session:
        return redirect('kuning:login')
    
    id = request.session['user'].get('id')
    role = request.session['user'].get('role')

    if request.method == 'POST':
        # Get current timezone-aware timestamp
        now = timezone.now()
        formatted_timestamp = now.strftime("%Y-%m-%d %H:%M:%S.%f")
        formatted_timestamp = formatted_timestamp.rstrip("0").rstrip(".")

        current_date = timezone.now().date() 
        formatted_pg_date = current_date.strftime('%Y-%m-%d')

        kategori = request.POST.get('kategori')

        # Handle different transaction categories
        with connection.cursor() as cursor:
            cursor.execute("""
                        SELECT saldo_mypay 
                        FROM SIJARTA."USER"
                        WHERE id = %s
                    """, [id])
            user_saldo = cursor.fetchone()[0]

            if kategori == 'Topup MyPay':
                nominal_topup = request.POST.get('nominal_topup')
                if nominal_topup and float(nominal_topup) > 0:
                    cursor.execute("""
                        UPDATE SIJARTA."USER"
                        SET saldo_mypay = saldo_mypay + %s
                        WHERE id = %s
                    """, [nominal_topup, id])

                    cursor.execute("""
                            INSERT INTO SIJARTA.TR_MYPAY VALUES
                            (%s, %s, %s, %s, %s)
                        """, [uuid.uuid4(), id, formatted_pg_date, nominal_topup, '44a6e520-f3e7-4761-87e8-1748e1465aae'])
                    return redirect('merah:mypay_info')  
                else:
                    return render(request, 'mypay_transaction.html', {
                        'error': 'Invalid Top-Up Amount',
                    })

            elif kategori == 'Membayar transaksi jasa':
                jasa_id = request.POST.get('jasa')
                harga_jasa = request.POST.get('harga_jasa')

                if jasa_id and harga_jasa:

                    if user_saldo >= float(harga_jasa):
                        cursor.execute("""
                            UPDATE SIJARTA."USER"
                            SET saldo_mypay = saldo_mypay - %s
                            WHERE id = %s
                        """, [harga_jasa, id])

                        cursor.execute("""
                            INSERT INTO SIJARTA.TR_PEMESANAN_STATUS VALUES
                            (%s, %s, %s)
                        """, [jasa_id, '0b97c6a2-b8d7-42a2-a0c3-f3867ea6dd22', formatted_timestamp])

                        cursor.execute("""
                            INSERT INTO SIJARTA.TR_MYPAY VALUES
                            (%s, %s, %s, %s ,%s)
                        """, [uuid.uuid4(), id, formatted_pg_date, harga_jasa, '546fa422-0eca-4da0-90d2-2cb106bccea4'])
                        return redirect('merah:mypay_info')  
                    else:
                        return render(request, 'mypay_transaction.html', {
                            'error': 'Insufficient Balance',
                        })

            elif kategori == 'Transfer MyPay ke pengguna lain':
                no_hp_tujuan = request.POST.get('no_hp_tujuan')
                nominal_transfer = request.POST.get('nominal_transfer')

                if no_hp_tujuan and nominal_transfer and float(nominal_transfer) > 0:

                    if user_saldo >= float(nominal_transfer):
                        # Deduct from sender
                        cursor.execute("""
                            UPDATE SIJARTA."USER"
                            SET saldo_mypay = saldo_mypay - %s
                            WHERE id = %s
                        """, [nominal_transfer, id])

                        # Add to recipient
                        cursor.execute("""
                            UPDATE SIJARTA."USER"
                            SET saldo_mypay = saldo_mypay + %s
                            WHERE no_hp = %s
                        """, [nominal_transfer, no_hp_tujuan])
                        
                        cursor.execute("""
                            INSERT INTO SIJARTA.TR_MYPAY VALUES
                            (%s, %s, %s, %s, %s)
                        """, [uuid.uuid4(), id, formatted_pg_date, nominal_transfer, '6390060b-0746-4da9-a6f0-4d3ee63c4d28'])

                        cursor.execute("""
                       SELECT id FROM SIJARTA."USER" AS U WHERE U.no_hp = %s
                       """, [no_hp_tujuan])
                        recipient_id = cursor.fetchone()[0]

                        cursor.execute("""
                            INSERT INTO SIJARTA.TR_MYPAY VALUES
                            (%s, %s, %s, %s, %s)
                        """, [uuid.uuid4(), recipient_id, formatted_pg_date, nominal_transfer, '8347f8e9-677e-43f6-b9d4-4d3fd5211e4d'])

                        return redirect('merah:mypay_info') 
                    else:
                        return redirect('merah:mypay_transaction') 

            elif kategori == 'Withdrawal MyPay ke rekening bank':
                bank = request.POST.get('bank')
                rekening = request.POST.get('rekening')
                nominal_withdrawal = request.POST.get('nominal_withdrawal')

                if bank and rekening and nominal_withdrawal and float(nominal_withdrawal) > 0:
                    if user_saldo >= float(nominal_withdrawal):
                        cursor.execute("""
                            UPDATE SIJARTA."USER"
                            SET saldo_mypay = saldo_mypay - %s
                            WHERE id = %s
                        """, [nominal_withdrawal, id])

                        cursor.execute("""
                            INSERT INTO SIJARTA.TR_MYPAY VALUES
                            (%s, %s, %s, %s, %s)
                        """, [uuid.uuid4(), id, formatted_pg_date, nominal_withdrawal, '7080df35-dd42-44cf-b09f-956414f5d499'])
                        return redirect('merah:mypay_info') 
                    else:
                        return render(request, 'mypay_transaction.html', {
                            'error': 'Insufficient Balance',
                        })

    with connection.cursor() as cursor:
        cursor.execute("""
                       SELECT no_hp, saldo_mypay FROM SIJARTA."USER" AS U WHERE U.id = %s
                       """, [id])
        row = cursor.fetchone()

        user_data = dict(zip([column[0] for column in cursor.description], row))

        if role == 'PELANGGAN':
            cursor.execute("""
                            SELECT SJ.nama_subkategori, SJ.deskripsi, SL.sesi, TP.total_biaya, TP.id
                           FROM SIJARTA.TR_PEMESANAN_JASA TP
                           JOIN SIJARTA.SESI_LAYANAN SL ON TP.id_kategori_jasa = SL.subkategori_id AND TP.sesi = SL.sesi
                           JOIN SIJARTA.SUBKATEGORI_JASA SJ ON SL.subkategori_id = SJ.id
                           JOIN SIJARTA.TR_PEMESANAN_STATUS TS ON TS.id_tr_pemesanan = TP.id
                           WHERE TP.id_pelanggan = %s AND TP.id_metode_bayar = 'a3c14e6e-1d39-458c-8323-8e70671817fb' AND TS.id_status = 'bb573456-b644-4e58-9ced-3e887f8381ba' AND TS.tgl_waktu = (
                                SELECT MAX(TPS.tgl_waktu)
                                FROM SIJARTA.TR_PEMESANAN_STATUS TPS
                                WHERE TPS.id_tr_pemesanan = TS.id_tr_pemesanan
                           )
                            """, [id])
            
            rows = cursor.fetchall()

            if rows is None:
                tr_data = []
            else:
                columns = [col[0] for col in cursor.description]
                tr_data = [dict(zip(columns, row)) for row in rows]

            cursor.execute("""
                           SELECT nama FROM SIJARTA.KATEGORI_TR_MYPAY
                           WHERE nama NOT IN ('Menerima honor transaksi jasa', 'Transfer MyPay dari pengguna lain') 
                           """)
            
        else:
            cursor.execute("""
                           SELECT nama FROM SIJARTA.KATEGORI_TR_MYPAY
                           WHERE nama NOT IN ('Membayar transaksi jasa', 'Menerima honor transaksi jasa', 'Transfer MyPay dari pengguna lain')
                           """)

            tr_data = []
        
        rows = cursor.fetchall()
        category_data = [row[0] for row in rows]
        return render(request, 'mypay_transaction.html', {'user': user_data,'category_data': category_data, 'tr_data': tr_data})

def get_service_price(request, service_id):
    # Check if the request is an AJAX request by looking for the X-Requested-With header
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == "GET":
        with connection.cursor() as cursor:
            cursor.execute("""
                            SELECT total_biaya
                            FROM SIJARTA.TR_PEMESANAN_JASA
                            WHERE id = %s
                            """, [service_id])
            
            row = cursor.fetchone()

            if row:
                total_biaya = row[0]  # Correctly extract the price value
                return JsonResponse({'total_biaya': total_biaya})
            else:
                return JsonResponse({'error': 'Service not found'}, status=404)

    return JsonResponse({'error': 'Invalid request'}, status=400)

def pekerjaan_jasa(request):
    if 'user' not in request.session:
        return redirect('kuning:login')
    
    id = request.session['user'].get('id')
    role = request.session['user'].get('role')

    if role != "PEKERJA":
        return redirect('kuning:login')
    
    with connection.cursor() as cursor:
        if request.method == 'POST':
            pesanan_id = request.POST.get('pesanan_id')
            now = timezone.now()
            formatted_timestamp = now.strftime("%Y-%m-%d %H:%M:%S.%f")
            formatted_timestamp = formatted_timestamp.rstrip("0").rstrip(".")
            cursor.execute("""
                            INSERT INTO SIJARTA.TR_PEMESANAN_STATUS VALUES
                            (%s, %s, %s)
                        """, [pesanan_id, 'f6c936b2-54c9-49dc-84b9-664e3cded1e5', formatted_timestamp])
            
            cursor.execute("""
                            UPDATE SIJARTA.TR_PEMESANAN_JASA
                            SET id_pekerja = %s
                            WHERE id = %s
                        """, [id, pesanan_id])
            
            cursor.execute("""
                            UPDATE SIJARTA.TR_PEMESANAN_JASA
                            SET tgl_pekerjaan = %s
                            WHERE id = %s
                        """, [formatted_timestamp, pesanan_id])
            
            cursor.execute("""
                            SELECT sesi
                            FROM SIJARTA.TR_PEMESANAN_JASA
                            WHERE id = %s
                            """, [pesanan_id])
            
            row = cursor.fetchone()[0]

            # Tambahkan 3 hari ke timestamp
            waktu_pekerjaan = now + timedelta(days=row)
            formatted_waktu_pekerjaan = waktu_pekerjaan.strftime("%Y-%m-%d %H:%M:%S.%f").rstrip("0").rstrip(".")
            cursor.execute("""
                            UPDATE SIJARTA.TR_PEMESANAN_JASA
                            SET waktu_pekerjaan = %s
                            WHERE id = %s
                        """, [formatted_waktu_pekerjaan, pesanan_id])
            return redirect('merah:status_pekerjaan_jasa')  
        
        cursor.execute("""
                        SELECT KJ.id, KJ.nama_kategori
                        FROM SIJARTA.KATEGORI_JASA KJ
                        JOIN SIJARTA.PEKERJA_KATEGORI_JASA PKJ ON KJ.id = PKJ.kategori_jasa_id
                        WHERE PKJ.pekerja_id = %s
                        """, [id])
        
        rows = cursor.fetchall()

        if rows is None:
            kategori_jasa = []
        else:
            columns = [col[0] for col in cursor.description]
            kategori_jasa = [dict(zip(columns, row)) for row in rows]
    return render(request, 'pekerjaan_jasa.html', {"kategori": kategori_jasa})

def get_subkategori_jasa(request, kategori_id):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == "GET":
        with connection.cursor() as cursor:
            cursor.execute("""
                            SELECT id, nama_subkategori
                            FROM SIJARTA.SUBKATEGORI_JASA
                            WHERE kategori_jasa_id = %s
                            """, [kategori_id])
            
            rows = cursor.fetchall()
            
            if rows is None:
                return JsonResponse({'error': 'Service not found'}, status=404)
            else:
                columns = [col[0] for col in cursor.description]
                subkategori = [dict(zip(columns, row)) for row in rows]
                return JsonResponse({'subkategori': subkategori})
            
    return JsonResponse({'error': 'Invalid request'}, status=400)

def filter_pekerjaan_jasa(request, kategori_id, subkategori_id):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == "GET":
        with connection.cursor() as cursor:
            if kategori_id == uuid.UUID('2233108e-9383-45d8-ac3a-752c8e1f8810') or subkategori_id == uuid.UUID('b6cea022-ddb7-49f9-b1f4-a131778e038a') :
                cursor.execute("""
                    SELECT SJ.nama_subkategori, SJ.deskripsi, TP.total_biaya, TP.id, TP.tgl_pemesanan, TP.sesi, SL.sesi, U.nama
                    FROM SIJARTA.TR_PEMESANAN_JASA TP
                    JOIN SIJARTA.SESI_LAYANAN SL ON TP.id_kategori_jasa = SL.subkategori_id AND TP.sesi = SL.sesi
                    JOIN SIJARTA.SUBKATEGORI_JASA SJ ON SL.subkategori_id = SJ.id
                    JOIN SIJARTA.TR_PEMESANAN_STATUS TS ON TS.id_tr_pemesanan = TP.id
                    JOIN SIJARTA."USER" U ON TP.id_pelanggan = U.id
                    WHERE TS.id_status = '0b97c6a2-b8d7-42a2-a0c3-f3867ea6dd22' AND TS.tgl_waktu = (
                        SELECT MAX(TPS.tgl_waktu)
                        FROM SIJARTA.TR_PEMESANAN_STATUS TPS
                        WHERE TPS.id_tr_pemesanan = TS.id_tr_pemesanan
                    )
                """)
            else:
                cursor.execute("""
                    SELECT SJ.nama_subkategori, SJ.deskripsi, TP.total_biaya, TP.id, TP.tgl_pemesanan, TP.sesi, SL.sesi, U.nama
                    FROM SIJARTA.TR_PEMESANAN_JASA TP
                    JOIN SIJARTA.SESI_LAYANAN SL ON TP.id_kategori_jasa = SL.subkategori_id AND TP.sesi = SL.sesi
                    JOIN SIJARTA.SUBKATEGORI_JASA SJ ON SL.subkategori_id = SJ.id
                    JOIN SIJARTA.TR_PEMESANAN_STATUS TS ON TS.id_tr_pemesanan = TP.id
                    JOIN SIJARTA."USER" U ON TP.id_pelanggan = U.id
                    WHERE SJ.kategori_jasa_id = %s AND SJ.id = %s AND TS.id_status = '0b97c6a2-b8d7-42a2-a0c3-f3867ea6dd22' AND TS.tgl_waktu = (
                        SELECT MAX(TPS.tgl_waktu)
                        FROM SIJARTA.TR_PEMESANAN_STATUS TPS
                        WHERE TPS.id_tr_pemesanan = TS.id_tr_pemesanan
                    )
                """, [kategori_id, subkategori_id])
            
            rows = cursor.fetchall()
            
            if not rows:
                return JsonResponse({'empty': 'Service not found'})
            else:
                columns = [col[0] for col in cursor.description]
                pekerjaan_jasa = [dict(zip(columns, row)) for row in rows]
                return JsonResponse({'pekerjaan': pekerjaan_jasa})
            
    return JsonResponse({'error': 'Invalid request'}, status=400)

def status_pekerjaan_jasa(request):
    if 'user' not in request.session:
        return redirect('kuning:login')
    
    id = request.session['user'].get('id')

    with connection.cursor() as cursor:
        if request.method == 'POST':
            pesanan_id = request.POST.get('pesanan_id')
            status_pesanan = request.POST.get('status_pesanan')
            now = timezone.now()
            formatted_timestamp = now.strftime("%Y-%m-%d %H:%M:%S.%f")
            formatted_timestamp = formatted_timestamp.rstrip("0").rstrip(".")
            if status_pesanan == "Menunggu Pekerja Berangkat":
                cursor.execute("""
                                INSERT INTO SIJARTA.TR_PEMESANAN_STATUS VALUES
                                (%s, %s, %s)
                            """, [pesanan_id, 'ee71d120-34aa-4659-9e4f-606cf2545935', formatted_timestamp])
            elif status_pesanan == "Pekerja Tiba di Lokasi":
                cursor.execute("""
                                INSERT INTO SIJARTA.TR_PEMESANAN_STATUS VALUES
                                (%s, %s, %s)
                            """, [pesanan_id, 'e89ac7f7-8168-4861-8a67-7b601cf720c2', formatted_timestamp])
            
            elif status_pesanan == "Pelayanan Jasa sedang Dilakukan":
                cursor.execute("""
                                INSERT INTO SIJARTA.TR_PEMESANAN_STATUS VALUES
                                (%s, %s, %s)
                            """, [pesanan_id, '7d2d2293-9fc0-4acb-898a-e1fd710c2269', formatted_timestamp])

        cursor.execute("""
                        SELECT *
                        FROM SIJARTA.STATUS_PESANAN
                        WHERE status NOT IN ('Menunggu Pembayaran', 'Mencari Pekerja Terdekat')
                       """)
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        status = [dict(zip(columns, row)) for row in rows]    

    return render(request, 'status_pekerjaan_jasa.html',  {'statuses': status})

def filter_status_pekerjaan_jasa(request, nama_jasa, status_pesanan):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == "GET":
        id = request.session['user'].get('id')
        if nama_jasa == "any" and status_pesanan == uuid.UUID("0f6cf279-d325-4e55-be8a-eac84939e0fc"):
            with connection.cursor() as cursor:
                cursor.execute("""
                            SELECT SJ.nama_subkategori, TP.total_biaya, TP.id, TP.tgl_pemesanan, TP.sesi, U.nama, SP.status
                            FROM SIJARTA.TR_PEMESANAN_JASA TP
                            JOIN SIJARTA.SESI_LAYANAN SL ON TP.id_kategori_jasa = SL.subkategori_id AND TP.sesi = SL.sesi
                            JOIN SIJARTA.SUBKATEGORI_JASA SJ ON SL.subkategori_id = SJ.id
                            JOIN SIJARTA.TR_PEMESANAN_STATUS TS ON TS.id_tr_pemesanan = TP.id
                            JOIN SIJARTA."USER" U ON TP.id_pelanggan = U.id
                            JOIN SIJARTA.STATUS_PESANAN SP ON TS.id_status = SP.id
                            WHERE TP.id_pekerja = %s AND SP.status NOT IN ('Menunggu Pembayaran', 'Mencari Pekerja Terdekat') AND TS.tgl_waktu = (
                                SELECT MAX(TPS.tgl_waktu)
                                FROM SIJARTA.TR_PEMESANAN_STATUS TPS
                                WHERE TPS.id_tr_pemesanan = TS.id_tr_pemesanan
                            )
                        """, [id])

                rows = cursor.fetchall()
                columns = [col[0] for col in cursor.description]
                pekerjaan_jasa = [dict(zip(columns, row)) for row in rows]
                return JsonResponse({'pekerjaan': pekerjaan_jasa})
        else:
            with connection.cursor() as cursor:
                cursor.execute("""
                            SELECT SJ.nama_subkategori, TP.total_biaya, TP.id, TP.tgl_pemesanan, TP.sesi, U.nama, SP.status
                            FROM SIJARTA.TR_PEMESANAN_JASA TP
                            JOIN SIJARTA.SESI_LAYANAN SL ON TP.id_kategori_jasa = SL.subkategori_id AND TP.sesi = SL.sesi
                            JOIN SIJARTA.SUBKATEGORI_JASA SJ ON SL.subkategori_id = SJ.id
                            JOIN SIJARTA.TR_PEMESANAN_STATUS TS ON TS.id_tr_pemesanan = TP.id
                            JOIN SIJARTA."USER" U ON TP.id_pelanggan = U.id
                            JOIN SIJARTA.STATUS_PESANAN SP ON TS.id_status = SP.id
                            WHERE TP.id_pekerja = %s AND SP.status NOT IN ('Menunggu Pembayaran', 'Mencari Pekerja Terdekat') AND SJ.nama_subkategori LIKE %s AND SP.id = %s AND TS.tgl_waktu = (
                                SELECT MAX(TPS.tgl_waktu)
                                FROM SIJARTA.TR_PEMESANAN_STATUS TPS
                                WHERE TPS.id_tr_pemesanan = TS.id_tr_pemesanan
                            )
                        """, [id, f'%{nama_jasa}%', status_pesanan])

                rows = cursor.fetchall()
                columns = [col[0] for col in cursor.description]
                pekerjaan_jasa = [dict(zip(columns, row)) for row in rows]
                return JsonResponse({'pekerjaan': pekerjaan_jasa})

    return JsonResponse({'error': 'Invalid request'}, status=400)
        # TODO:something 
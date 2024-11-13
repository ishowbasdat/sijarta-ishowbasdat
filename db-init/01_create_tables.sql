-- Pembuatan Schema SIJARTA
CREATE SCHEMA IF NOT EXISTS SIJARTA;

-- TABEL
-- 1. USER
CREATE TABLE IF NOT EXISTS SIJARTA."USER" (
    id UUID PRIMARY KEY,
    nama VARCHAR,
    jenis_kelamin CHAR(1) CHECK (jenis_kelamin IN ('L', 'P')),
    no_hp VARCHAR,
    pwd VARCHAR,
    tgl_lahir DATE,
    alamat VARCHAR,
    saldo_mypay DECIMAL
);

-- 2. METODE_BAYAR
CREATE TABLE IF NOT EXISTS SIJARTA.METODE_BAYAR (
    id UUID PRIMARY KEY,
    nama VARCHAR NOT NULL
);

-- 3. PELANGGAN
CREATE TABLE IF NOT EXISTS SIJARTA.PELANGGAN (
    id UUID PRIMARY KEY,
    level VARCHAR,
    FOREIGN KEY (id) REFERENCES SIJARTA."USER"(id)
);

-- 4. PEKERJA
CREATE TABLE IF NOT EXISTS SIJARTA.PEKERJA (
    id UUID PRIMARY KEY, 
    nama_bank VARCHAR,
    nomor_rekening VARCHAR,
    npwp VARCHAR,
    link_foto VARCHAR,
    rating FLOAT,
    jml_pesanan_selesai INT,
    FOREIGN KEY (id) REFERENCES SIJARTA."USER"(id)
);

-- 5. KATEGORI_TR_MYPAY
CREATE TABLE IF NOT EXISTS SIJARTA.KATEGORI_TR_MYPAY (
    id UUID PRIMARY KEY,
    nama VARCHAR
);

-- 6. TR_MYPAY
CREATE TABLE IF NOT EXISTS SIJARTA.TR_MYPAY (
    id UUID PRIMARY KEY,
    user_id UUID,
    tgl DATE,
    nominal DECIMAL,
    kategori_id UUID,
    FOREIGN KEY (user_id) REFERENCES SIJARTA."USER"(id),
    FOREIGN KEY (kategori_id) REFERENCES SIJARTA.KATEGORI_TR_MYPAY(id)
);

-- 7. KATEGORI_JASA
CREATE TABLE IF NOT EXISTS SIJARTA.KATEGORI_JASA (
    id UUID PRIMARY KEY,
    nama_kategori VARCHAR
);

-- 8. SUBKATEGORI_JASA
CREATE TABLE IF NOT EXISTS SIJARTA.SUBKATEGORI_JASA (
    id UUID PRIMARY KEY,
    nama_subkategori VARCHAR,
    deskripsi TEXT,
    kategori_jasa_id UUID,
    FOREIGN KEY (kategori_jasa_id) REFERENCES SIJARTA.KATEGORI_JASA(id)
);

-- 9. SESI_LAYANAN
CREATE TABLE IF NOT EXISTS SIJARTA.SESI_LAYANAN (
    subkategori_id UUID,
    sesi INT,
    harga DECIMAL,
    PRIMARY KEY (subkategori_id, sesi), 
    FOREIGN KEY (subkategori_id) REFERENCES SIJARTA.SUBKATEGORI_JASA(id)
);

-- 10. PEKERJA_KATEGORI_JASA
CREATE TABLE IF NOT EXISTS SIJARTA.PEKERJA_KATEGORI_JASA (
    pekerja_id UUID,
    kategori_jasa_id UUID,
    PRIMARY KEY (pekerja_id, kategori_jasa_id),
    FOREIGN KEY (pekerja_id) REFERENCES SIJARTA.PEKERJA(id),
    FOREIGN KEY (kategori_jasa_id) REFERENCES SIJARTA.KATEGORI_JASA(id)
);

-- 11. DISKON
CREATE TABLE IF NOT EXISTS SIJARTA.DISKON (
    kode VARCHAR(50) PRIMARY KEY,
    potongan DECIMAL NOT NULL CHECK (potongan >= 0),
    min_tr_pemesanan INT NOT NULL CHECK (min_tr_pemesanan >= 0)
);

-- 12. VOUCHER
CREATE TABLE IF NOT EXISTS SIJARTA.VOUCHER (
    kode VARCHAR PRIMARY KEY,
    jml_hari_berlaku INT NOT NULL CHECK (jml_hari_berlaku >= 0),
    kuota_penggunaan INT,
    harga DECIMAL NOT NULL CHECK (harga >= 0),
    FOREIGN KEY (kode) REFERENCES SIJARTA.DISKON(kode)
);

-- 13. PROMO
CREATE TABLE IF NOT EXISTS SIJARTA.PROMO (
    kode VARCHAR PRIMARY KEY,
    tgl_akhir_berlaku DATE NOT NULL,
    FOREIGN KEY (kode) REFERENCES SIJARTA.DISKON(kode)
);

-- 14. TR_PEMBELIAN_VOUCHER
CREATE TABLE IF NOT EXISTS SIJARTA.TR_PEMBELIAN_VOUCHER (
    id UUID PRIMARY KEY,
    tgl_awal DATE NOT NULL,
    tgl_akhir DATE NOT NULL,
    telah_digunakan INT NOT NULL CHECK (telah_digunakan >= 0),
    id_pelanggan UUID,
    id_voucher VARCHAR,
    id_metode_bayar UUID,
    FOREIGN KEY (id_pelanggan) REFERENCES SIJARTA.PELANGGAN(id),
    FOREIGN KEY (id_voucher) REFERENCES SIJARTA.VOUCHER(kode),
    FOREIGN KEY (id_metode_bayar) REFERENCES SIJARTA.METODE_BAYAR(id)
);

-- 15. TR_PEMESANAN_JASA
CREATE TABLE IF NOT EXISTS SIJARTA.TR_PEMESANAN_JASA (
    id UUID PRIMARY KEY,
    tgl_pemesanan DATE NOT NULL,
    tgl_pekerjaan DATE NOT NULL,
    waktu_pekerjaan TIMESTAMP NOT NULL, 
    total_biaya DECIMAL NOT NULL CHECK (total_biaya >= 0),
    id_pelanggan UUID,
    id_pekerja UUID,
    id_kategori_jasa UUID,
    sesi INT,
    id_diskon VARCHAR(50),
    id_metode_bayar UUID,
    FOREIGN KEY (id_pelanggan) REFERENCES SIJARTA.PELANGGAN(id),
    FOREIGN KEY (id_pekerja) REFERENCES SIJARTA.PEKERJA(id),
    FOREIGN KEY (id_kategori_jasa, sesi) REFERENCES SIJARTA.SESI_LAYANAN(subkategori_id, sesi), 
    FOREIGN KEY (id_diskon) REFERENCES SIJARTA.DISKON(kode),
    FOREIGN KEY (id_metode_bayar) REFERENCES SIJARTA.METODE_BAYAR(id)
);

-- 16. STATUS_PESANAN
CREATE TABLE IF NOT EXISTS SIJARTA.STATUS_PESANAN (
    id UUID PRIMARY KEY,
    status VARCHAR(50) NOT NULL
);

-- 17. TR_PEMESANAN_STATUS
CREATE TABLE IF NOT EXISTS SIJARTA.TR_PEMESANAN_STATUS (
    id_tr_pemesanan UUID,
    id_status UUID,
    tgl_waktu TIMESTAMP NOT NULL,
    PRIMARY KEY (id_tr_pemesanan, id_status),
    FOREIGN KEY (id_tr_pemesanan) REFERENCES SIJARTA.TR_PEMESANAN_JASA(id),
    FOREIGN KEY (id_status) REFERENCES SIJARTA.STATUS_PESANAN(id)
);

-- 18. TESTIMONI
CREATE TABLE IF NOT EXISTS SIJARTA.TESTIMONI (
    id_tr_pemesanan UUID,
    tgl DATE,
    teks TEXT,
    rating INT NOT NULL DEFAULT 0,
    PRIMARY KEY (id_tr_pemesanan, tgl),
    FOREIGN KEY (id_tr_pemesanan) REFERENCES SIJARTA.TR_PEMESANAN_JASA(id)
);

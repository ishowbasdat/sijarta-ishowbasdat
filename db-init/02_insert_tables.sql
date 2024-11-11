-- DUMMY DATA
-- 1. USER
INSERT INTO SIJARTA."USER" VALUES
('ce820534-45af-4871-9d91-4da9e52dc988', 'Christian Raphael Heryanto', 'L', '081213151719', 'ThisIsMyPasswordDontHackMePls', '2005-01-01', 'Jalan Haji Kukusan', 200000.00),
('0b35b618-026e-459a-8f8d-47ffadd5df6d', 'Steven Setiawan', 'L', '082265402230', 'Admin1234Hehe', '2005-02-27', 'Jalan Mandor Goweng', 1000000.00),
('f8681d0c-7aa3-44d7-b4ed-aa7d920c84b4', 'Pascal Hafidz Fajri', 'L', '081245557020', 'ThisIsPascalBro', '2005-03-02', 'Jalan Permata Indah', 2500000.00),
('de600d74-5d18-4c30-85a0-7401ca06f3f1', 'Muhammad Afwan Hafizh', 'L', '081260677789', 'AmeGanteng123', '2004-12-05', 'Jalan Mawar Putih', 500000.00),
('5785126d-33fc-4466-8c4a-9e9cbf2e0444', 'Aditya Putra', 'L', '081234567890', 'P@sswordAditya2024', '1998-05-10', 'Jalan Melati Indah', 1500000.00),
('52a79acb-f262-4c97-a303-8ed5687136b0', 'Dewi Lestari', 'P', '085678945612', 'DewiSejati789!', '1990-12-15', 'Jalan Mawar Merah', 3000000.00),
('914d70f3-6f69-4573-8334-4852f72b44c9', 'Bambang Surya', 'L', '087654321098', 'SuryaMaster234!', '1985-08-20', 'Jalan Merpati Raya', 1800000.00),
('dc47021a-5ea6-47c8-8653-1fadac5ce466', 'Anita Wijaya', 'P', '081345678901', 'Anita2023#Secure', '1995-04-25', 'Jalan Anggrek Baru', 2000000.00),
('d8c84f25-72f2-40b9-aba9-2ceb1ef34bac', 'Nadya Putri', 'P', '082112345678', 'NadyaPutri!2024', '1992-11-03', 'Jalan Kemuning Jaya', 2200000.00),
('94dc8a6d-811f-4eb6-8e8c-dd36686f4554', 'Dini Rahayu', 'P', '081234567890', 'RahayuPassword88*', '1988-07-18', 'Jalan Dahlia Indah', 2500000.00);

-- 2. METODE_BAYAR
INSERT INTO SIJARTA.METODE_BAYAR VALUES
('a3c14e6e-1d39-458c-8323-8e70671817fb', 'MyPay'),
('7bfd66f8-fce1-429a-907d-97f94d2b7675', 'GoPay'),
('80a5fb37-8fe5-4039-8d8d-e6c2074f9316', 'OVO'),
('0823f75d-5636-472c-a0dc-31339955584a', 'Virtual Account BCA'),
('a9741cba-ba94-4c92-9902-0ee34f5f50ac', 'Virtual Account BNI'),
('cff8443c-7fef-4f8c-9e10-5b698d1ff6f3', 'Virtual Account Mandiri');

-- 3. PELANGGAN
INSERT INTO SIJARTA.PELANGGAN VALUES
('ce820534-45af-4871-9d91-4da9e52dc988', 'Basic'),
('0b35b618-026e-459a-8f8d-47ffadd5df6d', 'Basic'),
('f8681d0c-7aa3-44d7-b4ed-aa7d920c84b4', 'Gold'),
('de600d74-5d18-4c30-85a0-7401ca06f3f1', 'Basic'),
('5785126d-33fc-4466-8c4a-9e9cbf2e0444', 'Silver');

-- 4. PEKERJA
INSERT INTO SIJARTA.PEKERJA VALUES
('52a79acb-f262-4c97-a303-8ed5687136b0', 'Bank Mandiri', '140001234567890', '12.345.678.5-678.000', 'https://p16-va.lemon8cdn.com/tos-alisg-v-a3e477-sg/oECGEmxHAeAAX95AIlDnRmbUQAIDgp4ABQfiut~tplv-tej9nj120t-origin.webp', 4.8, 150),
('914d70f3-6f69-4573-8334-4852f72b44c9', 'Bank BNI', '009001234567890', '31.654.987.2-435.000', 'https://image.popmama.com/content-images/post/20220208/openingjpg-11b4aeff3bb18fa97f7954c2cb2abb68.jpg?width=600&height=auto', 4.5, 120),
('dc47021a-5ea6-47c8-8653-1fadac5ce466', 'Bank BCA', '001501234567890', '45.987.654.8-321.000', 'https://darahkubiru.com/wp-content/uploads/2023/06/yuji-itadori-dari-jujutsu-kaisen-1.jpg', 4.9, 50),
('d8c84f25-72f2-40b9-aba9-2ceb1ef34bac', 'Bank Mandiri', '140001234567891', '11.123.456.7-890.000', 'https://cdn.vcgamers.com/news/wp-content/uploads/2023/08/Gambar-Anime.jpg', 4.6, 175),
('94dc8a6d-811f-4eb6-8e8c-dd36686f4554', 'Bank BCA', '001501234567892', '62.456.789.9-123.000', 'https://png.pngtree.com/thumb_back/fh260/background/20230524/pngtree-an-anime-girl-in-headphones-looking-at-the-city-with-lights-image_2680902.jpg', 4.7, 130);

-- 5. KATEGORI_TR_MYPAY
INSERT INTO SIJARTA.KATEGORI_TR_MYPAY VALUES 
('44a6e520-f3e7-4761-87e8-1748e1465aae', 'Topup MyPay'),
('546fa422-0eca-4da0-90d2-2cb106bccea4', 'Membayar transaksi jasa'),
('6390060b-0746-4da9-a6f0-4d3ee63c4d28', 'Transfer MyPay ke pengguna lain'),
('b43d8c74-b918-43ec-ab5f-30a1796b9543', 'Menerima honor transaksi jasa'),
('7080df35-dd42-44cf-b09f-956414f5d499', 'Withdrawal MyPay ke rekening bank');

-- 6. TR_MYPAY
INSERT INTO SIJARTA.TR_MYPAY VALUES 
('8540efb1-d052-4043-80f7-ecf32e7591d0', '5785126d-33fc-4466-8c4a-9e9cbf2e0444', '2023-08-27', 53454.0, '546fa422-0eca-4da0-90d2-2cb106bccea4'),
('e5cc83e0-5a40-4680-abad-aa47f0ee19cd', 'ce820534-45af-4871-9d91-4da9e52dc988', '2023-12-07', 544873.37, '6390060b-0746-4da9-a6f0-4d3ee63c4d28'),
('e0638e5e-c427-44a2-95d9-af2b1e08514a', '0b35b618-026e-459a-8f8d-47ffadd5df6d', '2024-11-29', 723744.84, '44a6e520-f3e7-4761-87e8-1748e1465aae'),
('d20419f2-7519-4758-b17c-d2c2bf7b0c27', 'de600d74-5d18-4c30-85a0-7401ca06f3f1', '2023-11-23', 830844.04, '546fa422-0eca-4da0-90d2-2cb106bccea4'),
('152d8a87-38df-4d69-9dd2-1ff05589da9d', 'dc47021a-5ea6-47c8-8653-1fadac5ce466', '2021-04-05', 84246.4, 'b43d8c74-b918-43ec-ab5f-30a1796b9543'),
('57b446c0-f00e-4c0f-962f-33b1e37e28bc', 'ce820534-45af-4871-9d91-4da9e52dc988', '2023-05-05', 121150.27, 'b43d8c74-b918-43ec-ab5f-30a1796b9543'),
('dcf4b991-c7d8-4fc8-a3a7-9a2585a7a349', '914d70f3-6f69-4573-8334-4852f72b44c9', '2022-02-18', 512769.58, 'b43d8c74-b918-43ec-ab5f-30a1796b9543'),
('30cea16f-0d18-4117-b5cf-8a6937a1bc1a', 'f8681d0c-7aa3-44d7-b4ed-aa7d920c84b4', '2024-06-24', 205455.11, '6390060b-0746-4da9-a6f0-4d3ee63c4d28'),
('f71ea03a-a520-44d4-a1a1-2dda1359d728', '52a79acb-f262-4c97-a303-8ed5687136b0', '2024-03-05', 363535.52, '546fa422-0eca-4da0-90d2-2cb106bccea4'),
('cec1989c-a0d2-45f5-9cb9-654fe3615cb5', '5785126d-33fc-4466-8c4a-9e9cbf2e0444', '2024-12-28', 612799.18, '7080df35-dd42-44cf-b09f-956414f5d499'),
('dab1b831-d0f6-4c0a-8e24-a3de155d0296', 'de600d74-5d18-4c30-85a0-7401ca06f3f1', '2023-10-10', 686503.79, '7080df35-dd42-44cf-b09f-956414f5d499'),
('87bccbb8-f418-4bdf-a72f-b0f4abdddea8', '914d70f3-6f69-4573-8334-4852f72b44c9', '2020-01-24', 273779.64, '44a6e520-f3e7-4761-87e8-1748e1465aae'),
('0c61cc4c-774b-4b70-af45-5dbec62ad653', 'd8c84f25-72f2-40b9-aba9-2ceb1ef34bac', '2020-08-18', 772191.43, '6390060b-0746-4da9-a6f0-4d3ee63c4d28'),
('fce8df2c-54f6-43a2-abfb-967052fb6d74', '52a79acb-f262-4c97-a303-8ed5687136b0', '2020-06-10', 175212.85, '44a6e520-f3e7-4761-87e8-1748e1465aae'),
('d4cc9c0b-4953-420b-bab3-88fe08317b87', '94dc8a6d-811f-4eb6-8e8c-dd36686f4554', '2021-04-20', 395426.37, '44a6e520-f3e7-4761-87e8-1748e1465aae'),
('2e2fb533-f3b4-4943-98a7-8e179363bda2', 'dc47021a-5ea6-47c8-8653-1fadac5ce466', '2021-11-22', 485018.91, '546fa422-0eca-4da0-90d2-2cb106bccea4'),
('4f0e1786-9e64-41f8-b301-edad2041949c', 'ce820534-45af-4871-9d91-4da9e52dc988', '2020-04-30', 960967.33, '546fa422-0eca-4da0-90d2-2cb106bccea4'),
('9a054376-1c6e-4184-9e27-bc413b687375', 'de600d74-5d18-4c30-85a0-7401ca06f3f1', '2024-10-01', 113613.35, '7080df35-dd42-44cf-b09f-956414f5d499'),
('52b27d98-1041-4857-ba26-b143defa002f', '0b35b618-026e-459a-8f8d-47ffadd5df6d', '2022-08-30', 506572.62, '7080df35-dd42-44cf-b09f-956414f5d499'),
('b4e37fce-e8ea-4dc8-bf29-996336b80fd6', 'dc47021a-5ea6-47c8-8653-1fadac5ce466', '2020-05-03', 263037.05, '6390060b-0746-4da9-a6f0-4d3ee63c4d28'),
('53e0b293-2df2-4d39-a37a-defffcc480a2', '0b35b618-026e-459a-8f8d-47ffadd5df6d', '2023-09-14', 510355.58, '44a6e520-f3e7-4761-87e8-1748e1465aae'),
('883dc842-58a5-4842-b1a1-28a0418bcfef', '914d70f3-6f69-4573-8334-4852f72b44c9', '2024-05-02', 501832.14, '44a6e520-f3e7-4761-87e8-1748e1465aae'),
('d05c2d27-6f2a-4676-a3bf-5e2a42379d95', '52a79acb-f262-4c97-a303-8ed5687136b0', '2021-08-31', 831785.18, '44a6e520-f3e7-4761-87e8-1748e1465aae'),
('40c52dca-4e55-47b3-bd68-2bb9f5897aa0', '5785126d-33fc-4466-8c4a-9e9cbf2e0444', '2023-08-28', 912177.84, '546fa422-0eca-4da0-90d2-2cb106bccea4'),
('1e1d713d-dc7c-4a19-96f5-39b36fc1ae78', 'd8c84f25-72f2-40b9-aba9-2ceb1ef34bac', '2024-03-30', 948841.86, '7080df35-dd42-44cf-b09f-956414f5d499');

-- 7. KATEGORI_JASA
INSERT INTO SIJARTA.KATEGORI_JASA VALUES
('e46edbcc-a04a-49d0-b37d-93bbb228fb53', 'Home Cleaning'),
('4812608c-700a-4a89-bb2e-bc9939a5d90c', 'Deep Cleaning'),
('35db18e5-c6a0-4519-8b3d-7a0f7c39e82d', 'Service AC'),
('f9d5d1db-cd8d-4476-96ad-5ec424977290', 'Message'),
('37226a20-3d4d-4792-a4b2-56b52380a587', 'Hair Care');

-- 8. SUBKATEGORI_JASA
INSERT INTO SIJARTA.SUBKATEGORI_JASA VALUES
('342e2903-fae6-450e-ad25-c22189b087b8', 'Daily Cleaning', 'Layanan pembersihan harian untuk rumah', 'e46edbcc-a04a-49d0-b37d-93bbb228fb53'),
('8e37bb39-c1ef-4552-b93a-d7823d2debf9', 'Setrika', 'Layanan menyetrika pakaian', 'e46edbcc-a04a-49d0-b37d-93bbb228fb53'),
('affbc756-0a6f-48af-8bdf-62bfd6a6bd28', 'Pembersihan Dapur dan Kulkas', 'Layanan pembersihan menyeluruh untuk area dapur dan kulkas', 'e46edbcc-a04a-49d0-b37d-93bbb228fb53'),
('44073dfd-d8f3-4aee-b090-6fe75e068025', 'Kombo Daily Cleaning + Setrika', 'Paket layanan pembersihan harian dan menyetrika', 'e46edbcc-a04a-49d0-b37d-93bbb228fb53'),
('096c5059-8e91-4ca7-a1e0-3491336b9b82', 'Kombo Daily Cleaning + Dapur', 'Paket layanan pembersihan harian dengan fokus tambahan pada dapur', 'e46edbcc-a04a-49d0-b37d-93bbb228fb53'),
('60651b5e-32eb-4d04-96ea-51e263fe5120', 'Pembersihan Mendalam Rumah', 'Layanan pembersihan menyeluruh untuk seluruh rumah', '4812608c-700a-4a89-bb2e-bc9939a5d90c'),
('cd0d7ef5-0381-4b50-be01-698264dda637', 'Pembersihan Karpet dan Sofa', 'Layanan pembersihan mendalam untuk karpet dan sofa', '4812608c-700a-4a89-bb2e-bc9939a5d90c'),
('7297c14d-8dda-434a-b7b5-0b6dbb0a0b17', 'Cuci AC', 'Layanan pembersihan rutin untuk unit AC', '35db18e5-c6a0-4519-8b3d-7a0f7c39e82d'),
('18831c74-fb17-4094-98a1-da083a814bfc', 'Pijat Relaksasi', 'Layanan pijat untuk relaksasi seluruh tubuh', 'f9d5d1db-cd8d-4476-96ad-5ec424977290'),
('71428286-a3c6-4489-884b-79810b9f0cd4', 'Potong Rambut', 'Layanan potong dan styling rambut', '37226a20-3d4d-4792-a4b2-56b52380a587');



-- 9. SESI_LAYANAN
INSERT INTO SIJARTA.SESI_LAYANAN VALUES 
('342e2903-fae6-450e-ad25-c22189b087b8', 1, 15000.00),
('342e2903-fae6-450e-ad25-c22189b087b8', 2, 28000.00),
('342e2903-fae6-450e-ad25-c22189b087b8', 3, 40000.00),
('8e37bb39-c1ef-4552-b93a-d7823d2debf9', 1, 35000.00),
('8e37bb39-c1ef-4552-b93a-d7823d2debf9', 2, 65000.00),
('8e37bb39-c1ef-4552-b93a-d7823d2debf9', 3, 90000.00),
('affbc756-0a6f-48af-8bdf-62bfd6a6bd28', 1, 60000.00),
('affbc756-0a6f-48af-8bdf-62bfd6a6bd28', 2, 100000.00),
('affbc756-0a6f-48af-8bdf-62bfd6a6bd28', 3, 120000.00),
('44073dfd-d8f3-4aee-b090-6fe75e068025', 1, 10000.00),
('44073dfd-d8f3-4aee-b090-6fe75e068025', 2, 18000.00),
('44073dfd-d8f3-4aee-b090-6fe75e068025', 3, 25000.00),
('096c5059-8e91-4ca7-a1e0-3491336b9b82', 1, 13000.00),
('096c5059-8e91-4ca7-a1e0-3491336b9b82', 2, 25000.00),
('096c5059-8e91-4ca7-a1e0-3491336b9b82', 3, 35000.00),
('60651b5e-32eb-4d04-96ea-51e263fe5120', 1, 15000.00),
('60651b5e-32eb-4d04-96ea-51e263fe5120', 2, 30000.00),
('60651b5e-32eb-4d04-96ea-51e263fe5120', 3, 45000.00),
('cd0d7ef5-0381-4b50-be01-698264dda637', 1, 25000.00),
('cd0d7ef5-0381-4b50-be01-698264dda637', 2, 45000.00),
('cd0d7ef5-0381-4b50-be01-698264dda637', 3, 60000.00),
('7297c14d-8dda-434a-b7b5-0b6dbb0a0b17', 1, 125000.00),
('7297c14d-8dda-434a-b7b5-0b6dbb0a0b17', 2, 225000.00),
('7297c14d-8dda-434a-b7b5-0b6dbb0a0b17', 3, 300000.00),
('18831c74-fb17-4094-98a1-da083a814bfc', 1, 88000.00),
('18831c74-fb17-4094-98a1-da083a814bfc', 2, 160000.00),
('18831c74-fb17-4094-98a1-da083a814bfc', 3, 230000.00),
('71428286-a3c6-4489-884b-79810b9f0cd4', 1, 51000.00),
('71428286-a3c6-4489-884b-79810b9f0cd4', 2, 99000.00),
('71428286-a3c6-4489-884b-79810b9f0cd4', 3, 140000.00);

-- 10. PEKERJA_KATEGORI_JASA
INSERT INTO SIJARTA.PEKERJA_KATEGORI_JASA VALUES
('52a79acb-f262-4c97-a303-8ed5687136b0', 'e46edbcc-a04a-49d0-b37d-93bbb228fb53'),
('52a79acb-f262-4c97-a303-8ed5687136b0', '4812608c-700a-4a89-bb2e-bc9939a5d90c'),
('52a79acb-f262-4c97-a303-8ed5687136b0', '37226a20-3d4d-4792-a4b2-56b52380a587'),
('914d70f3-6f69-4573-8334-4852f72b44c9', 'e46edbcc-a04a-49d0-b37d-93bbb228fb53'),
('914d70f3-6f69-4573-8334-4852f72b44c9', '35db18e5-c6a0-4519-8b3d-7a0f7c39e82d'),
('dc47021a-5ea6-47c8-8653-1fadac5ce466', '37226a20-3d4d-4792-a4b2-56b52380a587'),
('dc47021a-5ea6-47c8-8653-1fadac5ce466', 'f9d5d1db-cd8d-4476-96ad-5ec424977290'),
('d8c84f25-72f2-40b9-aba9-2ceb1ef34bac', '35db18e5-c6a0-4519-8b3d-7a0f7c39e82d'),
('94dc8a6d-811f-4eb6-8e8c-dd36686f4554', '4812608c-700a-4a89-bb2e-bc9939a5d90c'),
('94dc8a6d-811f-4eb6-8e8c-dd36686f4554', 'f9d5d1db-cd8d-4476-96ad-5ec424977290');

-- 11. DISKON
INSERT INTO SIJARTA.DISKON VALUES
('PROMOGEBYAR01', 1000.00, 5000),
('PROMOHAPPYSAVING', 3000.00, 15000),
('PROMOEXTRADEAL', 5000.00, 25000),
('PROMOMEGABONUS', 7000.00, 35000),
('PROMORAINBOW', 9000.00, 45000),
('PROMOSPECIALDAY', 11000.00, 55000),
('PROMOBESTDEAL', 13000.00, 65000),
('PROMOFLASHSALE', 15000.00, 75000),
('PROMOFINALHOUR', 17000.00, 85000),
('PROMOMANTAP', 19000.00, 95000),
('UNTUNGTERUSSS', 2000.00, 10000),
('HEMATBANYAK', 4000.00, 20000),
('DISKONGOKIL', 6000.00, 30000),
('BELANJACERIA', 8000.00, 40000),
('UNTUNGBERSAMA', 10000.00, 50000),
('HAPPYCUSTOMER', 12000.00, 60000),
('SAVEBIGTIME', 14000.00, 70000),
('SUPERUNTUNG', 16000.00, 80000),
('BELANJARAME', 18000.00, 90000),
('DISKONHEBAT', 20000.00, 100000);

-- 12. VOUCHER
INSERT INTO SIJARTA.VOUCHER VALUES
('UNTUNGTERUSSS', 30, 100, 10000.00),
('HEMATBANYAK', 45, 50, 15000.00),
('DISKONGOKIL', 60, 60, 20000.00),
('BELANJACERIA', 90, 200, 5000.00),
('UNTUNGBERSAMA', 120, 70, 18000.00),
('HAPPYCUSTOMER', 30, 300, 25000.00),
('SAVEBIGTIME', 60, 150, 12000.00),
('SUPERUNTUNG', 90, 400, 22000.00),
('BELANJARAME', 120, 500, 27000.00),
('DISKONHEBAT', 30, 50, 10000.00);

-- 13. PROMO
INSERT INTO SIJARTA.PROMO VALUES
('PROMOGEBYAR01', '2024-12-31'),
('PROMOHAPPYSAVING', '2024-11-30'),
('PROMOEXTRADEAL', '2024-10-31'),
('PROMOMEGABONUS', '2024-09-30'),
('PROMORAINBOW', '2025-01-15'),
('PROMOSPECIALDAY', '2024-12-25'),
('PROMOBESTDEAL', '2024-11-15'),
('PROMOFLASHSALE', '2024-10-15'),
('PROMOFINALHOUR', '2024-09-15'),
('PROMOMANTAP', '2025-02-28');

-- 14. TR_PEMBELIAN_VOUCHER
INSERT INTO SIJARTA.TR_PEMBELIAN_VOUCHER VALUES
('b5c86172-3ce8-4bcd-b9b0-0b3550b32bbc', '2024-01-05', '2024-01-12', 0, 'ce820534-45af-4871-9d91-4da9e52dc988', 'UNTUNGTERUSSS', 'a3c14e6e-1d39-458c-8323-8e70671817fb'),
('f0213124-94c2-4e9e-8847-6c5c69946b59', '2024-01-07', '2024-01-14', 0, '0b35b618-026e-459a-8f8d-47ffadd5df6d', 'HEMATBANYAK',   '7bfd66f8-fce1-429a-907d-97f94d2b7675'),
('c02f3274-e29b-45af-88e0-a9116c0030c0', '2024-01-10', '2024-01-17', 1, 'f8681d0c-7aa3-44d7-b4ed-aa7d920c84b4', 'DISKONGOKIL',   '80a5fb37-8fe5-4039-8d8d-e6c2074f9316'),
('e87be252-28c6-48e2-8521-61ea5f46d05a', '2024-01-12', '2024-01-19', 0, 'de600d74-5d18-4c30-85a0-7401ca06f3f1', 'BELANJACERIA',  '0823f75d-5636-472c-a0dc-31339955584a'),
('d32e6567-d8e4-4bc0-88cb-120922289176', '2024-01-15', '2024-01-22', 1, '5785126d-33fc-4466-8c4a-9e9cbf2e0444', 'UNTUNGBERSAMA', 'a9741cba-ba94-4c92-9902-0ee34f5f50ac'),
('38291a82-fd62-474d-8d92-36b65c9c2b20', '2024-01-20', '2024-01-27', 0, 'ce820534-45af-4871-9d91-4da9e52dc988', 'HAPPYCUSTOMER', 'cff8443c-7fef-4f8c-9e10-5b698d1ff6f3'),
('d203f311-391d-47eb-8ae9-b3d47ec4be4e', '2024-01-25', '2024-02-01', 0, '0b35b618-026e-459a-8f8d-47ffadd5df6d', 'SAVEBIGTIME',   'a3c14e6e-1d39-458c-8323-8e70671817fb'),
('b0794dad-ba81-46ae-bf78-337e69b47b8e', '2024-02-01', '2024-02-08', 1, 'f8681d0c-7aa3-44d7-b4ed-aa7d920c84b4', 'SUPERUNTUNG',   '7bfd66f8-fce1-429a-907d-97f94d2b7675'),
('abdb8ab4-72b8-4895-aa3e-414052598987', '2024-02-04', '2024-02-11', 0, 'de600d74-5d18-4c30-85a0-7401ca06f3f1', 'BELANJARAME',   '80a5fb37-8fe5-4039-8d8d-e6c2074f9316'),
('266e96bb-bf78-4c31-b659-7b21aafb379b', '2024-02-06', '2024-02-13', 1, '5785126d-33fc-4466-8c4a-9e9cbf2e0444', 'DISKONHEBAT',   '0823f75d-5636-472c-a0dc-31339955584a'),
('16863df9-26b9-46d0-a45c-1f169aeff158', '2024-02-10', '2024-02-17', 0, '5785126d-33fc-4466-8c4a-9e9cbf2e0444', 'SAVEBIGTIME',   'a9741cba-ba94-4c92-9902-0ee34f5f50ac'),
('118c6a8e-b83f-4134-a75f-b43971854789', '2024-02-12', '2024-02-19', 0, 'ce820534-45af-4871-9d91-4da9e52dc988', 'SUPERUNTUNG',   'cff8443c-7fef-4f8c-9e10-5b698d1ff6f3'),
('c07c0274-8162-4042-b858-7b29142e71b3', '2024-02-15', '2024-02-22', 1, '0b35b618-026e-459a-8f8d-47ffadd5df6d', 'BELANJARAME',   'a3c14e6e-1d39-458c-8323-8e70671817fb'),
('305f50cd-ddc6-4210-87bb-dc94975175b5', '2024-02-18', '2024-02-25', 0, 'ce820534-45af-4871-9d91-4da9e52dc988', 'DISKONHEBAT',   '7bfd66f8-fce1-429a-907d-97f94d2b7675'),
('be542654-53b8-4d2b-95bc-d9fb604cb25e', '2024-02-20', '2024-02-27', 1, '0b35b618-026e-459a-8f8d-47ffadd5df6d', 'SAVEBIGTIME',   '80a5fb37-8fe5-4039-8d8d-e6c2074f9316'),
('2d4ea2bf-297f-4830-b8c6-7f3602c1e009', '2024-02-25', '2024-03-03', 0, 'f8681d0c-7aa3-44d7-b4ed-aa7d920c84b4', 'SUPERUNTUNG',   '0823f75d-5636-472c-a0dc-31339955584a'),
('a815a4cc-7256-4402-82d4-11e55168e4d1', '2024-02-28', '2024-03-07', 0, 'de600d74-5d18-4c30-85a0-7401ca06f3f1', 'BELANJARAME',   'a9741cba-ba94-4c92-9902-0ee34f5f50ac'),
('adc9147b-790b-4f0a-b1e0-57a7ec10fe09', '2024-03-01', '2024-03-08', 1, '5785126d-33fc-4466-8c4a-9e9cbf2e0444', 'DISKONHEBAT',   'cff8443c-7fef-4f8c-9e10-5b698d1ff6f3');

-- 15. TR_PEMESANAN_JASA
INSERT INTO SIJARTA.TR_PEMESANAN_JASA VALUES
('2c6b918e-3abd-41c2-bdfd-c640470a4278', '2024-01-01', '2024-01-05', '2024-01-05 09:00:00', 15000.00,  'ce820534-45af-4871-9d91-4da9e52dc988', '52a79acb-f262-4c97-a303-8ed5687136b0', '342e2903-fae6-450e-ad25-c22189b087b8', 1, 'PROMOGEBYAR01'   , 'a3c14e6e-1d39-458c-8323-8e70671817fb'),
('02102bfb-1836-4ea6-bf97-6742b771f850', '2024-01-02', '2024-01-06', '2024-01-06 10:30:00', 28000.00,  '0b35b618-026e-459a-8f8d-47ffadd5df6d', '914d70f3-6f69-4573-8334-4852f72b44c9', '342e2903-fae6-450e-ad25-c22189b087b8', 2, 'PROMOHAPPYSAVING', '7bfd66f8-fce1-429a-907d-97f94d2b7675'),
('5019c3ff-e043-426f-b68f-a75fcbfd9586', '2024-01-03', '2024-01-07', '2024-01-07 11:00:00', 40000.00,  'f8681d0c-7aa3-44d7-b4ed-aa7d920c84b4', 'dc47021a-5ea6-47c8-8653-1fadac5ce466', '342e2903-fae6-450e-ad25-c22189b087b8', 3, 'PROMOEXTRADEAL'  , '80a5fb37-8fe5-4039-8d8d-e6c2074f9316'),
('6f23ee1f-cb9d-4692-9d32-114144454f31', '2024-01-04', '2024-01-08', '2024-01-08 14:00:00', 35000.00,  'de600d74-5d18-4c30-85a0-7401ca06f3f1', 'd8c84f25-72f2-40b9-aba9-2ceb1ef34bac', '8e37bb39-c1ef-4552-b93a-d7823d2debf9', 1, 'PROMOMEGABONUS'  , '0823f75d-5636-472c-a0dc-31339955584a'),
('8e530da8-5082-44a1-9023-cd81fdb1965a', '2024-01-05', '2024-01-09', '2024-01-09 15:30:00', 65000.00,  '5785126d-33fc-4466-8c4a-9e9cbf2e0444', '94dc8a6d-811f-4eb6-8e8c-dd36686f4554', '8e37bb39-c1ef-4552-b93a-d7823d2debf9', 2, 'PROMORAINBOW'    , 'a9741cba-ba94-4c92-9902-0ee34f5f50ac'),
('8fd4654e-4eca-4055-9692-5fd494f0d04f', '2024-01-06', '2024-01-10', '2024-01-10 16:45:00', 90000.00,  'ce820534-45af-4871-9d91-4da9e52dc988', '52a79acb-f262-4c97-a303-8ed5687136b0', '8e37bb39-c1ef-4552-b93a-d7823d2debf9', 3, 'PROMOSPECIALDAY' , 'cff8443c-7fef-4f8c-9e10-5b698d1ff6f3'),
('bdf4d13d-d084-4109-bf43-0070af96226f', '2024-01-07', '2024-01-11', '2024-01-11 17:30:00', 60000.00,  '0b35b618-026e-459a-8f8d-47ffadd5df6d', '52a79acb-f262-4c97-a303-8ed5687136b0', 'affbc756-0a6f-48af-8bdf-62bfd6a6bd28', 1, 'PROMOBESTDEAL'   , '7bfd66f8-fce1-429a-907d-97f94d2b7675'),
('8dc17103-c3e2-4591-ad29-15e02f099832', '2024-01-08', '2024-01-12', '2024-01-12 18:00:00', 100000.00, 'f8681d0c-7aa3-44d7-b4ed-aa7d920c84b4', '914d70f3-6f69-4573-8334-4852f72b44c9', 'affbc756-0a6f-48af-8bdf-62bfd6a6bd28', 2, 'PROMOFLASHSALE'  , '80a5fb37-8fe5-4039-8d8d-e6c2074f9316'),
('de87b24b-548c-4c2a-b919-e9e18ad1fc85', '2024-01-09', '2024-01-13', '2024-01-13 19:15:00', 120000.00, 'de600d74-5d18-4c30-85a0-7401ca06f3f1', 'dc47021a-5ea6-47c8-8653-1fadac5ce466', 'affbc756-0a6f-48af-8bdf-62bfd6a6bd28', 3, 'PROMOFINALHOUR'  , '0823f75d-5636-472c-a0dc-31339955584a'),
('2d3642cc-6d9f-448a-9d30-8dbdc2b373b1', '2024-01-10', '2024-01-14', '2024-01-14 20:30:00', 10000.00,  '5785126d-33fc-4466-8c4a-9e9cbf2e0444', 'd8c84f25-72f2-40b9-aba9-2ceb1ef34bac', '44073dfd-d8f3-4aee-b090-6fe75e068025', 1, 'PROMOMANTAP'     , 'a3c14e6e-1d39-458c-8323-8e70671817fb'),
('2217803d-3e5d-48cd-bb9e-c699e2e95a32', '2024-01-11', '2024-01-15', '2024-01-15 21:45:00', 18000.00,  'ce820534-45af-4871-9d91-4da9e52dc988', '94dc8a6d-811f-4eb6-8e8c-dd36686f4554', '44073dfd-d8f3-4aee-b090-6fe75e068025', 2, 'UNTUNGTERUSSS'   , '7bfd66f8-fce1-429a-907d-97f94d2b7675'),
('3003a0d7-42d2-4044-857f-efd280b81397', '2024-01-12', '2024-01-16', '2024-01-16 22:00:00', 25000.00,  '0b35b618-026e-459a-8f8d-47ffadd5df6d', '914d70f3-6f69-4573-8334-4852f72b44c9', '44073dfd-d8f3-4aee-b090-6fe75e068025', 3, 'HEMATBANYAK'     , '80a5fb37-8fe5-4039-8d8d-e6c2074f9316'),
('f39b91e4-bc61-47ae-a8cf-b9d20361fc9a', '2024-01-13', '2024-01-17', '2024-01-17 23:15:00', 13000.00,  'f8681d0c-7aa3-44d7-b4ed-aa7d920c84b4', '52a79acb-f262-4c97-a303-8ed5687136b0', '096c5059-8e91-4ca7-a1e0-3491336b9b82', 1, 'DISKONGOKIL'     , '0823f75d-5636-472c-a0dc-31339955584a'),
('97faede6-3306-4973-b69e-42762ba6b495', '2024-01-14', '2024-01-18', '2024-01-18 10:30:00', 25000.00,  'de600d74-5d18-4c30-85a0-7401ca06f3f1', '914d70f3-6f69-4573-8334-4852f72b44c9', '096c5059-8e91-4ca7-a1e0-3491336b9b82', 2, 'BELANJACERIA'    , 'a9741cba-ba94-4c92-9902-0ee34f5f50ac'),
('1d810223-e910-40b4-8e3c-9ecfd5269d16', '2024-01-15', '2024-01-19', '2024-01-19 11:45:00', 35000.00,  '5785126d-33fc-4466-8c4a-9e9cbf2e0444', 'dc47021a-5ea6-47c8-8653-1fadac5ce466', '096c5059-8e91-4ca7-a1e0-3491336b9b82', 3, 'UNTUNGBERSAMA'   , 'cff8443c-7fef-4f8c-9e10-5b698d1ff6f3'),
('93a02b9a-a002-48c2-a9dc-76e9a64890cb', '2024-01-16', '2024-01-20', '2024-01-20 12:00:00', 15000.00,  'ce820534-45af-4871-9d91-4da9e52dc988', 'd8c84f25-72f2-40b9-aba9-2ceb1ef34bac', '60651b5e-32eb-4d04-96ea-51e263fe5120', 1, 'HAPPYCUSTOMER'   , 'a3c14e6e-1d39-458c-8323-8e70671817fb'),
('88bbdeea-58d9-4cb4-a3ea-ae42107ad188', '2024-01-17', '2024-01-21', '2024-01-21 13:15:00', 30000.00,  '0b35b618-026e-459a-8f8d-47ffadd5df6d', '94dc8a6d-811f-4eb6-8e8c-dd36686f4554', '60651b5e-32eb-4d04-96ea-51e263fe5120', 2, 'SAVEBIGTIME'     , 'a3c14e6e-1d39-458c-8323-8e70671817fb'),
('9e16669a-45d5-4555-bd85-2b9e0016c245', '2024-01-18', '2024-01-22', '2024-01-22 14:30:00', 45000.00,  'f8681d0c-7aa3-44d7-b4ed-aa7d920c84b4', '52a79acb-f262-4c97-a303-8ed5687136b0', '60651b5e-32eb-4d04-96ea-51e263fe5120', 3, 'SUPERUNTUNG'     , '7bfd66f8-fce1-429a-907d-97f94d2b7675'),
('b99e0a9c-0506-49e8-975e-50b15317d8a6', '2024-01-19', '2024-01-23', '2024-01-23 15:45:00', 25000.00,  'de600d74-5d18-4c30-85a0-7401ca06f3f1', '914d70f3-6f69-4573-8334-4852f72b44c9', 'cd0d7ef5-0381-4b50-be01-698264dda637', 1, 'BELANJARAME'     , '80a5fb37-8fe5-4039-8d8d-e6c2074f9316'),
('c5213fe8-24cc-4daf-b162-943c85102c48', '2024-01-20', '2024-01-24', '2024-01-24 16:00:00', 45000.00,  '5785126d-33fc-4466-8c4a-9e9cbf2e0444', 'dc47021a-5ea6-47c8-8653-1fadac5ce466', 'cd0d7ef5-0381-4b50-be01-698264dda637', 2, 'DISKONHEBAT'     , '0823f75d-5636-472c-a0dc-31339955584a'),
('44139880-c1e2-4cfe-aba1-a8c67cdca616', '2024-01-21', '2024-01-25', '2024-01-25 17:15:00', 60000.00,  'ce820534-45af-4871-9d91-4da9e52dc988', 'd8c84f25-72f2-40b9-aba9-2ceb1ef34bac', 'cd0d7ef5-0381-4b50-be01-698264dda637', 3, 'UNTUNGTERUSSS'   , 'a9741cba-ba94-4c92-9902-0ee34f5f50ac'),
('c6f5c866-aa34-4b1e-b456-ac5266af305f', '2024-01-22', '2024-01-26', '2024-01-26 18:30:00', 125000.00, '0b35b618-026e-459a-8f8d-47ffadd5df6d', '94dc8a6d-811f-4eb6-8e8c-dd36686f4554', '7297c14d-8dda-434a-b7b5-0b6dbb0a0b17', 1, 'HEMATBANYAK'     , 'cff8443c-7fef-4f8c-9e10-5b698d1ff6f3'),
('c12afaa5-b4ba-4716-a848-48bc5a19112f', '2024-01-23', '2024-01-27', '2024-01-27 19:00:00', 225000.00, 'f8681d0c-7aa3-44d7-b4ed-aa7d920c84b4', '52a79acb-f262-4c97-a303-8ed5687136b0', '7297c14d-8dda-434a-b7b5-0b6dbb0a0b17', 2, 'DISKONGOKIL'     , '7bfd66f8-fce1-429a-907d-97f94d2b7675'),
('cc91d59d-59fe-4f5a-87b3-cb14d13dfed0', '2024-01-24', '2024-01-28', '2024-01-28 20:15:00', 300000.00, 'de600d74-5d18-4c30-85a0-7401ca06f3f1', '914d70f3-6f69-4573-8334-4852f72b44c9', '7297c14d-8dda-434a-b7b5-0b6dbb0a0b17', 3, 'BELANJACERIA'    , '80a5fb37-8fe5-4039-8d8d-e6c2074f9316'),
('09b9e4f9-b2e5-4799-b652-939637670ff8', '2024-01-25', '2024-01-29', '2024-01-29 21:30:00', 88000.00,  '5785126d-33fc-4466-8c4a-9e9cbf2e0444', '914d70f3-6f69-4573-8334-4852f72b44c9', '18831c74-fb17-4094-98a1-da083a814bfc', 1, 'BELANJACERIA'    , '0823f75d-5636-472c-a0dc-31339955584a');

-- 16. STATUS_PESANAN
INSERT INTO SIJARTA.STATUS_PESANAN VALUES
('bb573456-b644-4e58-9ced-3e887f8381ba', 'Menunggu Pembayaran'),
('0b97c6a2-b8d7-42a2-a0c3-f3867ea6dd22', 'Mencari Pekerja Terdekat'),
('f6c936b2-54c9-49dc-84b9-664e3cded1e5', 'Menunggu Pekerja Berangkat'),
('ee71d120-34aa-4659-9e4f-606cf2545935', 'Pekerja Tiba di Lokasi'),
('636fbe63-0ab1-42c4-ab96-87391e12abde', 'Menunggu Pembayaran'),
('e89ac7f7-8168-4861-8a67-7b601cf720c2', 'Pelayanan Jasa sedang Dilakukan'),
('7d2d2293-9fc0-4acb-898a-e1fd710c2269', 'Pesanan Selesai');

-- 17. TR_PEMESANAN_STATUS
INSERT INTO SIJARTA.TR_PEMESANAN_STATUS VALUES
( '2c6b918e-3abd-41c2-bdfd-c640470a4278', 'bb573456-b644-4e58-9ced-3e887f8381ba', '2024-01-05 09:15:12'),
( '02102bfb-1836-4ea6-bf97-6742b771f850', '0b97c6a2-b8d7-42a2-a0c3-f3867ea6dd22', '2024-01-07 10:30:45'),
( '5019c3ff-e043-426f-b68f-a75fcbfd9586', 'f6c936b2-54c9-49dc-84b9-664e3cded1e5', '2024-01-10 14:05:10'),
( '6f23ee1f-cb9d-4692-9d32-114144454f31', 'ee71d120-34aa-4659-9e4f-606cf2545935', '2024-01-12 16:45:30'),
( '8e530da8-5082-44a1-9023-cd81fdb1965a', '636fbe63-0ab1-42c4-ab96-87391e12abde', '2024-01-15 18:20:55'),
( '8fd4654e-4eca-4055-9692-5fd494f0d04f', 'e89ac7f7-8168-4861-8a67-7b601cf720c2', '2024-01-20 07:55:12'),
( 'bdf4d13d-d084-4109-bf43-0070af96226f', '7d2d2293-9fc0-4acb-898a-e1fd710c2269', '2024-01-25 12:10:05'),
( '8dc17103-c3e2-4591-ad29-15e02f099832', '0b97c6a2-b8d7-42a2-a0c3-f3867ea6dd22', '2024-01-28 14:25:33'),
( 'de87b24b-548c-4c2a-b919-e9e18ad1fc85', 'f6c936b2-54c9-49dc-84b9-664e3cded1e5', '2024-01-30 17:05:27'),
( '2d3642cc-6d9f-448a-9d30-8dbdc2b373b1', 'f6c936b2-54c9-49dc-84b9-664e3cded1e5', '2024-02-02 19:35:19'),
( '2217803d-3e5d-48cd-bb9e-c699e2e95a32', 'bb573456-b644-4e58-9ced-3e887f8381ba', '2024-02-04 21:40:50'),
( '3003a0d7-42d2-4044-857f-efd280b81397', '0b97c6a2-b8d7-42a2-a0c3-f3867ea6dd22', '2024-02-06 15:40:00'),
( 'f39b91e4-bc61-47ae-a8cf-b9d20361fc9a', 'bb573456-b644-4e58-9ced-3e887f8381ba', '2024-02-09 18:15:18'),
( '97faede6-3306-4973-b69e-42762ba6b495', '0b97c6a2-b8d7-42a2-a0c3-f3867ea6dd22', '2024-02-12 22:05:34'),
( '1d810223-e910-40b4-8e3c-9ecfd5269d16', '0b97c6a2-b8d7-42a2-a0c3-f3867ea6dd22', '2024-02-15 11:55:42'),
( '93a02b9a-a002-48c2-a9dc-76e9a64890cb', 'f6c936b2-54c9-49dc-84b9-664e3cded1e5', '2024-02-17 09:35:00'),
( '88bbdeea-58d9-4cb4-a3ea-ae42107ad188', '0b97c6a2-b8d7-42a2-a0c3-f3867ea6dd22', '2024-02-20 13:22:16'),
( '9e16669a-45d5-4555-bd85-2b9e0016c245', 'bb573456-b644-4e58-9ced-3e887f8381ba', '2024-02-23 12:00:00'),
( 'b99e0a9c-0506-49e8-975e-50b15317d8a6', '0b97c6a2-b8d7-42a2-a0c3-f3867ea6dd22', '2024-02-25 16:10:37'),
( 'c5213fe8-24cc-4daf-b162-943c85102c48', 'f6c936b2-54c9-49dc-84b9-664e3cded1e5', '2024-02-27 14:45:23'),
( '44139880-c1e2-4cfe-aba1-a8c67cdca616', '0b97c6a2-b8d7-42a2-a0c3-f3867ea6dd22', '2024-02-28 20:15:12'),
( 'c6f5c866-aa34-4b1e-b456-ac5266af305f', 'bb573456-b644-4e58-9ced-3e887f8381ba', '2024-03-01 08:25:47'),
( 'c12afaa5-b4ba-4716-a848-48bc5a19112f', '0b97c6a2-b8d7-42a2-a0c3-f3867ea6dd22', '2024-03-02 13:50:30'),
( 'cc91d59d-59fe-4f5a-87b3-cb14d13dfed0', 'f6c936b2-54c9-49dc-84b9-664e3cded1e5', '2024-03-05 19:30:00'),
( '09b9e4f9-b2e5-4799-b652-939637670ff8', 'f6c936b2-54c9-49dc-84b9-664e3cded1e5', '2024-03-06 22:05:59'),
( '2d3642cc-6d9f-448a-9d30-8dbdc2b373b1', 'ee71d120-34aa-4659-9e4f-606cf2545935', '2024-03-08 18:55:43'),
( '2217803d-3e5d-48cd-bb9e-c699e2e95a32', '0b97c6a2-b8d7-42a2-a0c3-f3867ea6dd22', '2024-03-10 15:35:22'),
( '3003a0d7-42d2-4044-857f-efd280b81397', 'f6c936b2-54c9-49dc-84b9-664e3cded1e5', '2024-03-12 10:15:12'),
( 'f39b91e4-bc61-47ae-a8cf-b9d20361fc9a', '0b97c6a2-b8d7-42a2-a0c3-f3867ea6dd22', '2024-03-14 14:45:38'),
( '97faede6-3306-4973-b69e-42762ba6b495', 'f6c936b2-54c9-49dc-84b9-664e3cded1e5', '2024-03-17 16:30:05'),
( '1d810223-e910-40b4-8e3c-9ecfd5269d16', 'f6c936b2-54c9-49dc-84b9-664e3cded1e5', '2024-03-19 09:10:20'),
( '93a02b9a-a002-48c2-a9dc-76e9a64890cb', 'ee71d120-34aa-4659-9e4f-606cf2545935', '2024-03-22 20:25:15'),
( '88bbdeea-58d9-4cb4-a3ea-ae42107ad188', 'f6c936b2-54c9-49dc-84b9-664e3cded1e5', '2024-03-24 11:55:55'),
( 'b99e0a9c-0506-49e8-975e-50b15317d8a6', 'ee71d120-34aa-4659-9e4f-606cf2545935', '2024-03-27 11:20:00'),
( '9e16669a-45d5-4555-bd85-2b9e0016c245', 'f6c936b2-54c9-49dc-84b9-664e3cded1e5', '2024-03-26 13:40:00');

-- 18. TESTIMONI
INSERT INTO SIJARTA.TESTIMONI VALUES
('2217803d-3e5d-48cd-bb9e-c699e2e95a32', '2024-03-05', 'Pakaiannya jadi bersih sekali dan skill menyetrikanya sudah tidak diragukan lagi!', 5),
('3003a0d7-42d2-4044-857f-efd280b81397', '2024-03-07', 'hasilnya sangat bersih tapi sayangnya masih ada noda yang tertinggal.', 4),
('f39b91e4-bc61-47ae-a8cf-b9d20361fc9a', '2024-03-10', 'Hasilnya bagus sekali, dapur saya juga jadi bersih. Namun, pelayanannya lambat.', 3),
('97faede6-3306-4973-b69e-42762ba6b495', '2024-03-12', 'Layanan yang sangat baik dan ramah, dapur jadi kinclong. saya suka sekali!', 5),
('1d810223-e910-40b4-8e3c-9ecfd5269d16', '2024-03-15', 'Layanan tidak sesuai harapan. Dapur masih kotor.', 2),
('93a02b9a-a002-48c2-a9dc-76e9a64890cb', '2024-03-20', 'Rumah jadi bersih seperti rumah baru! Saya sangat merekomendasikan!', 5),
('88bbdeea-58d9-4cb4-a3ea-ae42107ad188', '2024-03-25', 'Harga terlalu mahal apabila dibandingkan hasil dari layanannya.', 3),
('9e16669a-45d5-4555-bd85-2b9e0016c245', '2024-03-01', 'Pelayanan cepat dan hasil cukup memuaskan!', 4),
('b99e0a9c-0506-49e8-975e-50b15317d8a6', '2024-03-05', 'Hasil bagus, tetapi masih ada noda di bagian bawah karpet', 3),
('c5213fe8-24cc-4daf-b162-943c85102c48', '2024-03-10', 'Sangat puas dengan hasil pelayanan yang diberikan.', 5),
('44139880-c1e2-4cfe-aba1-a8c67cdca616', '2024-04-12', 'Hasil oke, sofa dan karpet jadi bersih.', 4),
('c6f5c866-aa34-4b1e-b456-ac5266af305f', '2024-04-15', 'AC masih kotor, kualitas layanan tidak sesuai harga.', 2),
('c12afaa5-b4ba-4716-a848-48bc5a19112f', '2024-04-18', 'Hasil layanan yang sangat luar biasa! AC jadi bersih sekali.', 5),
('cc91d59d-59fe-4f5a-87b3-cb14d13dfed0', '2024-04-20', 'Hasil pencucian AC cukup oke, tetapi bisa diperbaiki', 3),
('09b9e4f9-b2e5-4799-b652-939637670ff8', '2024-04-25', 'Layanan pijat yang sangat baik, badan jadi tidak pegel. Sangat direkomendasikan!', 5),
('2d3642cc-6d9f-448a-9d30-8dbdc2b373b1', '2024-04-01', 'Hasilnya cukup oke, tidak ada yang istimewa.', 3),
('2217803d-3e5d-48cd-bb9e-c699e2e95a32', '2024-04-05', 'Pelayanan cepat dan hasilnya baik.', 4);
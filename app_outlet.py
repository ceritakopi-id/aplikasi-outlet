import streamlit as st
import pandas as pd
import datetime
import requests
import json

# Set konfigurasi halaman web
st.set_page_config(page_title="Sistem Operasional Outlet", layout="wide")

# URL Google Apps Script Anda (Sudah Terkunci Permanen)
API_URL = "https://script.google.com/macros/s/AKfycbwrQf1WcvsLbkaVLPTqULBSzp5bM_V3sGuKevJAawnXjn07e8ZGucyGAf0PVOC9qlsT/exec"

st.title("🏪 Aplikasi Gudang & Penjualan Outlet Kopi")
st.write("---")

# Data Master Pilihan (Sesuai file excel Anda)
OUTLETS = [
    "ArtMarketMKN", "BangsalMKN", "BellezaMKN", "Coffe Walk Puri", "EVENT PUPR", 
    "EventDPS", "EventJKT", "EventJKT2", "Happy Food Kemang", "ITC Depok", 
    "KutaBeachMKN", "Lvl21MKN", "MerdekaDPS", "PasarayaJKT", "PuputanMKN", 
    "SEMINYAK", "SanurMKN", "ScientiaMKN", "SegaraMKN", "TabananMKN", 
    "Taman Jajan Bintaro", "WahanaMKN"
]

MENUS = [
    "AMERICANO HOT", "AMERICANO HOT KINTAMANI", "AMERICANO ICED", "AMERICANO ICED KINTAMANI", 
    "AQUA 600 ML", "BLACK SPARKLE ICED", "BLACK YUZU HOT", "BLACK YUZU ICED", "BLACK YUZU KINTAMANI", 
    "CAPPUCCINO HOT", "CAPPUCCINO ICED", "CHOCO BTS", "CHOCO LATTE HOT", "CHOCO LATTE ICED", 
    "COFFEE LATTE HOT", "COFFEE LATTE ICED", "COFFEE LATTE ICED KINTAMANI", "ES BATU", "ES POTONG", 
    "EXTRA SHOT", "FRUIT PUNCH SPARKLE", "GOLDEN TWIST ICED", "HOT COFFEE MILK GULA AREN", 
    "ICED COFFEE BUTTERSCOTCH", "ICED COFFEE MILK GULA AREN", "ICED COFFEE MILK GULA AREN KINTAMANI", 
    "ICED COFFEE PANDAN", "ICED COFFEE SALT CARAMEL", "ICED LEMON TEA", "ICED LYCHEE TEA", 
    "LEMON SPARKLE", "LYCHEE COFFEE", "MATCHA BTS", "MATCHA LATTE HOT", "MATCHA LATTE ICED", 
    "MOCHACINO COFFEE", "PEPPERMINT YAKULT", "TARRO LATTE", "TULUS 330 ML", "TUMBLER"
]

BAHAN_BAKU = [
    "Cup Hot", "Cap Hot", "Cup Ice", "Cap Ice", "House Blend Bean", "Kintamani Bean", 
    "Susu", "Creamer", "Gula Aren", "Yuzu", "Butterscotch", "Salted Caramel", "Leci", 
    "Matcha", "Choco", "Taro", "Lemon Tea", "Fruit Punch", "Peppermint", "Pineapple", 
    "Pandan", "Nipis Madu", "Yakult", "Aqua", "Tulus", "Es Batu", "Es Potong", "Tumbler"
]

# Menu Navigasi Samping
st.sidebar.title("📌 Menu Kerja Harian")
menu_pilihan = st.sidebar.radio("Pilih Modul:", [
    "🛒 Input Penjualan Harian",
    "📥 Input Bahan Baku Masuk",
    "🔍 Stock Opname Harian (Malam)"
])

# 1. MODUL INPUT PENJUALAN
if menu_pilihan == "🛒 Input Penjualan Harian":
    st.subheader("Catat Produk Terjual Hari Ini")
    col1, col2 = st.columns(2)
    with col1:
        tgl = st.date_input("Tanggal Transaksi", datetime.date.today()).strftime("%Y-%m-%d")
        outlet = st.selectbox("Pilih Outlet", OUTLETS)
    with col2:
        menu_item = st.selectbox("Pilih Menu Terjual", MENUS)
        qty = st.number_input("Kuantitas (Qty)", min_value=1, value=1, step=1)
        
    if st.button("Kirim Penjualan ke Google Sheet"):
        payload = {
            "target_sheet": "penjualan",
            "data": [tgl, outlet, menu_item, qty]
        }
        try:
            res = requests.post(API_URL, data=json.dumps(payload))
            if res.status_code == 200:
                st.success(f"✅ Berhasil! Data penjualan [{menu_item} x{qty}] di {outlet} masuk ke Google Sheet.")
            else:
                st.error("❌ Gagal mengirim. Cek koneksi internet Anda.")
        except Exception as e:
            st.error(f"❌ Terjadi kesalahan jaringan: {e}")

# 2. MODUL INPUT BAHAN BAKU MASUK
elif menu_pilihan == "📥 Input Bahan Baku Masuk":
    st.subheader("Catat Bahan Baku Masuk / Pengiriman Stok")
    col1, col2 = st.columns(2)
    with col1:
        tgl_masuk = st.date_input("Tanggal Penerimaan", datetime.date.today()).strftime("%Y-%m-%d")
        outlet_terima = st.selectbox("Outlet Penerima", OUTLETS)
    with col2:
        bahan = st.selectbox("Nama Bahan Baku", BAHAN_BAKU)
        qty_masuk = st.number_input("Jumlah Masuk", min_value=1, value=100, step=1)
        
    if st.button("Kirim Laporan Stok Masuk"):
        payload = {
            "target_sheet": "stok_masuk",
            "data": [tgl_masuk, outlet_terima, bahan, qty_masuk]
        }
        try:
            res = requests.post(API_URL, data=json.dumps(payload))
            if res.status_code == 200:
                st.success(f"✅ Berhasil! Stok {bahan} sebanyak {qty_masuk} telah ditambahkan ke {outlet_terima}.")
            else:
                st.error("❌ Gagal mengirim stok masuk.")
        except Exception as e:
            st.error(f"❌ Terjadi kesalahan: {e}")

# 3. MODUL STOCK OPNAME HARIAN
elif menu_pilihan == "🔍 Stock Opname Harian (Malam)":
    st.subheader("Audit Fisik Tutup Toko Harian (Setiap Malam)")
    outlet_audit = st.selectbox("Pilih Outlet yang Diaudit Malam Ini", OUTLETS)
    tgl_audit = st.date_input("Tanggal Audit", datetime.date.today()).strftime("%Y-%m-%d")
    
    st.info("💡 Masukkan hasil timbangan atau hitungan fisik riil barang di toko malam ini:")
    
    opname_data = {}
    for b in BAHAN_BAKU:
        opname_data[b] = st.number_input(f"Sisa Fisik Aktual: {b}", min_value=0.0, value=0.0, step=1.0, key=f"op_{b}")
        
    if st.button("Kunci & Kirim Seluruh Data Opname Malam Ini"):
        success_count = 0
        with st.spinner("Sedang memproses seluruh bahan baku... Mohon tunggu..."):
            for bahan, stok_fisik in opname_data.items():
                payload = {
                    "target_sheet": "opname",
                    "data": [tgl_audit, outlet_audit, bahan, "Dihitung di Sheet", stok_fisik, "=E{row}-D{row}"]
                }
                try:
                    res = requests.post(API_URL, data=json.dumps(payload))
                    if res.status_code == 200:
                        success_count += 1
                except:
                    pass
            
        if success_count == len(BAHAN_BAKU):
            st.balloons()
            st.success(f"🎉 Selesai! Seluruh {len(BAHAN_BAKU)} data bahan baku di {outlet_audit} berhasil disinkronisasi ke tab 'opname'. Varian selisih otomatis terkunci.")
        else:
            st.warning(f"⚠️ Berhasil mengirim {success_count} dari {len(BAHAN_BAKU)} bahan baku. Periksa jaringan internet outlet Anda lalu coba kirim ulang jika ada data yang terlewat.")

import ee
import streamlit as st
import json

def initialize_gee():
    """
    Inisialisasi Google Earth Engine menggunakan Streamlit Secrets.
    Menangani konversi format kunci rahasia secara otomatis.
    """
    # 1. Periksa apakah secrets dengan nama 'gee_service_account' ada
    if "gee_service_account" in st.secrets:
        try:
            # Mengambil data dari secrets sebagai dictionary
            creds_dict = dict(st.secrets["gee_service_account"])
            
            # Membersihkan private_key:
            # Menangani jika ada karakter newline literal (\n) yang terbaca sebagai string
            if "private_key" in creds_dict:
                creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")
            
            # Membuat objek kredensial Service Account
            # json.dumps digunakan untuk memastikan data dikonversi ke format string JSON yang valid
            credentials = ee.ServiceAccountCredentials(
                creds_dict['client_email'],
                key_data=json.dumps(creds_dict)
            )
            
            # Inisialisasi GEE dengan kredensial dan Project ID
            project_id = creds_dict.get('project_id', 'ee-streamlit-mataram')
            ee.Initialize(credentials=credentials, project=project_id)
            
            st.success(f"✅ Terhubung ke Google Earth Engine (Project: {project_id})")
            return True

        except Exception as e:
            # Menampilkan pesan error jika autentikasi gagal
            st.error(f"❌ Gagal Autentikasi GEE: {e}")
            
            # Memberikan petunjuk perbaikan jika error spesifik muncul
            if "converted to bytes" in str(e).lower():
                st.info("💡 Tip: Pastikan format 'private_key' di Secrets sudah benar (gunakan tanda kutip tiga [\"\"\"] jika perlu).")
            
            return False
    else:
        # Tampilan jika Secrets belum diatur di Streamlit Cloud
        st.warning("⚠️ Secrets 'gee_service_account' tidak ditemukan.")
        st.info("Pastikan Anda sudah menambahkan Service Account Key di menu Settings > Secrets pada Streamlit Cloud.")
        
        # Opsi Mode Demo agar aplikasi tetap bisa terbuka
        if st.button("🎮 Jalankan Mode Demo (Data Simulasi)", key="demo_mode_btn"):
            st.session_state['demo_mode'] = True
            st.rerun()
            
        return False

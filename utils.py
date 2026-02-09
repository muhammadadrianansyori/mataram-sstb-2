import ee
import streamlit as st
import os
import json

def initialize_gee():
    """
    Inisialisasi Google Earth Engine dengan dukungan Streamlit Secrets (Cloud)
    dan fallback untuk penggunaan lokal.
    """
    
    # STRATEGI 1: Menggunakan Streamlit Secrets (WAJIB untuk Deploy di Cloud)
    # Pastikan di Settings > Secrets kamu pakai nama [gee_service_account]
    if "gee_service_account" in st.secrets:
        try:
            secret_info = dict(st.secrets["gee_service_account"])
            
            # Membersihkan format private_key agar karakter \n terbaca dengan benar
            if "private_key" in secret_info:
                secret_info["private_key"] = secret_info["private_key"].replace("\\n", "\n")
            
            # Membuat credentials dari data secrets
            credentials = ee.ServiceAccountCredentials(
                secret_info['client_email'], 
                key_data=json.dumps(secret_info)
            )
            
            # Inisialisasi dengan Project ID yang sesuai dari Secrets
            project_id = secret_info.get("project_id", "ee-streamlit-mataram")
            ee.Initialize(credentials=credentials, project=project_id)
            
            st.success(f"✅ Terhubung ke GEE via Secrets (Project: {project_id})")
            return True
            
        except Exception as e:
            st.error(f"❌ Gagal Auth via Secrets: {e}")
            # Jika gagal via secrets, lanjut ke strategi berikutnya
    
    # STRATEGI 2: Inisialisasi Standar (Untuk Lokal/Komputer Sendiri)
    try:
        # Coba inisialisasi default
        ee.Initialize()
        st.success("✅ Terhubung ke GEE (Metode Default)")
        return True
    except Exception as e:
        # STRATEGI 3: Inisialisasi dengan Nama Project Manual
        try:
            project_manual = "ee-streamlit-mataram"
            ee.Initialize(project=project_manual)
            st.success(f"✅ Terhubung ke GEE (Project: {project_manual})")
            return True
        except Exception as e2:
            st.warning(f"⚠️ GEE gagal inisialisasi: {e2}")

    # STRATEGI 4: Troubleshooting & Demo Mode
    st.error("❌ GEE Initialization Failed.")
    
    with st.expander("🔧 Cara Memperbaiki Error GEE"):
        st.markdown(f"""
        1.  **Cek Streamlit Secrets:** Pastikan judul di Secrets adalah `[gee_service_account]` (pakai kurung siku).
        2.  **Whitelist Service Account:** Pastikan email ini sudah terdaftar di Google Earth Engine:  
            `streamlit-access@ee-streamlit-mataram.iam.gserviceaccount.com`
        3.  **Project ID:** Pastikan project ID di Secrets adalah `ee-streamlit-mataram`.
        """)
        
    # Sediakan tombol demo jika GEE gagal total
    if st.button("🎮 Jalankan Mode Demo (Tanpa GEE Real-time)", key="utils_demo_btn"):
        st.session_state['use_dummy_data'] = True
        st.rerun()
        
    return False

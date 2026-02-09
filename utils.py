import ee
import streamlit as st
import json

def initialize_gee():
    if "gee_service_account" in st.secrets:
        try:
            # Mengambil data dari secrets
            creds_dict = dict(st.secrets["gee_service_account"])
            
            # Membersihkan karakter \n jika tersimpan sebagai teks
            if "private_key" in creds_dict:
                creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")
            
            # Inisialisasi menggunakan Service Account Credentials
            # Kita menggunakan json.dumps untuk memastikan data dikonversi ke bytes dengan benar
            credentials = ee.ServiceAccountCredentials(
                creds_dict['client_email'],
                key_data=json.dumps(creds_dict)
            )
            
            ee.Initialize(credentials=credentials, project=creds_dict['project_id'])
            st.success(f"✅ Berhasil! Terhubung ke GEE (Project: {creds_dict['project_id']})")
            return True

        except Exception as e:
            st.error(f"❌ Autentikasi GEE Gagal: {e}")
            return False
    
    st.warning("⚠️ Konfigurasi GEE (Secrets) belum ditemukan.")
    return False

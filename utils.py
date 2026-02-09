import ee
import streamlit as st
import json

def initialize_gee():
    if "gee_service_account" in st.secrets:
        try:
            creds_dict = dict(st.secrets["gee_service_account"])
            
            # Membersihkan karakter escape yang sering merusak kunci
            if "private_key" in creds_dict:
                creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")
            
            # Inisialisasi Kredensial secara manual agar lebih stabil
            from google.oauth2 import service_account
            
            # GEE butuh JSON string untuk key_data
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

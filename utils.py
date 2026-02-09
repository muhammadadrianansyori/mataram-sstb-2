import ee
import streamlit as st
import json

def initialize_gee():
    if "gee_service_account" in st.secrets:
        try:
            # Ambil data dari secrets
            s = st.secrets["gee_service_account"]
            
            # Buat dictionary baru agar kita bisa memodifikasi isinya
            creds_dict = {
                "type": s["type"],
                "project_id": s["project_id"],
                "private_key_id": s["private_key_id"],
                "private_key": s["private_key"].replace("\\n", "\n"), # Paksa perbaikan baris baru
                "client_email": s["client_email"],
                "client_id": s["client_id"],
                "auth_uri": s["auth_uri"],
                "token_uri": s["token_uri"],
                "auth_provider_x509_cert_url": s["auth_provider_x509_cert_url"],
                "client_x509_cert_url": s["client_x509_cert_url"]
            }
            
            # Gunakan ServiceAccountCredentials secara langsung
            credentials = ee.ServiceAccountCredentials(
                creds_dict['client_email'],
                key_data=json.dumps(creds_dict)
            )
            
            ee.Initialize(credentials=credentials, project=creds_dict['project_id'])
            st.success(f"✅ GEE Connected: {creds_dict['project_id']}")
            return True

        except Exception as e:
            st.error(f"❌ Autentikasi Gagal: {e}")
            return False
    
    st.warning("⚠️ Secrets tidak ditemukan.")
    return False

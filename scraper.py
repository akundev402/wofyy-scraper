import os
import requests
from bs4 import BeautifulSoup
from supabase import create_client, Client

# Koneksi ke Supabase menggunakan Environment Variables (Nanti kita setting di GitHub)
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def run_scraper():
    print("Memulai proses scraping data komik...")
    
    # CONTOH: Kita ambil data dari web sumber (Contoh target uji coba)
    # Anda bisa mengganti URL ini nanti dengan target situs komik pilihan Anda
    target_url = "https://bato.to/" # atau situs komik lain
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    try:
        response = requests.get(target_url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Contoh logika mengambil elemen komik (disesuaikan dengan target web)
            # Ini adalah kerangka dasar untuk menyimpan data ke Supabase
            sample_comic = {
                "title": "Contoh Judul Otomatis",
                "cover_url": "https://via.placeholder.com/150",
                "chapter": "Ch. 1",
                "type": "manhwa",
                "source_url": target_url
            }
            
            # Masukkan ke database Supabase tabel 'comics'
            data, count = supabase.table("comics").insert(sample_comic).execute()
            print("Berhasil memasukkan data ke Supabase:", data)
        else:
            print("Gagal mengakses situs target, status code:", response.status_code)
            
    except Exception as e:
        print("Terjadi error:", str(e))

if __name__ == "__main__":
    run_scraper()


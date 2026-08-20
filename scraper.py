import os
import requests
from bs4 import BeautifulSoup
from supabase import create_client, Client
import time

# Inisialisasi Koneksi Supabase
supabase: Client = create_client(os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_KEY"))

def scrape_doujindesu(url):
    # Header yang kuat untuk menyamarkan bot menjadi browser asli
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://www.google.com/"
    }
    
    print(f"Mencoba mengakses: {url}")
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            print(f"Gagal! Status code: {response.status_code}")
            return

        soup = BeautifulSoup(response.text, 'html.parser')
        
        # PERHATIAN: Selector ini mungkin perlu disesuaikan 
        # karena ini adalah URL halaman utama (Home), bukan URL spesifik satu komik.
        # Untuk sementara kita ambil judul pertama yang muncul.
        
        title_element = soup.select_one('h3.title') or soup.select_one('.entry-title')
        title = title_element.text.strip() if title_element else "Judul Uji Coba (Elemen tidak ditemukan)"
        
        img_element = soup.select_one('.thumb img') or soup.select_one('img')
        cover_url = img_element.get('src') if img_element else ""
        
        data = {
            "title": title,
            "cover_url": cover_url,
            "source_url": url,
            "is_18plus": True
        }
        
        print(f"Data yang akan dikirim: {data}")
        
        # Kirim ke database
        supabase.table("comics").insert(data).execute()
        print(f"✅ Sukses menyimpan data ke database!")
        
    except Exception as e:
        print(f"❌ Error saat menjalankan skrip: {e}")

if __name__ == "__main__":
    target_url = "https://doujin.desu.xxx/?ref=porndude"
    scrape_doujindesu(target_url)

# 📦 Pasca Panen Krisan
# Panduan panen, grading, dan perpanjangan vase life

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Pasca Panen", page_icon="📦", layout="wide")

st.markdown("## 📦 Teknologi Pasca Panen Krisan Spray")
st.info("Panduan pemanenan, grading, handling, dan teknik perpanjangan vase life untuk bunga potong berkualitas.")

tab1, tab2, tab3, tab4 = st.tabs(["✂️ Teknik Panen", "📊 Grading", "💧 Vase Life", "📦 Packing & Distribusi"])

# TAB 1: Teknik Panen
with tab1:
    st.subheader("✂️ Teknik Pemanenan Krisan Spray")
    
    st.markdown("""
    ### ⏰ Waktu Panen Optimal
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Waktu Terbaik:**
        - Pagi hari: 06.00 - 09.00 WIB
        - Sore hari: 15.00 - 17.00 WIB
        - **HINDARI:** Tengah hari saat terik!
        
        **Kondisi Bunga:**
        - 2-3 kuntum sudah mekar penuh (untuk spray)
        - Kuntum lain masih kuncup berwarna
        - Hindari panen saat bunga basah embun/hujan
        """)
    
    with col2:
        st.markdown("""
        **Peralatan:**
        - Pisau/gunting tajam & steril
        - Ember berisi air bersih + preservative
        - Keranjang pengangkut (hindari menumpuk)
        - Sarung tangan (opsional)
        
        **Cara Potong:**
        - Potong miring 45° untuk area penyerapan lebih besar
        - Sisakan minimal 2 ruas daun di tanaman
        - Langsung masukkan ke air!
        """)
    
    st.warning("⚠️ **PENTING:** Jangan biarkan tangkai bunga terkena udara lebih dari 30 detik! Air embolism akan mengurangi vase life.")
    
    st.markdown("---")
    
    st.markdown("### 📏 Standar Panjang Tangkai")
    
    length_data = pd.DataFrame({
        "Grade": ["Super", "A", "B", "C"],
        "Panjang (cm)": ["80-90", "70-80", "60-70", "50-60"],
        "Kuntum Mekar": ["3-4", "2-3", "2-3", "1-2"],
        "Target Pasar": ["Ekspor, hotel", "Florist premium", "Florist umum", "Pasar tradisional"]
    })
    
    st.dataframe(length_data, use_container_width=True, hide_index=True)

# TAB 2: Grading
with tab2:
    st.subheader("📊 Sistem Grading Krisan Spray")
    
    st.markdown("""
    Grading yang konsisten = harga premium dan kepuasan pelanggan!
    """)
    
    grading_criteria = pd.DataFrame({
        "Kriteria": ["Panjang Tangkai", "Jumlah Kuntum", "Ukuran Kuntum", "Kesegaran", 
                     "Kerusakan/Cacat", "Keseragaman Warna", "Daun"],
        "Grade Super": ["80-90 cm", "7-10 kuntum", ">5 cm diameter", "Turgid, segar", 
                        "0%", "100% seragam", "Hijau segar, lengkap"],
        "Grade A": ["70-80 cm", "5-7 kuntum", "4-5 cm diameter", "Turgid", 
                    "<5%", ">95% seragam", "Hijau, sedikit bercak OK"],
        "Grade B": ["60-70 cm", "4-5 kuntum", "3-4 cm diameter", "Cukup segar", 
                    "<10%", ">90% seragam", "Minor yellowing OK"],
        "Reject": ["<60 cm", "<4 kuntum", "<3 cm", "Layu", 
                   ">10%", "Tidak seragam", "Rusak/kuning"]
    })
    
    st.dataframe(grading_criteria, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    st.markdown("### 💰 Estimasi Harga per Grade")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Super", "Rp 15.000-20.000", "/tangkai")
    with col2:
        st.metric("Grade A", "Rp 10.000-15.000", "/tangkai")
    with col3:
        st.metric("Grade B", "Rp 7.000-10.000", "/tangkai")
    with col4:
        st.metric("Grade C", "Rp 4.000-7.000", "/tangkai")
    
    st.info("💡 **Tips:** Konsistensi grading yang ketat akan membangun reputasi dan pelanggan loyal!")

# TAB 3: Vase Life
with tab3:
    st.subheader("💧 Teknik Perpanjangan Vase Life")
    
    st.success("""
    **Target Vase Life Krisan Spray:** 10-16 hari
    
    Dengan handling yang benar, krisan bisa bertahan hingga 3 minggu!
    """)
    
    st.markdown("### 🧪 Larutan Preservative")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Formula Komersial:**
        - Chrysal, Floralife, atau merek lain
        - Ikuti dosis pada kemasan
        - Ganti larutan setiap 2-3 hari
        
        **Kandungan Utama:**
        - Sukrosa (gula) - sumber energi
        - Biocide - mencegah bakteri
        - Acidifier - menurunkan pH
        """)
    
    with col2:
        st.markdown("""
        **Formula Sederhana (DIY):**
        
        Per 1 Liter air:
        - Gula pasir: 20 gram (2 sendok makan)
        - Cuka: 2 ml (atau asam sitrat 0.5g)
        - Pemutih (bleach): 0.2 ml (3-4 tetes)
        
        *pH target: 3.5-4.5*
        """)
    
    st.markdown("---")
    
    st.markdown("### 🌡️ Pendinginan (Cold Chain)")
    
    st.markdown("""
    | Tahap | Suhu | Durasi | Tujuan |
    |-------|------|--------|--------|
    | Hydration awal | 2-4°C | 2-4 jam | Rehidrasi cepat, turunkan suhu lapang |
    | Cold storage | 2-4°C | Maks 7 hari | Penyimpanan sebelum distribusi |
    | Display (florist) | 8-12°C | 3-5 hari | Showcase untuk pembeli |
    | Rumah konsumen | 18-22°C | 7-14 hari | Nikmati bunga! |
    """)
    
    st.error("🚨 **JANGAN** simpan krisan bersama buah/sayur yang menghasilkan etilen (apel, pisang, tomat)!")
    
    st.markdown("---")
    
    st.markdown("### 📋 SOP Handling Pasca Panen")
    
    with st.expander("📋 Langkah-langkah Detail", expanded=True):
        st.markdown("""
        1. **Panen** → Potong miring 45°, langsung masuk air
        2. **Transportasi ke packing house** → Dalam air, tutup dari matahari
        3. **Re-cut** → Potong ulang 2-3 cm dalam air
        4. **Grading** → Sortir per grade, ikat per bunch (10 tangkai)
        5. **Hydration** → Rendam di larutan preservative + cold water 2-4 jam
        6. **Packing** → Wrapping + box
        7. **Cold storage** → 2-4°C hingga siap kirim
        8. **Distribusi** → Truk berpendingin atau kirim pagi hari
        """)

# TAB 4: Packing
with tab4:
    st.subheader("📦 Packing & Distribusi")
    
    st.markdown("### 📦 Jenis Kemasan")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **1. Bunch Wrapping**
        - 10 tangkai per bunch
        - Wrapping: Plastik OPP/BOPP transparan
        - Label: Nama produk, grade, tanggal panen
        - Cocok untuk: Florist, grosir
        
        **2. Box Kardus**
        - Kapasitas: 20-50 bunch per box
        - Material: Kardus bergelombang, ventilasi
        - Liner: Plastik PE untuk menjaga kelembaban
        - Cocok untuk: Distribusi jarak jauh
        """)
    
    with col2:
        st.markdown("""
        **3. Bucket System**
        - Bucket plastik + air preservative
        - Kapasitas: 10-20 bunch per bucket
        - Tutup untuk transportasi
        - Cocok untuk: Jarak dekat, florist
        
        **4. Sleeve Individual**
        - Wrapping per tangkai (premium)
        - Untuk retail supermarket
        - Include sachet preservative mini
        """)
    
    st.markdown("---")
    
    st.markdown("### 🚚 Tips Distribusi")
    
    st.markdown("""
    | Jarak | Metode | Suhu | Durasi Aman |
    |-------|--------|------|-------------|
    | <50 km | Pickup terbuka + tutup | Ambient | 2-3 jam (pagi) |
    | 50-200 km | Mobil box tertutup | 8-15°C | 4-6 jam |
    | >200 km / antar pulau | Truk reefer / pesawat | 2-4°C | 24-48 jam |
    """)
    
    st.warning("⚠️ Pastikan bunga tidak terkena sinar matahari langsung selama transportasi!")
    
    st.markdown("---")
    
    st.markdown("### 🏪 Channel Penjualan")
    
    channels = pd.DataFrame({
        "Channel": ["Florist Retail", "Event Organizer", "Dekorasi Hotel/Kantor", 
                    "Pasar Bunga Tradisional", "Online/E-commerce", "Ekspor"],
        "Karakteristik": ["Order teratur, grade campuran", "Order besar musiman (wedding)", 
                          "Kontrak bulanan, kualitas stabil", "Volume besar, harga kompetitif",
                          "Packaging premium, individual", "Sertifikasi, cold chain ketat"],
        "Margin": ["Sedang", "Tinggi", "Sedang-Tinggi", "Rendah", "Tinggi", "Sangat Tinggi"]
    })
    
    st.dataframe(channels, use_container_width=True, hide_index=True)

# Footer
st.markdown("---")
st.caption("🌸 Budidaya Krisan Pro - Teknologi Pasca Panen")

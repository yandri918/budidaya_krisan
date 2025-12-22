# 🌸 Panduan Budidaya Krisan Spray Jepang
# SOP Lengkap dari Hulu hingga Hilir

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Panduan Budidaya Krisan",
    page_icon="🌸",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #ec4899 0%, #f472b6 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sop-card {
        background: linear-gradient(135deg, rgba(252, 231, 243, 0.8) 0%, rgba(255, 255, 255, 0.9) 100%);
        border: 1px solid rgba(236, 72, 153, 0.2);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    .phase-title {
        color: #be185d;
        font-weight: 700;
        font-size: 1.2rem;
        border-bottom: 2px solid #f9a8d4;
        padding-bottom: 0.5rem;
        margin-bottom: 1rem;
    }
    .timeline-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        background: #fce7f3;
        border-radius: 20px;
        font-size: 0.8rem;
        color: #be185d;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🌸 Panduan Budidaya Krisan Spray Jepang</h1>
    <p>SOP Lengkap dari Hulu hingga Hilir | Berbasis Riset & Praktik Petani</p>
</div>
""", unsafe_allow_html=True)

# ========== DATABASE VARIETAS ==========
KRISAN_VARIETIES = {
    "Krisan Spray Putih": {
        "emoji": "🤍",
        "color_code": "#ffffff",
        "market_price_min": 8000,
        "market_price_max": 15000,
        "demand": "Tinggi - Wedding, duka cita, formal",
        "vase_life": "10-14 hari",
        "characteristics": "Bunga spray dengan banyak kuntum, diameter 4-6 cm per kuntum",
        "best_season": "Sepanjang tahun, peak Desember-Februari"
    },
    "Krisan Spray Pink": {
        "emoji": "💗",
        "color_code": "#ec4899",
        "market_price_min": 10000,
        "market_price_max": 18000,
        "demand": "Sangat Tinggi - Valentine, ulang tahun, romantis",
        "vase_life": "12-16 hari",
        "characteristics": "Warna cerah, favorit florist, multi-kuntum",
        "best_season": "Peak Februari (Valentine), Mei (Mother's Day)"
    },
    "Krisan Spray Kuning": {
        "emoji": "💛",
        "color_code": "#fbbf24",
        "market_price_min": 8000,
        "market_price_max": 14000,
        "demand": "Tinggi - Imlek, dekorasi, cheerful occasion",
        "vase_life": "10-14 hari",
        "characteristics": "Warna cheerful, cocok rangkaian tropikal",
        "best_season": "Peak Januari-Februari (Imlek)"
    }
}

# ========== TABS ==========
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📋 Database Varietas",
    "🌱 Persiapan & Stek",
    "🌿 Fase Vegetatif",
    "🌸 Fase Generatif",
    "💡 Pengaturan Cahaya",
    "🧪 Pemupukan",
    "📅 Timeline Lengkap"
])

# TAB 1: Database Varietas
with tab1:
    st.subheader("📋 Database Varietas Krisan Spray Jepang")
    st.info("Krisan Spray Jepang terkenal dengan kualitas bunga yang tahan lama dan banyak kuntum per tangkai.")
    
    for name, data in KRISAN_VARIETIES.items():
        with st.expander(f"{data['emoji']} {name}", expanded=True):
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.markdown(f"""
                <div style="background: {data['color_code']}; 
                            width: 100px; height: 100px; 
                            border-radius: 50%; 
                            border: 3px solid #e5e7eb;
                            margin: 0 auto;"></div>
                """, unsafe_allow_html=True)
                st.metric("Harga Pasar", f"Rp {data['market_price_min']:,}-{data['market_price_max']:,}/tangkai")
            
            with col2:
                st.markdown(f"**Karakteristik:** {data['characteristics']}")
                st.markdown(f"**Permintaan:** {data['demand']}")
                st.markdown(f"**Vase Life:** {data['vase_life']}")
                st.markdown(f"**Musim Peak:** {data['best_season']}")

# TAB 2: Persiapan & Stek
with tab2:
    st.subheader("🌱 Fase 1: Persiapan Lahan & Stek")
    st.markdown('<span class="timeline-badge">📅 Hari 0 - 21</span>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="sop-card">
        <div class="phase-title">🏗️ A. Persiapan Greenhouse & Bedengan</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **1. Syarat Lokasi:**
        - Ketinggian: **800 - 1.500 mdpl** (ideal 1.000-1.200 mdpl)
        - Suhu: 18-24°C siang, 15-18°C malam
        - Intensitas cahaya: 40.000-60.000 lux
        - Tersedia sumber air bersih
        
        **2. Konstruksi Greenhouse:**
        - Tipe: Tunnel atau multispan
        - Tinggi: minimal 4 meter
        - Material: Plastik UV 14% atau paranet
        - Ventilasi samping yang bisa dibuka-tutup
        """)
    
    with col2:
        st.markdown("""
        **3. Persiapan Bedengan:**
        - Lebar: 100-120 cm
        - Tinggi: 20-30 cm
        - Jarak antar bedengan: 40-50 cm
        - Sterilisasi tanah: fumigasi atau solarisasi 2-3 minggu
        
        **4. Media Tanam:**
        - Tanah : Sekam bakar : Pupuk kandang = 2:1:1
        - pH optimal: 6.0 - 6.5
        - EC: 1.5 - 2.5 mS/cm
        """)
    
    st.markdown("---")
    
    st.markdown("""
    <div class="sop-card">
        <div class="phase-title">✂️ B. Persiapan Stek (Cutting)</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    | Parameter | Standar |
    |-----------|---------|
    | Sumber stek | Tanaman induk sehat, bebas virus |
    | Panjang stek | 5-7 cm dengan 3-4 daun |
    | Diameter batang | 3-5 mm |
    | Pemotongan | Gunakan pisau tajam, steril |
    | Hormon akar | IBA 1000-2000 ppm (celup 5 detik) |
    | Media rooting | Pasir steril atau rockwool |
    | Waktu rooting | 14-21 hari |
    | Kelembaban | 85-95% (gunakan misting) |
    """)
    
    st.success("✅ **Target:** Stek berakar dengan akar 3-5 cm, siap dipindah ke bedengan produksi.")

# TAB 3: Fase Vegetatif
with tab3:
    st.subheader("🌿 Fase 2: Pertumbuhan Vegetatif")
    st.markdown('<span class="timeline-badge">📅 Hari 21 - 49 (4 minggu)</span>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="sop-card">
        <div class="phase-title">🌱 Transplanting & Pemeliharaan Vegetatif</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **1. Pindah Tanam (Transplanting):**
        - Waktu: Sore hari (hindari terik)
        - Jarak tanam: 12.5 x 12.5 cm (64 tanaman/m²)
        - Kedalaman: 2-3 cm
        - Siram segera setelah tanam
        
        **2. Pencahayaan Fase Vegetatif:**
        - **PENTING:** Berikan hari panjang (Long Day)
        - Durasi: **16-18 jam cahaya/hari**
        - Gunakan lampu TL/LED 100-150 lux
        - Penyinaran malam: 22.00 - 02.00 WIB
        """)
    
    with col2:
        st.markdown("""
        **3. Pemeliharaan:**
        - Penyiraman: 2x sehari (pagi & sore)
        - EC nutrisi: 1.5-2.0 mS/cm
        - Pinching (potong pucuk): Minggu ke-2 setelah tanam
        - Jumlah cabang dipertahankan: 3-4 cabang/tanaman
        
        **4. Target Vegetatif:**
        - Tinggi tanaman: 25-30 cm
        - Jumlah daun: 15-20 helai
        - Batang kokoh, hijau tua
        """)
    
    st.warning("⚠️ **Kritis:** Fase vegetatif menentukan jumlah cabang produktif. Pinching yang tepat menghasilkan banyak kuntum bunga!")
    
    # Visualization: Pinching diagram
    st.markdown("### 📐 Teknik Pinching")
    st.image("https://via.placeholder.com/600x200/fce7f3/be185d?text=Diagram+Pinching+Krisan", 
             caption="Ilustrasi: Potong pucuk utama untuk merangsang cabang lateral", 
             use_container_width=True) if False else st.info("💡 Potong pucuk utama menyisakan 4-5 ruas untuk menghasilkan 3-4 cabang produktif.")

# TAB 4: Fase Generatif
with tab4:
    st.subheader("🌸 Fase 3: Pembungaan (Generatif)")
    st.markdown('<span class="timeline-badge">📅 Hari 49 - 105 (8 minggu)</span>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="sop-card">
        <div class="phase-title">💡 Induksi Pembungaan dengan Hari Pendek</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.error("🔴 **KRITIS:** Krisan adalah tanaman **short day plant**. Pembungaan HANYA terjadi jika hari pendek (<12 jam cahaya)!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **1. Induksi Hari Pendek (Short Day):**
        - Durasi cahaya: **10-11 jam/hari MAKSIMAL**
        - Metode: Penutupan dengan plastik hitam
        - Waktu tutup: 17.00 - 07.00 WIB (14 jam gelap)
        - Lakukan KONSISTEN selama 8 minggu
        
        **2. Timeline Pembungaan:**
        - Minggu 1-2: Inisiasi tunas bunga
        - Minggu 3-4: Kuncup mulai terlihat
        - Minggu 5-6: Kuncup membesar
        - Minggu 7-8: Bunga mulai mekar
        """)
    
    with col2:
        st.markdown("""
        **3. Parameter Lingkungan:**
        - Suhu siang: 20-24°C
        - Suhu malam: 15-18°C (PENTING untuk warna)
        - Kelembaban: 60-70%
        - EC nutrisi: 2.0-2.5 mS/cm
        
        **4. Peningkatan Kualitas Bunga:**
        - Kurangi N, tingkatkan K di minggu ke-6
        - Suhu malam rendah → warna lebih intens
        - Jaga konsistensi tutup plastik hitam
        """)
    
    st.markdown("---")
    
    st.markdown("""
    <div class="sop-card">
        <div class="phase-title">🎯 Disbudding (Pembuangan Kuncup Samping)</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    Untuk krisan **spray**, TIDAK perlu disbudding karena kita ingin banyak kuntum per tangkai.
    
    Tetapi untuk krisan **standard** (satu bunga besar), lakukan disbudding:
    - Buang semua kuncup samping, sisakan hanya kuncup terminal
    - Lakukan saat kuncup masih kecil (<5mm)
    """)

# TAB 5: Pengaturan Cahaya
with tab5:
    st.subheader("💡 Pengaturan Photoperiod (Hari Panjang vs Pendek)")
    
    st.info("""
    **Konsep Dasar:**
    - Krisan adalah **Short Day Plant** (SDP)
    - Vegetatif membutuhkan **hari panjang** (>14 jam cahaya)
    - Pembungaan membutuhkan **hari pendek** (<12 jam cahaya)
    - Di Indonesia (dekat ekuator), hari alami ~12 jam → perlu manipulasi!
    """)
    
    # Timeline visualization
    st.markdown("### 📊 Jadwal Photoperiod")
    
    schedule_data = {
        "Minggu": list(range(1, 16)),
        "Fase": ["Rooting"]*3 + ["Vegetatif"]*4 + ["Generatif"]*8,
        "Jam Cahaya": [16]*3 + [16]*4 + [10]*8,
        "Perlakuan": ["Lampu malam"]*3 + ["Lampu malam"]*4 + ["Tutup plastik hitam"]*8
    }
    
    df = pd.DataFrame(schedule_data)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df["Minggu"],
        y=df["Jam Cahaya"],
        marker_color=['#86efac' if x >= 14 else '#f472b6' for x in df["Jam Cahaya"]],
        text=df["Jam Cahaya"].astype(str) + " jam",
        textposition='outside'
    ))
    
    fig.update_layout(
        title="Durasi Cahaya per Minggu",
        xaxis_title="Minggu ke-",
        yaxis_title="Jam Cahaya/Hari",
        yaxis_range=[0, 20],
        height=400,
        showlegend=False
    )
    
    fig.add_hline(y=12, line_dash="dash", line_color="red", 
                  annotation_text="Batas Kritis (12 jam)")
    
    st.plotly_chart(fig, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🌙 Teknik Perpanjangan Hari (Long Day)
        **Tujuan:** Memperpanjang fase vegetatif
        
        **Metode:**
        1. Pasang lampu di atas bedengan (tinggi 2m)
        2. Jenis lampu: LED putih atau TL 40W
        3. Intensitas: 100-150 lux
        4. Jadwal: 22.00 - 02.00 WIB (4 jam tambahan)
        5. Jarak lampu: setiap 2-3 meter
        """)
    
    with col2:
        st.markdown("""
        ### 🌑 Teknik Hari Pendek (Short Day)
        **Tujuan:** Memicu pembungaan
        
        **Metode:**
        1. Gunakan plastik hitam 0.3-0.5 mm
        2. Konstruksi: Rangka besi/bambu + plastik
        3. Tutup: 17.00 WIB (sebelum matahari terbenam)
        4. Buka: 07.00 WIB (setelah matahari terbit)
        5. Wajib konsisten setiap hari!
        """)

# TAB 6: Pemupukan
with tab6:
    st.subheader("🧪 Program Pemupukan Krisan Spray")
    
    st.markdown("""
    <div class="sop-card">
        <div class="phase-title">📊 Kebutuhan Nutrisi per Fase</div>
    </div>
    """, unsafe_allow_html=True)
    
    fertilizer_program = pd.DataFrame({
        "Fase": ["Rooting (0-3 minggu)", "Vegetatif Awal (3-5 minggu)", 
                 "Vegetatif Akhir (5-7 minggu)", "Generatif Awal (7-11 minggu)",
                 "Generatif Akhir (11-15 minggu)"],
        "N-P-K Ratio": ["10-52-10", "20-10-20", "15-10-30", "10-10-30", "5-10-40"],
        "EC (mS/cm)": ["0.8-1.0", "1.5-1.8", "1.8-2.0", "2.0-2.2", "2.0-2.5"],
        "Frekuensi": ["1x/minggu", "2x/minggu", "2x/minggu", "3x/minggu", "3x/minggu"],
        "Catatan": [
            "Fokus akar, P tinggi",
            "Dorong pertumbuhan vegetatif",
            "Transisi ke K tinggi",
            "Pembentukan bunga",
            "Kualitas & warna bunga"
        ]
    })
    
    st.dataframe(fertilizer_program, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    st.markdown("### 🧪 Contoh Formulasi Pupuk")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **Fase Vegetatif:**
        - NPK 20-10-20: 2 g/L
        - Kalsium Nitrat: 1 g/L
        - MgSO4: 0.5 g/L
        - Mikro: sesuai label
        """)
    
    with col2:
        st.markdown("""
        **Fase Generatif:**
        - NPK 10-10-30: 2 g/L
        - KNO3: 1 g/L
        - MgSO4: 0.5 g/L
        - Boron: 0.1 g/L
        """)
    
    with col3:
        st.markdown("""
        **Finishing:**
        - KCl / K2SO4: 2 g/L
        - Kalsium: 0.5 g/L
        - Kurangi N drastis
        - Fokus warna & kekerasan
        """)
    
    st.warning("⚠️ **Penting:** Selalu cek pH larutan (6.0-6.5) dan EC sebelum aplikasi!")

# TAB 7: Timeline Lengkap
with tab7:
    st.subheader("📅 Timeline Lengkap Budidaya Krisan Spray")
    
    st.info("Total durasi: **105-120 hari** dari stek hingga panen")
    
    # Interactive timeline
    timeline_data = [
        {"Minggu": "0-3", "Hari": "0-21", "Fase": "Rooting", "Aktivitas": "Persiapan stek, pembentukan akar", "Warna": "#86efac"},
        {"Minggu": "3-4", "Hari": "21-28", "Fase": "Transplanting", "Aktivitas": "Pindah tanam ke bedengan produksi", "Warna": "#4ade80"},
        {"Minggu": "4-5", "Hari": "28-35", "Fase": "Vegetatif 1", "Aktivitas": "Pinching, pembentukan cabang", "Warna": "#22c55e"},
        {"Minggu": "5-7", "Hari": "35-49", "Fase": "Vegetatif 2", "Aktivitas": "Pertumbuhan cabang, lampu malam ON", "Warna": "#16a34a"},
        {"Minggu": "7-9", "Hari": "49-63", "Fase": "Inisiasi Bunga", "Aktivitas": "Mulai tutup plastik hitam, tunas bunga", "Warna": "#f9a8d4"},
        {"Minggu": "9-11", "Hari": "63-77", "Fase": "Kuncup Terlihat", "Aktivitas": "Kuncup membesar, naikkan K", "Warna": "#f472b6"},
        {"Minggu": "11-13", "Hari": "77-91", "Fase": "Pematangan", "Aktivitas": "Bunga mulai berwarna, finishing", "Warna": "#ec4899"},
        {"Minggu": "13-15", "Hari": "91-105", "Fase": "Panen", "Aktivitas": "Panen saat 2-3 kuntum mekar/tangkai", "Warna": "#be185d"},
    ]
    
    for item in timeline_data:
        st.markdown(f"""
        <div style="display: flex; align-items: center; margin: 0.5rem 0; padding: 1rem; 
                    background: {item['Warna']}20; border-left: 4px solid {item['Warna']}; 
                    border-radius: 8px;">
            <div style="min-width: 100px; font-weight: bold; color: {item['Warna']};">
                Minggu {item['Minggu']}<br>
                <small style="color: #6b7280;">Hari {item['Hari']}</small>
            </div>
            <div style="margin-left: 1rem;">
                <strong>{item['Fase']}</strong><br>
                <span style="color: #4b5563;">{item['Aktivitas']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Harvest date calculator
    st.markdown("### 🧮 Kalkulator Tanggal Panen")
    
    start_date = st.date_input("Tanggal mulai stek:", datetime.now())
    
    if start_date:
        harvest_start = start_date + timedelta(days=98)
        harvest_end = start_date + timedelta(days=112)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Mulai Tutup Plastik", (start_date + timedelta(days=49)).strftime('%d %B %Y'))
        with col2:
            st.metric("Estimasi Panen Awal", harvest_start.strftime('%d %B %Y'))
        with col3:
            st.metric("Estimasi Panen Akhir", harvest_end.strftime('%d %B %Y'))
        
        st.success(f"🌸 Bunga siap panen antara **{harvest_start.strftime('%d %B')}** hingga **{harvest_end.strftime('%d %B %Y')}**")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #9ca3af; font-size: 0.8rem;">
    🌸 Budidaya Krisan Pro | Panduan berbasis riset dan praktik petani Indonesia
</div>
""", unsafe_allow_html=True)

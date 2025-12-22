# 🌸 Budidaya Krisan Pro - Home Page
# Modern Streamlit Dashboard for Chrysanthemum Cultivation

import streamlit as st
from datetime import datetime

# ========== PAGE CONFIG ==========
st.set_page_config(
    page_title="Budidaya Krisan Pro",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== CUSTOM STYLING ==========
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Modern Gradient Background */
    .stApp {
        background: linear-gradient(135deg, #f0fdf4 0%, #ecfdf5 50%, #f9fafb 100%);
    }
    
    /* Hero Section */
    .hero-container {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.08) 0%, rgba(255, 255, 255, 0.9) 100%);
        backdrop-filter: blur(10px);
        border-radius: 24px;
        padding: 3rem 2rem;
        text-align: center;
        border: 1px solid rgba(16, 185, 129, 0.2);
        box-shadow: 0 20px 40px rgba(16, 185, 129, 0.08);
        margin-bottom: 2rem;
    }
    
    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #064e3b 0%, #059669 50%, #10b981 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .hero-subtitle {
        font-size: 1.1rem;
        color: #6b7280;
        max-width: 600px;
        margin: 0 auto;
    }
    
    /* Glass Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(16, 185, 129, 0.15);
        border-radius: 20px;
        padding: 1.5rem;
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(16, 185, 129, 0.12);
        border-color: rgba(16, 185, 129, 0.3);
    }
    
    .card-icon {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    
    .card-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #065f46;
        margin-bottom: 0.5rem;
    }
    
    .card-desc {
        font-size: 0.9rem;
        color: #6b7280;
    }
    
    /* Variety Cards */
    .variety-card {
        text-align: center;
        padding: 1.5rem;
        border-radius: 16px;
        transition: all 0.3s ease;
    }
    
    .variety-white {
        background: linear-gradient(135deg, #f9fafb 0%, #ffffff 100%);
        border: 2px solid #e5e7eb;
    }
    
    .variety-pink {
        background: linear-gradient(135deg, #fce7f3 0%, #fbcfe8 100%);
        border: 2px solid #f9a8d4;
    }
    
    .variety-yellow {
        background: linear-gradient(135deg, #fef9c3 0%, #fef08a 100%);
        border: 2px solid #fde047;
    }
    
    /* Badges */
    .badge {
        display: inline-block;
        padding: 0.4rem 1rem;
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        border-radius: 50px;
        font-size: 0.85rem;
        font-weight: 600;
        color: #065f46;
        margin: 0.25rem;
    }
    
    /* Stats */
    .stat-number {
        font-size: 2rem;
        font-weight: 800;
        color: #059669;
    }
    
    .stat-label {
        font-size: 0.8rem;
        color: #9ca3af;
        text-transform: uppercase;
    }
</style>
""", unsafe_allow_html=True)

# ========== HERO SECTION ==========
st.markdown("""
<div class="hero-container">
    <div style="font-size: 4rem; margin-bottom: 0.5rem;">🌸</div>
    <h1 class="hero-title">Budidaya Krisan Spray Jepang</h1>
    <p class="hero-subtitle">
        SOP Lengkap dari Hulu hingga Hilir — Panduan profesional budidaya 
        Chrysanthemum untuk petani dan pengusaha bunga.
    </p>
    <div style="margin-top: 1.5rem; display: flex; justify-content: center; gap: 0.5rem; flex-wrap: wrap;">
        <span class="badge">🌺 3 Varietas Warna</span>
        <span class="badge">📊 Kalkulator Bisnis</span>
        <span class="badge">🌡️ Monitor Lingkungan</span>
        <span class="badge">📋 SOP Lengkap</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ========== VARIETY SHOWCASE ==========
st.markdown("### 🌺 Varietas Krisan")
st.markdown("*Tiga varietas unggulan yang bisa Anda budidayakan:*")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="variety-card variety-white">
        <div style="font-size: 3rem;">🤍</div>
        <h3 style="color: #374151; margin: 0.5rem 0;">Krisan Putih</h3>
        <p style="color: #6b7280; font-size: 0.85rem;">
            Elegan dan timeless. Cocok untuk dekorasi pernikahan, 
            pemakaman, dan buket formal.
        </p>
        <div style="margin-top: 1rem;">
            <span style="color: #059669; font-weight: 600;">💰 Rp 8.000-15.000/tangkai</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="variety-card variety-pink">
        <div style="font-size: 3rem;">💗</div>
        <h3 style="color: #be185d; margin: 0.5rem 0;">Krisan Pink</h3>
        <p style="color: #6b7280; font-size: 0.85rem;">
            Romantis dan feminin. Favorit untuk hadiah, 
            dekorasi acara, dan florist retail.
        </p>
        <div style="margin-top: 1rem;">
            <span style="color: #059669; font-weight: 600;">💰 Rp 10.000-18.000/tangkai</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="variety-card variety-yellow">
        <div style="font-size: 3rem;">💛</div>
        <h3 style="color: #ca8a04; margin: 0.5rem 0;">Krisan Kuning</h3>
        <p style="color: #6b7280; font-size: 0.85rem;">
            Cerah dan ceria. Populer untuk Imlek, 
            dekorasi rumah, dan rangkaian tropikal.
        </p>
        <div style="margin-top: 1rem;">
            <span style="color: #059669; font-weight: 600;">💰 Rp 8.000-14.000/tangkai</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ========== FEATURE CARDS ==========
st.markdown("### 📚 Modul Pembelajaran")

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
    <div class="glass-card">
        <div class="card-icon">🌸</div>
        <div class="card-title">Panduan Budidaya</div>
        <div class="card-desc">Teknik lengkap dari persiapan media, 
        stek, penanaman, hingga pemanenan bunga berkualitas.</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("📖 Buka Panduan", key="btn_guide", use_container_width=True):
        st.switch_page("pages/1_🌸_Panduan_Budidaya.py")

with c2:
    st.markdown("""
    <div class="glass-card">
        <div class="card-icon">🌡️</div>
        <div class="card-title">Monitor Lingkungan</div>
        <div class="card-desc">Pantau dan analisis parameter suhu, 
        kelembaban, dan pencahayaan untuk hasil optimal.</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("📊 Cek Parameter", key="btn_monitor", use_container_width=True):
        st.switch_page("pages/2_🌡️_Monitor_Lingkungan.py")

with c3:
    st.markdown("""
    <div class="glass-card">
        <div class="card-icon">📊</div>
        <div class="card-title">Kalkulator Produksi</div>
        <div class="card-desc">Hitung estimasi hasil panen, biaya produksi, 
        dan proyeksi keuntungan usaha Anda.</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🧮 Hitung Produksi", key="btn_calc", use_container_width=True):
        st.switch_page("pages/3_📊_Kalkulator_Produksi.py")

c4, c5, c6 = st.columns(3)

with c4:
    st.markdown("""
    <div class="glass-card">
        <div class="card-icon">🐛</div>
        <div class="card-title">Hama & Penyakit</div>
        <div class="card-desc">Identifikasi dan pengendalian hama penyakit 
        krisan dengan pendekatan IPM.</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🔍 Lihat Panduan", key="btn_pest", use_container_width=True):
        st.switch_page("pages/4_🐛_Hama_Penyakit.py")

with c5:
    st.markdown("""
    <div class="glass-card">
        <div class="card-icon">📦</div>
        <div class="card-title">Pasca Panen</div>
        <div class="card-desc">Teknik pemanenan, grading, packing, 
        dan perpanjangan vase life bunga potong.</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("📋 Baca Panduan", key="btn_harvest", use_container_width=True):
        st.switch_page("pages/5_📦_Pasca_Panen.py")

with c6:
    st.markdown("""
    <div class="glass-card">
        <div class="card-icon">💰</div>
        <div class="card-title">Analisis Usaha</div>
        <div class="card-desc">Perhitungan modal, BEP, ROI, dan 
        proyeksi bisnis budidaya krisan Anda.</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("📈 Analisis Bisnis", key="btn_business", use_container_width=True):
        st.switch_page("pages/6_💰_Analisis_Usaha.py")

st.markdown("---")

# ========== QUICK STATS ==========
st.markdown("### 📈 Fakta Budidaya Krisan")

stat1, stat2, stat3, stat4 = st.columns(4)

with stat1:
    st.markdown("""
    <div style="text-align: center; padding: 1rem;">
        <div class="stat-number">90-120</div>
        <div class="stat-label">Hari Tanam-Panen</div>
    </div>
    """, unsafe_allow_html=True)

with stat2:
    st.markdown("""
    <div style="text-align: center; padding: 1rem;">
        <div class="stat-number">18-24°C</div>
        <div class="stat-label">Suhu Optimal</div>
    </div>
    """, unsafe_allow_html=True)

with stat3:
    st.markdown("""
    <div style="text-align: center; padding: 1rem;">
        <div class="stat-number">60-70%</div>
        <div class="stat-label">Kelembaban Ideal</div>
    </div>
    """, unsafe_allow_html=True)

with stat4:
    st.markdown("""
    <div style="text-align: center; padding: 1rem;">
        <div class="stat-number">800+</div>
        <div class="stat-label">mdpl Lokasi Ideal</div>
    </div>
    """, unsafe_allow_html=True)

# ========== FOOTER ==========
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: #9ca3af; font-size: 0.8rem; padding: 1rem;">
    🌸 Budidaya Krisan Pro v1.0 | © 2025 AgriSensa<br>
    <small>Server Time: {datetime.now().strftime('%d %B %Y, %H:%M WIB')}</small>
</div>
""", unsafe_allow_html=True)

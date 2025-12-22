# 📦 Pasca Panen Krisan
# Panduan panen, grading input, dan perpanjangan vase life

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go

st.set_page_config(page_title="Pasca Panen", page_icon="📦", layout="wide")

# CSS
st.markdown("""
<style>
    .grade-card {
        background: linear-gradient(135deg, #ecfdf5 0%, #ffffff 100%);
        border: 1px solid #a7f3d0;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .grade-bs {
        background: linear-gradient(135deg, #fef3c7 0%, #ffffff 100%);
        border: 1px solid #fcd34d;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .progress-bar {
        background: #e5e7eb;
        border-radius: 10px;
        height: 20px;
        overflow: hidden;
    }
    .progress-fill {
        background: linear-gradient(90deg, #10b981 0%, #059669 100%);
        height: 100%;
        transition: width 0.3s ease;
    }
    .summary-box {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
        border: 1px solid #93c5fd;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("## 📦 Teknologi Pasca Panen Krisan Spray")
st.info("Panduan pemanenan, grading input aktual, handling, dan perpanjangan vase life.")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "✂️ Teknik Panen", 
    "📊 Input Grading", 
    "📋 Standar Grade",
    "💧 Vase Life", 
    "📦 Packing"
])

# TAB 1: Teknik Panen
with tab1:
    st.subheader("✂️ Teknik Pemanenan Krisan Spray")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### ⏰ Waktu Panen Optimal
        
        **Waktu Terbaik:**
        - Pagi hari: 06.00 - 09.00 WIB
        - Sore hari: 15.00 - 17.00 WIB
        - **HINDARI:** Tengah hari saat terik!
        
        **Kondisi Bunga:**
        - 2-3 kuntum sudah mekar penuh (untuk spray)
        - Kuntum lain masih kuncup berwarna
        - Hindari panen saat bunga basah
        """)
    
    with col2:
        st.markdown("""
        ### 🔧 Peralatan & Teknik
        
        **Peralatan:**
        - Pisau/gunting tajam & steril
        - Ember berisi air + preservative
        - Keranjang pengangkut
        
        **Cara Potong:**
        - Potong miring 45°
        - Sisakan 2 ruas daun di tanaman
        - Langsung masukkan ke air!
        """)
    
    st.warning("⚠️ **PENTING:** Jangan biarkan tangkai terkena udara >30 detik! Air embolism akan mengurangi vase life.")

# TAB 2: Input Grading Aktual
with tab2:
    st.subheader("📊 Input Hasil Grading Aktual")
    
    # Get potential harvest from session or input
    col_setup, col_summary = st.columns([2, 1])
    
    with col_setup:
        potential_harvest = st.number_input(
            "🌱 Potensi Tanaman Panen (batang)",
            min_value=1000, max_value=100000, value=17000, step=1000,
            help="Jumlah tanaman yang siap panen"
        )
    
    with col_summary:
        st.markdown(f"""
        <div class="summary-box">
            💡 <strong>Masukkan hasil grading dari panen.</strong><br>
            Potensi tanaman panen: <strong>{potential_harvest:,}</strong> batang
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Initialize session state for grades
    if 'grading_data' not in st.session_state:
        st.session_state.grading_data = {
            'g60': 0, 'g80': 0, 'g100': 0, 'g120': 0, 'g160': 0,
            'r80': 0, 'r100': 0, 'r160': 0, 'r200': 0
        }
    
    # GRADE NORMAL (Panjang 90 cm)
    st.markdown("### ✅ Grade Normal (Panjang 90 cm)")
    
    normal_grades = [
        {"name": "Grade 60", "key": "g60", "qty": 60, "price": 60000},
        {"name": "Grade 80", "key": "g80", "qty": 80, "price": 80000},
        {"name": "Grade 100", "key": "g100", "qty": 100, "price": 100000},
        {"name": "Grade 120", "key": "g120", "qty": 120, "price": 120000},
        {"name": "Grade 160", "key": "g160", "qty": 160, "price": 160000},
    ]
    
    cols_normal = st.columns(5)
    
    for i, grade in enumerate(normal_grades):
        with cols_normal[i]:
            st.markdown(f"""
            <div class="grade-card">
                <strong>{grade['name']}</strong><br>
                <small>{grade['qty']} btg/ikat</small>
            </div>
            """, unsafe_allow_html=True)
            
            st.session_state.grading_data[grade['key']] = st.number_input(
                "Jumlah Ikat",
                min_value=0, max_value=500, value=st.session_state.grading_data[grade['key']],
                key=f"input_{grade['key']}",
                label_visibility="visible"
            )
            
            st.caption(f"Rp {grade['price']:,}/ikat")
    
    st.markdown("---")
    
    # GRADE BS/RUSAK (Panjang 70-80 cm)
    st.markdown("### ⚠️ Grade Rusak/BS (Panjang 70-80 cm)")
    st.caption("Untuk bunga dengan batang lebih pendek dari standar")
    
    bs_grades = [
        {"name": "R-80", "key": "r80", "qty": 80, "length": 80, "price": 40000},
        {"name": "R-100", "key": "r100", "qty": 100, "length": 80, "price": 50000},
        {"name": "R-160", "key": "r160", "qty": 160, "length": 70, "price": 60000},
        {"name": "R-200", "key": "r200", "qty": 200, "length": 70, "price": 70000},
    ]
    
    cols_bs = st.columns(4)
    
    for i, grade in enumerate(bs_grades):
        with cols_bs[i]:
            st.markdown(f"""
            <div class="grade-bs">
                <strong>{grade['name']}</strong><br>
                <small>({grade['qty']} btg, {grade['length']}cm)</small>
            </div>
            """, unsafe_allow_html=True)
            
            st.session_state.grading_data[grade['key']] = st.number_input(
                "Jml Ikat",
                min_value=0, max_value=500, value=st.session_state.grading_data[grade['key']],
                key=f"input_{grade['key']}",
                label_visibility="visible"
            )
            
            st.caption(f"Rp {grade['price']:,}/ikat")
    
    st.markdown("---")
    
    # CALCULATE TOTALS
    total_normal_stems = sum(
        st.session_state.grading_data[g['key']] * g['qty'] 
        for g in normal_grades
    )
    
    total_bs_stems = sum(
        st.session_state.grading_data[g['key']] * g['qty'] 
        for g in bs_grades
    )
    
    total_graded = total_normal_stems + total_bs_stems
    progress_pct = (total_graded / potential_harvest * 100) if potential_harvest > 0 else 0
    remaining = potential_harvest - total_graded
    
    # Revenue calculation
    revenue_normal = sum(
        st.session_state.grading_data[g['key']] * g['price'] 
        for g in normal_grades
    )
    
    revenue_bs = sum(
        st.session_state.grading_data[g['key']] * g['price'] 
        for g in bs_grades
    )
    
    total_revenue = revenue_normal + revenue_bs
    
    # PROGRESS BAR
    st.markdown("### 📊 Progress Grading")
    
    progress_color = "#10b981" if progress_pct <= 100 else "#ef4444"
    st.markdown(f"""
    <div class="progress-bar">
        <div class="progress-fill" style="width: {min(progress_pct, 100)}%; background: {progress_color};"></div>
    </div>
    <div style="text-align: center; margin-top: 0.5rem;">
        <strong>{total_graded:,}</strong> / {potential_harvest:,} batang 
        (<strong>{progress_pct:.1f}%</strong>)
        {f" — Sisa: {remaining:,} batang" if remaining > 0 else ""}
    </div>
    """, unsafe_allow_html=True)
    
    if progress_pct > 100:
        st.error(f"⚠️ Total grading ({total_graded:,}) melebihi potensi panen ({potential_harvest:,})!")
    
    st.markdown("---")
    
    # SUMMARY TABLE
    st.markdown("### 💰 Ringkasan Hasil Grading")
    
    col_sum1, col_sum2, col_sum3 = st.columns(3)
    
    with col_sum1:
        st.metric("🌸 Total Batang Normal", f"{total_normal_stems:,}")
        st.metric("💵 Pendapatan Normal", f"Rp {revenue_normal:,.0f}")
    
    with col_sum2:
        st.metric("⚠️ Total Batang BS", f"{total_bs_stems:,}")
        st.metric("💵 Pendapatan BS", f"Rp {revenue_bs:,.0f}")
    
    with col_sum3:
        st.metric("📦 **TOTAL BATANG**", f"{total_graded:,}")
        st.metric("💰 **TOTAL PENDAPATAN**", f"Rp {total_revenue:,.0f}")
    
    # Detailed breakdown table
    with st.expander("📋 Lihat Rincian per Grade", expanded=False):
        breakdown_data = []
        
        for g in normal_grades:
            ikat = st.session_state.grading_data[g['key']]
            if ikat > 0:
                breakdown_data.append({
                    "Grade": g['name'],
                    "Tipe": "Normal",
                    "Ikat": ikat,
                    "Batang": ikat * g['qty'],
                    "Harga/Ikat": f"Rp {g['price']:,}",
                    "Subtotal": f"Rp {ikat * g['price']:,}"
                })
        
        for g in bs_grades:
            ikat = st.session_state.grading_data[g['key']]
            if ikat > 0:
                breakdown_data.append({
                    "Grade": g['name'],
                    "Tipe": "BS/Rusak",
                    "Ikat": ikat,
                    "Batang": ikat * g['qty'],
                    "Harga/Ikat": f"Rp {g['price']:,}",
                    "Subtotal": f"Rp {ikat * g['price']:,}"
                })
        
        if breakdown_data:
            st.dataframe(pd.DataFrame(breakdown_data), use_container_width=True, hide_index=True)
        else:
            st.info("Belum ada data grading yang diinput.")
    
    # Pie chart
    if total_graded > 0:
        st.markdown("### 📊 Distribusi Grade")
        
        labels = []
        values = []
        
        for g in normal_grades:
            stems = st.session_state.grading_data[g['key']] * g['qty']
            if stems > 0:
                labels.append(g['name'])
                values.append(stems)
        
        for g in bs_grades:
            stems = st.session_state.grading_data[g['key']] * g['qty']
            if stems > 0:
                labels.append(g['name'])
                values.append(stems)
        
        fig = go.Figure(data=[go.Pie(
            labels=labels, 
            values=values, 
            hole=0.4,
            marker_colors=['#10b981', '#059669', '#047857', '#065f46', '#064e3b', 
                          '#fbbf24', '#f59e0b', '#d97706', '#b45309']
        )])
        
        fig.update_layout(title="Distribusi Batang per Grade", height=400)
        st.plotly_chart(fig, use_container_width=True)

# TAB 3: Standar Grading
with tab3:
    st.subheader("📋 Standar Grading Krisan Spray")
    
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
    
    st.markdown("### 💰 Harga per Grade")
    
    cols = st.columns(4)
    with cols[0]:
        st.metric("Super", "Rp 15.000-20.000", "/tangkai")
    with cols[1]:
        st.metric("Grade A", "Rp 10.000-15.000", "/tangkai")
    with cols[2]:
        st.metric("Grade B", "Rp 7.000-10.000", "/tangkai")
    with cols[3]:
        st.metric("Grade C", "Rp 4.000-7.000", "/tangkai")

# TAB 4: Vase Life
with tab4:
    st.subheader("💧 Teknik Perpanjangan Vase Life")
    
    st.success("**Target Vase Life Krisan Spray:** 10-16 hari")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🧪 Larutan Preservative
        
        **Formula Komersial:**
        - Chrysal, Floralife
        - Ikuti dosis pada kemasan
        - Ganti setiap 2-3 hari
        
        **Formula DIY (per 1 Liter):**
        - Gula: 20g
        - Cuka: 2ml
        - Bleach: 3-4 tetes
        """)
    
    with col2:
        st.markdown("""
        ### 🌡️ Cold Chain
        
        | Tahap | Suhu | Durasi |
        |-------|------|--------|
        | Hydration | 2-4°C | 2-4 jam |
        | Storage | 2-4°C | Maks 7 hari |
        | Display | 8-12°C | 3-5 hari |
        """)
    
    st.error("🚨 JANGAN simpan bersama buah yang menghasilkan etilen!")

# TAB 5: Packing
with tab5:
    st.subheader("📦 Packing & Distribusi")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 📦 Jenis Kemasan
        
        **1. Bunch Wrapping** (10 tangkai/bunch)
        - Plastik OPP transparan
        - Cocok untuk florist
        
        **2. Box Kardus** (20-50 bunch)
        - Distribusi jarak jauh
        """)
    
    with col2:
        st.markdown("""
        ### 🚚 Distribusi
        
        | Jarak | Suhu | Durasi |
        |-------|------|--------|
        | <50 km | Ambient | 2-3 jam |
        | 50-200 km | 8-15°C | 4-6 jam |
        | >200 km | 2-4°C | 24-48 jam |
        """)

# Footer
st.markdown("---")
st.caption("🌸 Budidaya Krisan Pro - Teknologi Pasca Panen & Grading")

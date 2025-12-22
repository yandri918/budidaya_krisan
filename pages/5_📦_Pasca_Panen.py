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
    
    # ========== SYNC DATA DARI KALKULATOR PRODUKSI ==========
    # Check if synced data exists
    has_synced_data = 'krisan_data' in st.session_state and st.session_state.krisan_data.get('beds_putih', 0) > 0
    
    if has_synced_data:
        data = st.session_state.krisan_data
        st.markdown(f"""
        <div class="sync-badge">
            📊 <strong>Data Tersinkronisasi dari Kalkulator Produksi:</strong><br>
            🤍 Putih: <strong>{data.get('beds_putih', 0)}</strong> bedengan ({data.get('plants_putih', 0):,} tanaman) |
            💗 Pink: <strong>{data.get('beds_pink', 0)}</strong> bedengan ({data.get('plants_pink', 0):,} tanaman) |
            💛 Kuning: <strong>{data.get('beds_kuning', 0)}</strong> bedengan ({data.get('plants_kuning', 0):,} tanaman)
        </div>
        """, unsafe_allow_html=True)
        
        use_synced = st.checkbox("✅ Gunakan data dari Kalkulator Produksi", value=True)
        
        if use_synced:
            beds_putih = data.get('beds_putih', 4)
            beds_pink = data.get('beds_pink', 4)
            beds_kuning = data.get('beds_kuning', 4)
            plants_per_bed = data.get('plants_per_bed', 1400)
        else:
            st.markdown("### 🌸 Input Manual Proporsi Bedengan")
            col_bed1, col_bed2, col_bed3 = st.columns(3)
            with col_bed1:
                beds_putih = st.number_input("🤍 Bedengan Putih", 0, 50, 4, key="manual_beds_putih")
            with col_bed2:
                beds_pink = st.number_input("💗 Bedengan Pink", 0, 50, 4, key="manual_beds_pink")
            with col_bed3:
                beds_kuning = st.number_input("💛 Bedengan Kuning", 0, 50, 4, key="manual_beds_kuning")
            plants_per_bed = st.number_input("🌱 Tanaman per Bedengan", 500, 3000, 1400, step=100)
    else:
        st.info("💡 Untuk sinkronisasi otomatis, isi data di **Kalkulator Produksi** → Tab Populasi Tanaman terlebih dahulu.")
        
        st.markdown("### 🌸 Proporsi Bedengan per Varietas")
        col_bed1, col_bed2, col_bed3 = st.columns(3)
        with col_bed1:
            beds_putih = st.number_input("🤍 Bedengan Putih", 0, 50, 4, key="beds_putih")
        with col_bed2:
            beds_pink = st.number_input("💗 Bedengan Pink", 0, 50, 4, key="beds_pink")
        with col_bed3:
            beds_kuning = st.number_input("💛 Bedengan Kuning", 0, 50, 4, key="beds_kuning")
        plants_per_bed = st.number_input("🌱 Tanaman per Bedengan", 500, 3000, 1400, step=100,
                                         help="Berdasarkan panjang × baris × jarak tanam")
    
    # Calculate plants per variety
    total_beds = beds_putih + beds_pink + beds_kuning
    plants_putih = beds_putih * plants_per_bed
    plants_pink = beds_pink * plants_per_bed
    plants_kuning = beds_kuning * plants_per_bed
    total_plants = plants_putih + plants_pink + plants_kuning
    
    # Display proportion
    st.markdown("### 📊 Proporsi Tanaman per Varietas")
    
    prop_cols = st.columns(4)
    
    with prop_cols[0]:
        pct_putih = (plants_putih / total_plants * 100) if total_plants > 0 else 0
        st.metric("🤍 Krisan Putih", f"{plants_putih:,}", f"{pct_putih:.1f}%")
    with prop_cols[1]:
        pct_pink = (plants_pink / total_plants * 100) if total_plants > 0 else 0
        st.metric("💗 Krisan Pink", f"{plants_pink:,}", f"{pct_pink:.1f}%")
    with prop_cols[2]:
        pct_kuning = (plants_kuning / total_plants * 100) if total_plants > 0 else 0
        st.metric("💛 Krisan Kuning", f"{plants_kuning:,}", f"{pct_kuning:.1f}%")
    with prop_cols[3]:
        st.metric("🌸 **TOTAL**", f"{total_plants:,}")
    
    st.markdown("---")
    
    # ========== PILIH VARIETAS UNTUK GRADING ==========
    st.markdown("### 📝 Input Grading per Varietas")
    
    selected_variety = st.radio(
        "Pilih Varietas untuk Input Grading:",
        ["🤍 Krisan Putih", "💗 Krisan Pink", "💛 Krisan Kuning"],
        horizontal=True
    )
    
    # Map variety to key
    variety_key = {
        "🤍 Krisan Putih": "putih",
        "💗 Krisan Pink": "pink", 
        "💛 Krisan Kuning": "kuning"
    }[selected_variety]
    
    variety_plants = {
        "putih": plants_putih,
        "pink": plants_pink,
        "kuning": plants_kuning
    }
    
    potential_harvest = variety_plants[variety_key]
    
    st.info(f"📊 Potensi panen {selected_variety}: **{potential_harvest:,}** batang ({beds_putih if variety_key == 'putih' else beds_pink if variety_key == 'pink' else beds_kuning} bedengan)")
    
    st.markdown("---")
    
    # Initialize session state for grades per variety
    if 'grading_data_variety' not in st.session_state:
        st.session_state.grading_data_variety = {
            'putih': {'g60': 0, 'g80': 0, 'g100': 0, 'g120': 0, 'g160': 0, 'r80': 0, 'r100': 0, 'r160': 0, 'r200': 0},
            'pink': {'g60': 0, 'g80': 0, 'g100': 0, 'g120': 0, 'g160': 0, 'r80': 0, 'r100': 0, 'r160': 0, 'r200': 0},
            'kuning': {'g60': 0, 'g80': 0, 'g100': 0, 'g120': 0, 'g160': 0, 'r80': 0, 'r100': 0, 'r160': 0, 'r200': 0},
        }
    
    # Use current variety data
    grading_data = st.session_state.grading_data_variety[variety_key]
    
    # GRADE NORMAL (Panjang 90 cm)
    st.markdown("### ✅ Grade Normal (Panjang 90 cm)")
    
    # Initialize price session state
    if 'grade_prices' not in st.session_state:
        st.session_state.grade_prices = {
            'g60': 1000, 'g80': 1000, 'g100': 1000, 'g120': 1000, 'g160': 1000,
            'r80': 500, 'r100': 500, 'r160': 400, 'r200': 350
        }
    
    normal_grades = [
        {"name": "Grade 60", "key": "g60", "qty": 60},
        {"name": "Grade 80", "key": "g80", "qty": 80},
        {"name": "Grade 100", "key": "g100", "qty": 100},
        {"name": "Grade 120", "key": "g120", "qty": 120},
        {"name": "Grade 160", "key": "g160", "qty": 160},
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
            
            grading_data[grade['key']] = st.number_input(
                "Jml Ikat",
                min_value=0, max_value=500, value=grading_data[grade['key']],
                key=f"input_{variety_key}_{grade['key']}",
                label_visibility="visible"
            )
            
            # Harga per batang (editable)
            st.session_state.grade_prices[grade['key']] = st.number_input(
                "Rp/btg",
                min_value=100, max_value=10000, 
                value=st.session_state.grade_prices[grade['key']],
                step=50,
                key=f"price_{variety_key}_{grade['key']}",
                label_visibility="visible"
            )
            
            # Hitung total
            total_stems_grade = grading_data[grade['key']] * grade['qty']
            price_per_stem = st.session_state.grade_prices[grade['key']]
            total_price_grade = total_stems_grade * price_per_stem
            
            if total_stems_grade > 0:
                st.markdown(f"<small>= {total_stems_grade:,} btg<br>**Rp {total_price_grade:,.0f}**</small>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # GRADE BS/RUSAK (Panjang 70-80 cm)
    st.markdown("### ⚠️ Grade Rusak/BS (Panjang 70-80 cm)")
    st.caption("Untuk bunga dengan batang lebih pendek dari standar")
    
    bs_grades = [
        {"name": "R-80", "key": "r80", "qty": 80, "length": 80},
        {"name": "R-100", "key": "r100", "qty": 100, "length": 80},
        {"name": "R-160", "key": "r160", "qty": 160, "length": 70},
        {"name": "R-200", "key": "r200", "qty": 200, "length": 70},
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
            
            grading_data[grade['key']] = st.number_input(
                "Jml Ikat",
                min_value=0, max_value=500, value=grading_data[grade['key']],
                key=f"input_{variety_key}_{grade['key']}",
                label_visibility="visible"
            )
            
            # Harga per batang (editable)
            st.session_state.grade_prices[grade['key']] = st.number_input(
                "Rp/btg",
                min_value=100, max_value=10000, 
                value=st.session_state.grade_prices[grade['key']],
                step=50,
                key=f"price_{variety_key}_{grade['key']}",
                label_visibility="visible"
            )
            
            # Hitung total
            total_stems_grade = grading_data[grade['key']] * grade['qty']
            price_per_stem = st.session_state.grade_prices[grade['key']]
            total_price_grade = total_stems_grade * price_per_stem
            
            if total_stems_grade > 0:
                st.markdown(f"<small>= {total_stems_grade:,} btg<br>**Rp {total_price_grade:,.0f}**</small>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # CALCULATE TOTALS (for current variety) - ikat × qty
    total_normal_stems = sum(
        grading_data[g['key']] * g['qty']
        for g in normal_grades
    )
    
    total_bs_stems = sum(
        grading_data[g['key']] * g['qty']
        for g in bs_grades
    )
    
    total_graded = total_normal_stems + total_bs_stems
    progress_pct = (total_graded / potential_harvest * 100) if potential_harvest > 0 else 0
    remaining = potential_harvest - total_graded
    
    # Revenue calculation - (ikat × qty) × price per stem from session state
    revenue_normal = sum(
        grading_data[g['key']] * g['qty'] * st.session_state.grade_prices[g['key']] 
        for g in normal_grades
    )
    
    revenue_bs = sum(
        grading_data[g['key']] * g['qty'] * st.session_state.grade_prices[g['key']] 
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
    
    # ========== ANALISIS HARGA PER BATANG ==========
    st.markdown("---")
    st.markdown("### 💵 Analisis Harga Jual vs Biaya Produksi")
    
    col_cost, col_expected = st.columns(2)
    
    with col_cost:
        st.markdown("**📊 Input Parameter Biaya**")
        
        production_cost_total = st.number_input(
            "💰 Total Biaya Produksi (Rp/siklus)",
            min_value=1000000, max_value=500000000, value=30000000, step=1000000,
            help="Total biaya operasional per siklus (dari tab RAB)"
        )
        
        expected_price_per_stem = st.number_input(
            "🎯 Harga Ekspektasi Awal (Rp/batang)",
            min_value=500, max_value=5000, value=1200, step=100,
            help="Harga jual per batang yang diharapkan sebelum grading"
        )
    
    with col_expected:
        st.markdown("**🎯 Ekspektasi Awal**")
        
        expected_revenue = potential_harvest * expected_price_per_stem
        expected_profit = expected_revenue - production_cost_total
        expected_margin = (expected_profit / expected_revenue * 100) if expected_revenue > 0 else 0
        
        st.metric("Pendapatan Ekspektasi", f"Rp {expected_revenue:,.0f}")
        st.metric("Profit Ekspektasi", f"Rp {expected_profit:,.0f}")
        st.metric("Margin Ekspektasi", f"{expected_margin:.1f}%")
    
    # PERBANDINGAN AKTUAL VS EKSPEKTASI
    st.markdown("---")
    st.markdown("### 📈 Perbandingan Aktual vs Ekspektasi")
    
    # Calculate actual per stem values
    if total_graded > 0:
        actual_price_per_stem = total_revenue / total_graded
        cost_per_stem = production_cost_total / total_graded
        profit_per_stem = actual_price_per_stem - cost_per_stem
        margin_per_stem = (profit_per_stem / actual_price_per_stem * 100) if actual_price_per_stem > 0 else 0
        
        actual_profit = total_revenue - production_cost_total
        actual_margin = (actual_profit / total_revenue * 100) if total_revenue > 0 else 0
        
        # Variance calculation
        price_variance = actual_price_per_stem - expected_price_per_stem
        price_variance_pct = (price_variance / expected_price_per_stem * 100) if expected_price_per_stem > 0 else 0
        revenue_variance = total_revenue - expected_revenue
        profit_variance = actual_profit - expected_profit
        
        # Display comparison table
        comparison_data = pd.DataFrame({
            "Parameter": [
                "Jumlah Batang",
                "Harga per Batang",
                "Total Pendapatan",
                "Biaya Produksi",
                "Total Profit",
                "Margin (%)"
            ],
            "Ekspektasi": [
                f"{potential_harvest:,}",
                f"Rp {expected_price_per_stem:,.0f}",
                f"Rp {expected_revenue:,.0f}",
                f"Rp {production_cost_total:,.0f}",
                f"Rp {expected_profit:,.0f}",
                f"{expected_margin:.1f}%"
            ],
            "Aktual": [
                f"{total_graded:,}",
                f"Rp {actual_price_per_stem:,.0f}",
                f"Rp {total_revenue:,.0f}",
                f"Rp {production_cost_total:,.0f}",
                f"Rp {actual_profit:,.0f}",
                f"{actual_margin:.1f}%"
            ],
            "Selisih": [
                f"{total_graded - potential_harvest:+,}",
                f"Rp {price_variance:+,.0f} ({price_variance_pct:+.1f}%)",
                f"Rp {revenue_variance:+,.0f}",
                "-",
                f"Rp {profit_variance:+,.0f}",
                f"{actual_margin - expected_margin:+.1f}%"
            ]
        })
        
        st.dataframe(comparison_data, use_container_width=True, hide_index=True)
        
        # Visual indicators
        st.markdown("---")
        st.markdown("### 📊 Analisis Per Batang")
        
        m1, m2, m3, m4 = st.columns(4)
        
        with m1:
            st.metric(
                "Harga Jual/Batang", 
                f"Rp {actual_price_per_stem:,.0f}",
                delta=f"Rp {price_variance:+,.0f} vs ekspektasi",
                delta_color="normal" if price_variance >= 0 else "inverse"
            )
        
        with m2:
            st.metric("Biaya/Batang", f"Rp {cost_per_stem:,.0f}")
        
        with m3:
            st.metric(
                "Profit/Batang", 
                f"Rp {profit_per_stem:,.0f}",
                delta_color="normal" if profit_per_stem > 0 else "inverse"
            )
        
        with m4:
            st.metric(
                "Margin/Batang", 
                f"{margin_per_stem:.1f}%",
                delta_color="normal" if margin_per_stem > 20 else "inverse"
            )
        
        # Summary verdict
        st.markdown("---")
        
        if price_variance >= 0 and profit_variance >= 0:
            st.success(f"""
            ✅ **HASIL LEBIH BAIK DARI EKSPEKTASI!**
            
            - Harga aktual per batang **lebih tinggi** Rp {price_variance:,.0f} dari ekspektasi
            - Profit aktual **lebih besar** Rp {profit_variance:,.0f} dari target
            """)
        elif price_variance < 0 and profit_variance < 0:
            st.error(f"""
            ⚠️ **HASIL DI BAWAH EKSPEKTASI**
            
            - Harga aktual per batang **lebih rendah** Rp {abs(price_variance):,.0f} dari ekspektasi
            - Profit aktual **lebih kecil** Rp {abs(profit_variance):,.0f} dari target
            
            **Penyebab potensial:** Proporsi grade BS tinggi, harga pasar turun
            """)
        else:
            st.warning(f"""
            ⚡ **HASIL BERVARIASI**
            
            - Harga per batang: {'lebih tinggi' if price_variance >= 0 else 'lebih rendah'} dari ekspektasi
            - Total profit: {'tercapai' if profit_variance >= 0 else 'tidak tercapai'}
            """)
        
        # Grade price analysis
        st.markdown("---")
        st.markdown("### 📋 Harga per Batang tiap Grade")
        
        grade_price_data = []
        
        for g in normal_grades:
            ikat = st.session_state.grading_data[g['key']]
            if ikat > 0:
                price_per_stem = g['price'] / g['qty']
                grade_price_data.append({
                    "Grade": g['name'],
                    "Batang/Ikat": g['qty'],
                    "Harga/Ikat": f"Rp {g['price']:,}",
                    "Harga/Batang": f"Rp {price_per_stem:,.0f}",
                    "vs Ekspektasi": f"Rp {price_per_stem - expected_price_per_stem:+,.0f}",
                    "Status": "✅" if price_per_stem >= expected_price_per_stem else "⚠️"
                })
        
        for g in bs_grades:
            ikat = st.session_state.grading_data[g['key']]
            if ikat > 0:
                price_per_stem = g['price'] / g['qty']
                grade_price_data.append({
                    "Grade": g['name'],
                    "Batang/Ikat": g['qty'],
                    "Harga/Ikat": f"Rp {g['price']:,}",
                    "Harga/Batang": f"Rp {price_per_stem:,.0f}",
                    "vs Ekspektasi": f"Rp {price_per_stem - expected_price_per_stem:+,.0f}",
                    "Status": "✅" if price_per_stem >= expected_price_per_stem else "⚠️"
                })
        
        if grade_price_data:
            st.dataframe(pd.DataFrame(grade_price_data), use_container_width=True, hide_index=True)
    else:
        st.info("💡 Masukkan data grading di atas untuk melihat analisis perbandingan.")

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

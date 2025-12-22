# 📊 Kalkulator Produksi Krisan
# Estimasi hasil berdasarkan bedengan dan analisis finansial

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(page_title="Kalkulator Produksi", page_icon="📊", layout="wide")

st.markdown("""
<style>
    .calc-card {
        background: linear-gradient(135deg, #ecfdf5 0%, #ffffff 100%);
        border: 1px solid #a7f3d0;
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    .calc-title {
        color: #065f46;
        font-weight: 700;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("## 📊 Kalkulator Produksi Krisan Spray")
st.info("Hitung jumlah tanaman berdasarkan konfigurasi bedengan, estimasi hasil panen, dan proyeksi keuntungan.")

# ========== TABS ==========
tab1, tab2, tab3 = st.tabs(["🌱 Perhitungan Tanaman", "💰 Analisis Finansial", "📈 Sensitivitas"])

with tab1:
    st.subheader("🌱 Konfigurasi Bedengan & Perhitungan Populasi")
    
    col_bed, col_result = st.columns([1.2, 1])
    
    with col_bed:
        st.markdown('<div class="calc-card"><div class="calc-title">📐 Konfigurasi Bedengan</div></div>', unsafe_allow_html=True)
        
        # Bed configuration
        bed_length = st.number_input(
            "📏 Panjang Bedengan (meter)", 
            min_value=5, max_value=100, value=25, step=1,
            help="Panjang satu bedengan dalam meter"
        )
        
        bed_width = st.number_input(
            "📐 Lebar Bedengan (cm)", 
            min_value=80, max_value=150, value=100, step=10,
            help="Lebar standar bedengan krisan: 100-120 cm"
        )
        
        num_beds = st.number_input(
            "🔢 Jumlah Bedengan", 
            min_value=1, max_value=100, value=10, step=1,
            help="Total bedengan dalam greenhouse"
        )
        
        st.markdown("---")
        st.markdown('<div class="calc-card"><div class="calc-title">🌿 Konfigurasi Tanam</div></div>', unsafe_allow_html=True)
        
        rows_per_bed = st.selectbox(
            "📊 Jumlah Baris per Bedengan",
            options=[6, 7, 8, 9, 10],
            index=2,  # default 8 baris
            help="Standar: 8 baris untuk lebar bedengan 100cm (jarak antar baris ~12.5cm)"
        )
        
        plant_spacing = st.selectbox(
            "↔️ Jarak Tanam dalam Baris (cm)",
            options=[10, 12.5, 15],
            index=1,  # default 12.5 cm
            format_func=lambda x: f"{x} cm",
            help="Jarak antar tanaman dalam satu baris"
        )
        
        # Varietas
        variety = st.selectbox(
            "🌸 Varietas",
            ["Krisan Spray Putih", "Krisan Spray Pink", "Krisan Spray Kuning", "Campuran"]
        )
        
        survival_rate = st.slider(
            "📊 Survival Rate (%)", 
            min_value=70, max_value=98, value=85,
            help="Persentase tanaman yang berhasil hingga panen"
        )
        
        stems_per_plant = st.slider(
            "🌸 Tangkai per Tanaman",
            min_value=2.0, max_value=5.0, value=3.5, step=0.5,
            help="Jumlah tangkai bunga per tanaman (tergantung pinching)"
        )
    
    with col_result:
        st.markdown('<div class="calc-card"><div class="calc-title">📊 Hasil Perhitungan</div></div>', unsafe_allow_html=True)
        
        # CALCULATIONS
        # Tanaman per baris = panjang bedengan / jarak tanam
        plants_per_row = int((bed_length * 100) / plant_spacing)
        
        # Tanaman per bedengan = tanaman per baris x jumlah baris
        plants_per_bed = plants_per_row * rows_per_bed
        
        # Total tanaman = tanaman per bedengan x jumlah bedengan
        total_plants = plants_per_bed * num_beds
        
        # Luas efektif bedengan (m²)
        bed_area_m2 = (bed_length * (bed_width / 100))  # per bedengan
        total_bed_area = bed_area_m2 * num_beds
        
        # Densitas aktual
        actual_density = total_plants / total_bed_area if total_bed_area > 0 else 0
        
        # Tanaman yang hidup (survival)
        surviving_plants = int(total_plants * (survival_rate / 100))
        
        # Total tangkai
        total_stems = int(surviving_plants * stems_per_plant)
        
        # Display metrics
        st.metric("🌱 Tanaman per Baris", f"{plants_per_row:,}")
        st.metric("📦 Tanaman per Bedengan", f"{plants_per_bed:,}")
        st.metric("🌿 **TOTAL TANAMAN**", f"{total_plants:,}")
        
        st.markdown("---")
        
        st.metric("✅ Tanaman Hidup (Panen)", f"{surviving_plants:,}", 
                  delta=f"Survival {survival_rate}%")
        st.metric("🌸 **TOTAL TANGKAI BUNGA**", f"{total_stems:,}",
                  delta=f"{stems_per_plant} tangkai/tanaman")
        
        st.markdown("---")
        
        st.metric("📐 Luas Bedengan Total", f"{total_bed_area:.1f} m²")
        st.metric("📊 Densitas Aktual", f"{actual_density:.1f} tanaman/m²")
        
        # Save to session state for other tabs
        st.session_state['total_plants'] = total_plants
        st.session_state['surviving_plants'] = surviving_plants
        st.session_state['total_stems'] = total_stems
        st.session_state['total_bed_area'] = total_bed_area
        st.session_state['num_beds'] = num_beds
    
    # Visual summary
    st.markdown("---")
    st.subheader("📋 Ringkasan Konfigurasi")
    
    summary_cols = st.columns(5)
    
    with summary_cols[0]:
        st.markdown(f"""
        **Bedengan:**
        - Panjang: {bed_length}m
        - Lebar: {bed_width}cm
        - Jumlah: {num_beds} unit
        """)
    
    with summary_cols[1]:
        st.markdown(f"""
        **Tanam:**
        - Baris/bedengan: {rows_per_bed}
        - Jarak tanam: {plant_spacing}cm
        """)
    
    with summary_cols[2]:
        st.markdown(f"""
        **Populasi:**
        - Total: {total_plants:,}
        - Densitas: {actual_density:.1f}/m²
        """)
    
    with summary_cols[3]:
        st.markdown(f"""
        **Panen:**
        - Survival: {survival_rate}%
        - Hidup: {surviving_plants:,}
        """)
    
    with summary_cols[4]:
        st.markdown(f"""
        **Produksi:**
        - Tangkai/tanaman: {stems_per_plant}
        - **Total: {total_stems:,}**
        """)

with tab2:
    st.subheader("💰 Analisis Finansial")
    
    # Get data from session state or use defaults
    total_plants = st.session_state.get('total_plants', 10000)
    total_stems = st.session_state.get('total_stems', 25000)
    total_bed_area = st.session_state.get('total_bed_area', 250)
    
    col_cost, col_profit = st.columns([1, 1.2])
    
    with col_cost:
        st.markdown("### 🧮 Input Biaya & Harga")
        
        selling_price = st.number_input(
            "💵 Harga Jual (Rp/tangkai)", 
            min_value=5000, max_value=30000, value=12000, step=500
        )
        
        cycles_per_year = st.selectbox(
            "🔄 Siklus per Tahun",
            options=[2, 3, 4],
            index=1,
            help="1 siklus = 105-120 hari"
        )
        
        with st.expander("📋 Detail Biaya Produksi", expanded=True):
            cost_cutting = st.number_input("Bibit/Stek (Rp/batang)", 200, 1000, 400, step=50)
            cost_fertilizer = st.number_input("Pupuk (Rp/m² bedengan)", 1000, 5000, 2500, step=100)
            cost_pesticide = st.number_input("Pestisida (Rp/m² bedengan)", 500, 3000, 1500, step=100)
            cost_labor_daily = st.number_input("Tenaga Kerja (Rp/hari)", 50000, 150000, 80000, step=5000)
            labor_days = st.number_input("Hari Kerja per Siklus", 30, 120, 90, step=5)
            cost_electricity = st.number_input("Listrik/Lampu (Rp/bulan)", 200000, 2000000, 500000, step=50000)
            cost_other = st.number_input("Biaya Lain-lain (Rp/siklus)", 0, 5000000, 500000, step=100000)
    
    with col_profit:
        st.markdown("### 📊 Hasil Analisis")
        
        # Calculate costs
        cost_cuttings_total = total_plants * cost_cutting
        cost_fert_total = total_bed_area * cost_fertilizer
        cost_pest_total = total_bed_area * cost_pesticide
        cost_labor_total = cost_labor_daily * labor_days
        cost_elec_total = cost_electricity * 4  # 4 bulan per siklus
        
        total_cost_per_cycle = (cost_cuttings_total + cost_fert_total + cost_pest_total + 
                                cost_labor_total + cost_elec_total + cost_other)
        
        # Revenue
        revenue_per_cycle = total_stems * selling_price
        profit_per_cycle = revenue_per_cycle - total_cost_per_cycle
        margin = (profit_per_cycle / revenue_per_cycle * 100) if revenue_per_cycle > 0 else 0
        
        # Annual
        revenue_per_year = revenue_per_cycle * cycles_per_year
        cost_per_year = total_cost_per_cycle * cycles_per_year
        profit_per_year = profit_per_cycle * cycles_per_year
        
        # Display
        st.markdown("**Per Siklus (±4 bulan)**")
        m1, m2 = st.columns(2)
        with m1:
            st.metric("Pendapatan", f"Rp {revenue_per_cycle:,.0f}")
            st.metric("Total Biaya", f"Rp {total_cost_per_cycle:,.0f}")
        with m2:
            st.metric("Keuntungan", f"Rp {profit_per_cycle:,.0f}",
                      delta=f"Margin {margin:.1f}%",
                      delta_color="normal" if profit_per_cycle > 0 else "inverse")
        
        st.markdown("---")
        st.markdown("**Per Tahun**")
        m3, m4 = st.columns(2)
        with m3:
            st.metric("Pendapatan", f"Rp {revenue_per_year:,.0f}")
            st.metric("Total Biaya", f"Rp {cost_per_year:,.0f}")
        with m4:
            st.metric("**PROFIT TAHUNAN**", f"Rp {profit_per_year:,.0f}",
                      delta_color="normal" if profit_per_year > 0 else "inverse")
        
        # BEP
        st.markdown("---")
        st.markdown("**Break Even Point**")
        bep_units = total_cost_per_cycle / selling_price if selling_price > 0 else 0
        bep_pct = (bep_units / total_stems * 100) if total_stems > 0 else 0
        
        if total_stems > bep_units:
            st.success(f"✅ BEP: {bep_units:,.0f} tangkai ({bep_pct:.1f}%) — Surplus {total_stems - bep_units:,.0f} tangkai")
        else:
            st.error(f"❌ BEP tidak tercapai. Kurang {bep_units - total_stems:,.0f} tangkai")
    
    # Cost breakdown chart
    st.markdown("---")
    st.subheader("📊 Breakdown Biaya Produksi")
    
    cost_data = {
        "Kategori": ["Bibit/Stek", "Pupuk", "Pestisida", "Tenaga Kerja", "Listrik", "Lainnya"],
        "Biaya (Rp)": [cost_cuttings_total, cost_fert_total, cost_pest_total, 
                      cost_labor_total, cost_elec_total, cost_other]
    }
    
    df_cost = pd.DataFrame(cost_data)
    
    fig = go.Figure(data=[
        go.Pie(
            labels=df_cost["Kategori"],
            values=df_cost["Biaya (Rp)"],
            hole=0.4,
            marker_colors=['#10b981', '#059669', '#047857', '#065f46', '#064e3b', '#9ca3af']
        )
    ])
    
    fig.update_layout(title="Distribusi Biaya Produksi per Siklus", height=400)
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("📈 Analisis Sensitivitas")
    
    total_stems = st.session_state.get('total_stems', 25000)
    
    st.markdown("### 🎯 Sensitivitas Harga Jual")
    
    base_price = st.slider("Harga Dasar (Rp/tangkai)", 8000, 20000, 12000, 1000)
    base_cost = st.number_input("Estimasi Biaya per Siklus (Rp)", 10000000, 100000000, 30000000, 1000000)
    
    price_scenarios = [base_price * 0.7, base_price * 0.85, base_price, 
                       base_price * 1.15, base_price * 1.3]
    profits = [(total_stems * p) - base_cost for p in price_scenarios]
    
    fig_sens = go.Figure()
    
    fig_sens.add_trace(go.Bar(
        x=[f"Rp {int(p):,}" for p in price_scenarios],
        y=profits,
        marker_color=['#ef4444' if p < 0 else '#10b981' for p in profits],
        text=[f"Rp {p/1000000:.1f} jt" for p in profits],
        textposition='outside'
    ))
    
    fig_sens.update_layout(
        title="Keuntungan vs Harga Jual",
        xaxis_title="Harga Jual per Tangkai",
        yaxis_title="Keuntungan (Rp)",
        height=400
    )
    
    st.plotly_chart(fig_sens, use_container_width=True)
    
    # Sensitivity table
    st.markdown("### 📋 Tabel Sensitivitas")
    
    sens_data = []
    for p in price_scenarios:
        revenue = total_stems * p
        profit = revenue - base_cost
        margin = (profit / revenue * 100) if revenue > 0 else 0
        sens_data.append({
            "Harga (Rp)": f"{int(p):,}",
            "Pendapatan": f"Rp {revenue:,.0f}",
            "Profit": f"Rp {profit:,.0f}",
            "Margin": f"{margin:.1f}%",
            "Status": "✅ Untung" if profit > 0 else "❌ Rugi"
        })
    
    st.dataframe(pd.DataFrame(sens_data), use_container_width=True, hide_index=True)

# Footer
st.markdown("---")
st.caption("🌸 Budidaya Krisan Pro - Kalkulator Produksi")

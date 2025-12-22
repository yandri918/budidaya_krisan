# 📊 Kalkulator Produksi Krisan
# Estimasi hasil dan analisis finansial

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(page_title="Kalkulator Produksi", page_icon="📊", layout="wide")

st.markdown("## 📊 Kalkulator Produksi & Profit Krisan Spray")
st.info("Hitung estimasi hasil panen, biaya produksi, dan proyeksi keuntungan usaha Anda.")

# ========== INPUT SECTION ==========
col_input, col_result = st.columns([1, 1.5])

with col_input:
    st.subheader("📝 Input Data Usaha")
    
    # Varietas
    variety = st.selectbox(
        "🌸 Pilih Varietas",
        ["Krisan Spray Putih", "Krisan Spray Pink", "Krisan Spray Kuning"]
    )
    
    # Skala
    greenhouse_area = st.number_input("📐 Luas Greenhouse (m²)", 100, 10000, 500, step=100)
    
    # Densitas tanam
    density = st.slider("🌱 Densitas Tanam (tanaman/m²)", 40, 80, 64, 
                        help="Standar: 64 tanaman/m² (jarak 12.5x12.5 cm)")
    
    # Siklus per tahun
    cycles_per_year = st.slider("🔄 Siklus per Tahun", 2, 4, 3,
                                help="1 siklus = 105-120 hari")
    
    st.markdown("---")
    st.markdown("**💰 Parameter Harga**")
    
    selling_price = st.number_input("Harga Jual (Rp/tangkai)", 5000, 30000, 12000, step=500)
    
    # Production costs
    with st.expander("🧮 Detail Biaya Produksi (per siklus)", expanded=False):
        cost_cutting = st.number_input("Bibit/Stek (Rp/batang)", 200, 1000, 400)
        cost_fertilizer = st.number_input("Pupuk (Rp/m²)", 1000, 5000, 2500)
        cost_pesticide = st.number_input("Pestisida (Rp/m²)", 500, 3000, 1500)
        cost_labor_daily = st.number_input("Tenaga Kerja (Rp/hari)", 50000, 150000, 80000)
        labor_days = st.number_input("Hari Kerja per Siklus", 30, 120, 90)
        cost_electricity = st.number_input("Listrik/Lampu (Rp/bulan)", 200000, 2000000, 500000)
        cost_other = st.number_input("Biaya Lain-lain (Rp/siklus)", 0, 5000000, 500000)

with col_result:
    st.subheader("📈 Hasil Perhitungan")
    
    # Calculations
    total_plants = greenhouse_area * density
    
    # Assume 85% survival rate
    survival_rate = 0.85
    harvested_plants = int(total_plants * survival_rate)
    
    # Assume 3-4 tangkai per tanaman (spray type)
    stems_per_plant = 3.5
    total_stems = int(harvested_plants * stems_per_plant)
    
    # Revenue
    revenue_per_cycle = total_stems * selling_price
    revenue_per_year = revenue_per_cycle * cycles_per_year
    
    # Costs
    cost_cuttings_total = total_plants * cost_cutting
    cost_fert_total = greenhouse_area * cost_fertilizer
    cost_pest_total = greenhouse_area * cost_pesticide
    cost_labor_total = cost_labor_daily * labor_days
    cost_elec_months = 4  # ~4 bulan per siklus
    cost_elec_total = cost_electricity * cost_elec_months
    
    total_cost_per_cycle = (cost_cuttings_total + cost_fert_total + cost_pest_total + 
                            cost_labor_total + cost_elec_total + cost_other)
    total_cost_per_year = total_cost_per_cycle * cycles_per_year
    
    # Profit
    profit_per_cycle = revenue_per_cycle - total_cost_per_cycle
    profit_per_year = profit_per_cycle * cycles_per_year
    
    # Profit margin
    margin = (profit_per_cycle / revenue_per_cycle * 100) if revenue_per_cycle > 0 else 0
    
    # Display metrics
    m1, m2, m3 = st.columns(3)
    
    with m1:
        st.metric("Total Tanaman", f"{total_plants:,}")
        st.metric("Survival Rate", f"{survival_rate*100:.0f}%")
    
    with m2:
        st.metric("Total Tangkai/Siklus", f"{total_stems:,}")
        st.metric("Siklus/Tahun", f"{cycles_per_year}x")
    
    with m3:
        st.metric("Tangkai/Tahun", f"{total_stems * cycles_per_year:,}")
    
    st.markdown("---")
    
    # Financial Summary
    st.markdown("### 💰 Ringkasan Finansial")
    
    fin1, fin2 = st.columns(2)
    
    with fin1:
        st.markdown("**Per Siklus (±4 bulan)**")
        st.metric("Pendapatan", f"Rp {revenue_per_cycle:,.0f}")
        st.metric("Total Biaya", f"Rp {total_cost_per_cycle:,.0f}")
        st.metric("Keuntungan Bersih", f"Rp {profit_per_cycle:,.0f}",
                  delta=f"Margin {margin:.1f}%",
                  delta_color="normal" if profit_per_cycle > 0 else "inverse")
    
    with fin2:
        st.markdown("**Per Tahun**")
        st.metric("Pendapatan", f"Rp {revenue_per_year:,.0f}")
        st.metric("Total Biaya", f"Rp {total_cost_per_year:,.0f}")
        st.metric("Keuntungan Bersih", f"Rp {profit_per_year:,.0f}",
                  delta_color="normal" if profit_per_year > 0 else "inverse")

st.markdown("---")

# Cost Breakdown Chart
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
        marker_colors=['#f472b6', '#a78bfa', '#60a5fa', '#34d399', '#fbbf24', '#9ca3af']
    )
])

fig.update_layout(
    title="Distribusi Biaya Produksi per Siklus",
    height=400
)

st.plotly_chart(fig, use_container_width=True)

# Break Even Analysis
st.markdown("---")
st.subheader("📈 Analisis Break Even Point (BEP)")

# BEP in units
bep_units = total_cost_per_cycle / selling_price if selling_price > 0 else 0
bep_pct = (bep_units / total_stems * 100) if total_stems > 0 else 0

col_bep1, col_bep2 = st.columns(2)

with col_bep1:
    st.metric("BEP (Tangkai)", f"{bep_units:,.0f} tangkai")
    st.metric("BEP (%)", f"{bep_pct:.1f}% dari produksi")

with col_bep2:
    if total_stems > bep_units:
        st.success(f"✅ Produksi melebihi BEP! Surplus {total_stems - bep_units:,.0f} tangkai ({100-bep_pct:.1f}%)")
    else:
        st.error(f"❌ Produksi di bawah BEP. Kurang {bep_units - total_stems:,.0f} tangkai")

# Sensitivity Analysis
st.markdown("---")
st.subheader("🎯 Analisis Sensitivitas Harga")

price_scenarios = [selling_price * 0.7, selling_price * 0.85, selling_price, 
                   selling_price * 1.15, selling_price * 1.3]
profits = [(total_stems * p) - total_cost_per_cycle for p in price_scenarios]

fig_sens = go.Figure()

fig_sens.add_trace(go.Bar(
    x=[f"Rp {int(p):,}" for p in price_scenarios],
    y=profits,
    marker_color=['#ef4444' if p < 0 else '#10b981' for p in profits],
    text=[f"Rp {p:,.0f}" for p in profits],
    textposition='outside'
))

fig_sens.update_layout(
    title="Keuntungan vs Harga Jual",
    xaxis_title="Harga Jual per Tangkai",
    yaxis_title="Keuntungan (Rp)",
    height=350
)

st.plotly_chart(fig_sens, use_container_width=True)

# Footer
st.markdown("---")
st.caption("🌸 Budidaya Krisan Pro - Kalkulator Produksi")

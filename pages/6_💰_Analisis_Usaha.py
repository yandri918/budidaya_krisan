# 💰 Analisis Usaha Krisan
# Business analysis, ROI, dan break-even

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Analisis Usaha", page_icon="💰", layout="wide")

st.markdown("## 💰 Analisis Usaha Budidaya Krisan Spray")
st.info("Perhitungan investasi, ROI, break-even point, dan proyeksi bisnis lengkap.")

tab1, tab2, tab3, tab4 = st.tabs(["🏗️ Investasi Awal", "📊 Analisis Operasional", "📈 ROI & Payback", "🎯 Skenario Bisnis"])

# TAB 1: Investasi Awal
with tab1:
    st.subheader("🏗️ Kalkulasi Investasi Awal")
    
    st.markdown("Masukkan parameter untuk menghitung kebutuhan modal awal:")
    
    col_in, col_out = st.columns([1, 1.5])
    
    with col_in:
        greenhouse_area = st.number_input("📐 Luas Greenhouse (m²)", 200, 5000, 1000, step=100)
        
        with st.expander("🏗️ Detail Biaya Konstruksi", expanded=True):
            cost_greenhouse_per_m2 = st.number_input("Biaya Greenhouse (Rp/m²)", 100000, 500000, 250000, step=10000)
            cost_irrigation = st.number_input("Sistem Irigasi (Rp total)", 5000000, 50000000, 15000000, step=1000000)
            cost_lighting = st.number_input("Instalasi Lampu (Rp total)", 5000000, 30000000, 10000000, step=1000000)
            cost_shading = st.number_input("Plastik Hitam/Shading (Rp total)", 2000000, 20000000, 5000000, step=500000)
            cost_equipment = st.number_input("Peralatan Lain (Rp)", 2000000, 20000000, 8000000, step=1000000)
        
        working_capital = st.number_input("💵 Modal Kerja Awal (3 bulan)", 10000000, 100000000, 30000000, step=5000000)
    
    with col_out:
        # Calculate totals
        cost_greenhouse_total = greenhouse_area * cost_greenhouse_per_m2
        total_fixed_investment = cost_greenhouse_total + cost_irrigation + cost_lighting + cost_shading + cost_equipment
        total_investment = total_fixed_investment + working_capital
        
        st.markdown("### 📊 Ringkasan Investasi")
        
        investment_data = pd.DataFrame({
            "Komponen": ["Konstruksi Greenhouse", "Sistem Irigasi", "Instalasi Lampu", 
                        "Plastik Hitam/Shading", "Peralatan Lain", "Modal Kerja"],
            "Biaya (Rp)": [cost_greenhouse_total, cost_irrigation, cost_lighting, 
                          cost_shading, cost_equipment, working_capital]
        })
        
        st.dataframe(investment_data, use_container_width=True, hide_index=True)
        
        st.metric("**TOTAL INVESTASI**", f"Rp {total_investment:,.0f}")
        st.metric("Investasi per m²", f"Rp {total_investment/greenhouse_area:,.0f}/m²")
        
        # Pie chart
        fig = go.Figure(data=[go.Pie(
            labels=investment_data["Komponen"],
            values=investment_data["Biaya (Rp)"],
            hole=0.4,
            marker_colors=['#ec4899', '#f472b6', '#f9a8d4', '#fbcfe8', '#fce7f3', '#10b981']
        )])
        fig.update_layout(title="Distribusi Investasi", height=350)
        st.plotly_chart(fig, use_container_width=True)

# TAB 2: Analisis Operasional
with tab2:
    st.subheader("📊 Analisis Biaya & Pendapatan Operasional")
    
    # Sync with house_database
    if 'house_database' in st.session_state and st.session_state.house_database:
        house_db = st.session_state.house_database
        num_houses = len(house_db)
        total_beds = sum(h.get('beds', 12) for h in house_db.values())
        total_plants_synced = sum(h.get('total_plants', 0) for h in house_db.values())
        
        st.success(f"📊 Data tersinkronisasi: **{num_houses} house**, **{total_beds} bedengan**, **{total_plants_synced:,} tanaman/siklus**")
        use_synced = True
    else:
        use_synced = False
        total_plants_synced = 0
        st.info("💡 Sinkronkan data dari Kalkulator Produksi untuk hasil akurat")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📝 Parameter Produksi")
        
        if use_synced and total_plants_synced > 0:
            total_plants = total_plants_synced
            st.metric("🌱 Tanaman per Siklus (synced)", f"{total_plants:,}")
        else:
            density = st.slider("Densitas (tanaman/m²)", 40, 80, 64)
            total_plants = greenhouse_area * density
        
        survival_rate = st.slider("✅ Survival Rate (%)", 70, 95, 90) / 100
        stems_per_plant = st.slider("🌸 Tangkai per Tanaman", 1.0, 2.0, 1.0, 0.5, help="1 tanaman = 1 tangkai bunga")
        cycles_per_year = st.slider("📅 Siklus per Tahun", 2, 4, 3)
        
        st.markdown("### 💰 Parameter Harga")
        
        avg_selling_price = st.number_input("💵 Harga Jual Rata-rata (Rp/tangkai)", 500, 5000, 1000, step=100)
        
    with col2:
        st.markdown("### 📋 Biaya Operasional per Siklus")
        
        # Calculate production
        harvested = int(total_plants * survival_rate)
        total_stems = int(harvested * stems_per_plant)
        
        # Revenue
        revenue_cycle = total_stems * avg_selling_price
        revenue_year = revenue_cycle * cycles_per_year
        
        # Costs per cycle
        cost_cutting = total_plants * 400  # Rp 400/stek
        if use_synced:
            cost_fertilizer = total_beds * 50000  # Rp 50rb/bedengan
            cost_pesticide = total_beds * 30000   # Rp 30rb/bedengan
        else:
            cost_fertilizer = greenhouse_area * 2500
            cost_pesticide = greenhouse_area * 1500
        cost_electricity = 500000 * 4  # 4 bulan per siklus
        cost_labor = 80000 * 90  # 90 hari kerja
        cost_other = 2000000
        
        total_cost_cycle = cost_cutting + cost_fertilizer + cost_pesticide + cost_electricity + cost_labor + cost_other
        total_cost_year = total_cost_cycle * cycles_per_year
        
        profit_cycle = revenue_cycle - total_cost_cycle
        profit_year = profit_cycle * cycles_per_year
        
        # Display
        st.metric("🌸 Produksi per Siklus", f"{total_stems:,} tangkai")
        st.metric("💵 Pendapatan per Siklus", f"Rp {revenue_cycle:,.0f}")
        st.metric("💸 Biaya per Siklus", f"Rp {total_cost_cycle:,.0f}")
        
        margin_pct = (profit_cycle/revenue_cycle*100) if revenue_cycle > 0 else 0
        st.metric("📈 **PROFIT per Siklus**", f"Rp {profit_cycle:,.0f}", 
                  delta=f"Margin {margin_pct:.1f}%")
    
    st.markdown("---")
    
    # Annual summary
    st.markdown("### 📅 Ringkasan Tahunan")
    
    annual_cols = st.columns(4)
    
    with annual_cols[0]:
        st.metric("Produksi/Tahun", f"{total_stems * cycles_per_year:,} tangkai")
    with annual_cols[1]:
        st.metric("Pendapatan/Tahun", f"Rp {revenue_year:,.0f}")
    with annual_cols[2]:
        st.metric("Biaya/Tahun", f"Rp {total_cost_year:,.0f}")
    with annual_cols[3]:
        st.metric("**PROFIT/Tahun**", f"Rp {profit_year:,.0f}")

# TAB 3: ROI & Payback
with tab3:
    st.subheader("📈 Return on Investment & Payback Period")
    
    # Use values from previous tabs (simplified recalculation)
    if 'total_investment' not in dir():
        total_investment = 200000000  # Default
    if 'profit_year' not in dir():
        profit_year = 50000000  # Default
    
    # ROI
    roi = (profit_year / total_investment) * 100 if total_investment > 0 else 0
    
    # Payback period
    payback_months = (total_investment / profit_year * 12) if profit_year > 0 else 999
    payback_years = payback_months / 12
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Investasi", f"Rp {total_investment:,.0f}")
    with col2:
        st.metric("Profit Tahunan", f"Rp {profit_year:,.0f}")
    with col3:
        st.metric("ROI", f"{roi:.1f}%/tahun")
    
    st.markdown("---")
    
    st.markdown("### ⏱️ Payback Period")
    
    if payback_years <= 3:
        color = "🟢"
        status = "SANGAT BAIK"
    elif payback_years <= 5:
        color = "🟡"
        status = "BAIK"
    else:
        color = "🔴"
        status = "PERLU EVALUASI"
    
    st.markdown(f"""
    ### {color} {payback_years:.1f} Tahun ({payback_months:.0f} bulan)
    
    **Status:** {status}
    """)
    
    # Cumulative cash flow chart
    st.markdown("### 📊 Proyeksi Arus Kas Kumulatif")
    
    years = list(range(0, 6))
    cash_flow = [-total_investment]
    for y in range(1, 6):
        cash_flow.append(cash_flow[-1] + profit_year)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=years,
        y=cash_flow,
        mode='lines+markers',
        name='Kumulatif Cash Flow',
        line=dict(color='#ec4899', width=3),
        marker=dict(size=10)
    ))
    
    fig.add_hline(y=0, line_dash="dash", line_color="gray",
                  annotation_text="Break Even Point")
    
    fig.update_layout(
        xaxis_title="Tahun",
        yaxis_title="Cash Flow Kumulatif (Rp)",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

# TAB 4: Skenario Bisnis
with tab4:
    st.subheader("🎯 Simulasi Skenario Bisnis")
    
    st.markdown("Bandingkan berbagai skenario untuk pengambilan keputusan:")
    
    scenarios = {
        "Konservatif": {"price": 10000, "survival": 0.80, "stems": 3.0, "cycles": 2},
        "Moderat": {"price": 12000, "survival": 0.85, "stems": 3.5, "cycles": 3},
        "Optimis": {"price": 15000, "survival": 0.90, "stems": 4.0, "cycles": 3},
    }
    
    scenario_results = []
    
    for name, params in scenarios.items():
        plants = greenhouse_area * 64
        harvested = plants * params["survival"]
        stems = harvested * params["stems"]
        revenue = stems * params["price"]
        cost = plants * 400 + greenhouse_area * 4500 + 80000 * 90 + 2500000
        profit = (revenue - cost) * params["cycles"]
        
        scenario_results.append({
            "Skenario": name,
            "Harga Jual": f"Rp {params['price']:,}",
            "Survival": f"{params['survival']*100:.0f}%",
            "Tangkai/Tanaman": params["stems"],
            "Siklus/Tahun": params["cycles"],
            "Profit Tahunan": f"Rp {profit:,.0f}",
            "ROI": f"{(profit/total_investment)*100:.1f}%"
        })
    
    df_scenarios = pd.DataFrame(scenario_results)
    st.dataframe(df_scenarios, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Risk factors
    st.markdown("### ⚠️ Faktor Risiko")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Risiko Produksi:**
        - 🔴 Serangan hama/penyakit (terutama white rust)
        - 🟠 Gagal photoperiod → bunga tidak keluar
        - 🟡 Cuaca ekstrem → kualitas turun
        - 🟡 Bibit berkualitas rendah
        """)
    
    with col2:
        st.markdown("""
        **Risiko Pasar:**
        - 🔴 Fluktuasi harga musiman
        - 🟠 Kompetisi dengan impor
        - 🟡 Penurunan permintaan (resesi)
        - 🟢 Diversifikasi warna = mitigasi
        """)
    
    st.success("""
    **💡 Rekomendasi Mitigasi:**
    1. Asuransi pertanian (jika tersedia)
    2. Kontrak dengan buyer (florist, hotel)
    3. Diversifikasi 3 warna untuk spread risiko
    4. Emergency fund 2-3 bulan operasional
    """)

# Footer
st.markdown("---")
st.caption("🌸 Budidaya Krisan Pro - Analisis Usaha")

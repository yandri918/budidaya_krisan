# 📊 Kalkulator Budidaya Krisan Spray
# Populasi, Irigasi, RAB, dan AI Optimasi

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(page_title="Kalkulator Budidaya", page_icon="📊", layout="wide")

# CSS Styling
st.markdown("""
<style>
    .calc-card {
        background: linear-gradient(135deg, #ecfdf5 0%, #ffffff 100%);
        border: 1px solid #a7f3d0;
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    .sync-badge {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
        border: 1px solid #93c5fd;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
        font-size: 0.9rem;
    }
    .result-box {
        background: #f0fdf4;
        border-left: 4px solid #10b981;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    .warning-box {
        background: #fef3c7;
        border-left: 4px solid #f59e0b;
        padding: 1rem;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("## 📊 Kalkulator Budidaya Krisan Spray")
st.info("Perhitungan lengkap: Populasi, Irigasi, RAB, dan Rekomendasi AI Optimasi")

# ========== INITIALIZE SESSION STATE ==========
if 'krisan_data' not in st.session_state:
    st.session_state.krisan_data = {
        'total_plants': 0,
        'total_bed_area': 0,
        'num_beds': 0,
        'total_stems': 0,
        'nozzle_count': 0,
        'irrigation_cost': 0,
    }

# ========== TABS ==========
tab1, tab2, tab3, tab4 = st.tabs([
    "🌱 Populasi Tanaman", 
    "💧 Nozzle & Irigasi", 
    "💰 RAB Lengkap",
    "🤖 AI Optimasi"
])

# ==================== TAB 1: POPULASI ====================
with tab1:
    st.subheader("🌱 Perhitungan Populasi Tanaman")
    
    # ========== KONFIGURASI HOUSE ==========
    st.markdown("### 🏠 Konfigurasi House/Greenhouse")
    
    # Initialize house database in session state
    if 'house_database' not in st.session_state:
        st.session_state.house_database = {}
    
    house_config_cols = st.columns([1, 1, 1])
    
    with house_config_cols[0]:
        num_houses = st.number_input(
            "🏠 Jumlah House",
            min_value=1, max_value=20, value=4,
            help="Total greenhouse yang akan dikelola"
        )
    
    with house_config_cols[1]:
        beds_per_house_config = st.number_input(
            "📦 Bedengan per House",
            min_value=4, max_value=50, value=12,
            help="Jumlah bedengan dalam satu greenhouse"
        )
    
    with house_config_cols[2]:
        st.metric("📊 Total Bedengan", f"{num_houses * beds_per_house_config}")
    
    # House naming
    with st.expander("✏️ Konfigurasi Nama House", expanded=False):
        st.info("Beri nama setiap house untuk identifikasi")
        
        house_names = {}
        name_cols = st.columns(min(4, num_houses))
        
        for i in range(num_houses):
            col_idx = i % 4
            with name_cols[col_idx]:
                default_name = st.session_state.house_database.get(f"house_{i+1}", {}).get('name', f"House {i+1}")
                house_names[f"house_{i+1}"] = st.text_input(
                    f"House {i+1}",
                    value=default_name,
                    key=f"house_name_{i+1}"
                )
        
        if st.button("💾 Simpan Konfigurasi House", type="primary"):
            for i in range(num_houses):
                key = f"house_{i+1}"
                st.session_state.house_database[key] = {
                    'name': house_names[key],
                    'beds': beds_per_house_config,
                    'id': i + 1
                }
            st.session_state.krisan_data['num_houses'] = num_houses
            st.session_state.krisan_data['beds_per_house'] = beds_per_house_config
            st.success(f"✅ {num_houses} house tersimpan ke database!")
    
    # Show saved houses
    if st.session_state.house_database:
        st.markdown("#### 📋 Database House Tersimpan")
        house_list = []
        for key, data in st.session_state.house_database.items():
            house_list.append({
                "ID": data.get('id', 0),
                "Nama House": data.get('name', key),
                "Bedengan": data.get('beds', 12)
            })
        if house_list:
            st.dataframe(pd.DataFrame(house_list), use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    col_bed, col_result = st.columns([1.2, 1])
    
    with col_bed:
        st.markdown("### 📐 Konfigurasi Bedengan")
        
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
            "🔢 Jumlah Bedengan Total", 
            min_value=1, max_value=100, value=num_houses * beds_per_house_config, step=1,
            help="Total bedengan dalam greenhouse"
        )
        
        # ========== PROPORSI BEDENGAN PER VARIETAS ==========
        st.markdown("### 🌸 Proporsi Bedengan per Varietas")
        st.caption("Tentukan pembagian bedengan untuk setiap warna krisan")
        
        var_cols = st.columns(3)
        
        with var_cols[0]:
            beds_putih = st.number_input("🤍 Bedengan Putih", 0, num_beds, 4, key="calc_beds_putih")
        with var_cols[1]:
            beds_pink = st.number_input("💗 Bedengan Pink", 0, num_beds, 4, key="calc_beds_pink")
        with var_cols[2]:
            beds_kuning = st.number_input("💛 Bedengan Kuning", 0, num_beds, 4, key="calc_beds_kuning")
        
        total_assigned = beds_putih + beds_pink + beds_kuning
        
        if total_assigned != num_beds:
            st.warning(f"⚠️ Total bedengan varietas ({total_assigned}) tidak sama dengan total bedengan ({num_beds})")
        else:
            st.success(f"✅ Semua {num_beds} bedengan sudah dialokasikan")
        
        st.markdown("### 🌿 Konfigurasi Tanam")
        
        rows_per_bed = st.selectbox(
            "📊 Jumlah Baris per Bedengan",
            options=[6, 7, 8, 9, 10],
            index=2,
            help="Standar: 8 baris untuk lebar 100cm"
        )
        
        plant_spacing = st.selectbox(
            "↔️ Jarak Tanam dalam Baris (cm)",
            options=[10.0, 12.5, 15.0],
            index=1,
            format_func=lambda x: f"{x} cm"
        )
        
        survival_rate = st.slider("📊 Survival Rate (%)", 70, 98, 85)
        stems_per_plant = st.slider("🌸 Tangkai/Tanaman", 2.0, 5.0, 3.5, 0.5)
    
    with col_result:
        st.markdown("### 📊 Hasil Perhitungan")
        
        # CALCULATIONS
        plants_per_row = int((bed_length * 100) / plant_spacing)
        plants_per_bed = plants_per_row * rows_per_bed
        total_plants = plants_per_bed * num_beds
        bed_area_m2 = (bed_length * (bed_width / 100))
        total_bed_area = bed_area_m2 * num_beds
        actual_density = total_plants / total_bed_area if total_bed_area > 0 else 0
        surviving_plants = int(total_plants * (survival_rate / 100))
        total_stems = int(surviving_plants * stems_per_plant)
        
        # Update session state
        st.session_state.krisan_data['total_plants'] = total_plants
        st.session_state.krisan_data['total_bed_area'] = total_bed_area
        st.session_state.krisan_data['num_beds'] = num_beds
        st.session_state.krisan_data['total_stems'] = total_stems
        st.session_state.krisan_data['surviving_plants'] = surviving_plants
        st.session_state.krisan_data['bed_length'] = bed_length
        st.session_state.krisan_data['plants_per_bed'] = plants_per_bed
        st.session_state.krisan_data['actual_density'] = actual_density
        st.session_state.krisan_data['survival_rate'] = survival_rate
        st.session_state.krisan_data['stems_per_plant'] = stems_per_plant
        
        # Variety data for sync with Pasca Panen
        st.session_state.krisan_data['beds_putih'] = beds_putih
        st.session_state.krisan_data['beds_pink'] = beds_pink
        st.session_state.krisan_data['beds_kuning'] = beds_kuning
        st.session_state.krisan_data['plants_putih'] = beds_putih * plants_per_bed
        st.session_state.krisan_data['plants_pink'] = beds_pink * plants_per_bed
        st.session_state.krisan_data['plants_kuning'] = beds_kuning * plants_per_bed
        
        # Display
        st.metric("🌱 Tanaman per Baris", f"{plants_per_row:,}")
        st.metric("📦 Tanaman per Bedengan", f"{plants_per_bed:,}")
        st.metric("🌿 **TOTAL TANAMAN**", f"{total_plants:,}")
        
        st.markdown("---")
        
        st.metric("✅ Tanaman Hidup", f"{surviving_plants:,}", f"Survival {survival_rate}%")
        st.metric("🌸 **TOTAL TANGKAI**", f"{total_stems:,}", f"{stems_per_plant} tangkai/tanaman")
        
        st.markdown("---")
        
        st.metric("📐 Luas Bedengan Total", f"{total_bed_area:.1f} m²")
        st.metric("📊 Densitas", f"{actual_density:.1f} tanaman/m²")

# ==================== TAB 2: NOZZLE & IRIGASI ====================
with tab2:
    st.subheader("💧 Perhitungan Nozzle & Sistem Irigasi")
    
    # Sync badge
    data = st.session_state.krisan_data
    st.markdown(f"""
    <div class="sync-badge">
        📊 <strong>Data Tersinkronisasi:</strong> 
        🌱 Populasi: <strong>{data.get('total_plants', 0):,}</strong> tanaman | 
        📐 Luas: <strong>{data.get('total_bed_area', 0):.1f}</strong> m² |
        📦 Bedengan: <strong>{data.get('num_beds', 0)}</strong> unit
    </div>
    """, unsafe_allow_html=True)
    
    col_irr, col_res = st.columns([1, 1])
    
    with col_irr:
        st.markdown("### ⚙️ Konfigurasi Sistem Irigasi")
        
        irrigation_type = st.selectbox(
            "💧 Jenis Irigasi",
            ["Drip Irrigation", "Sprinkler/Misting", "Manual Selang"]
        )
        
        if irrigation_type == "Drip Irrigation":
            nozzle_spacing = st.selectbox(
                "↔️ Jarak Antar Dripper (cm)",
                [15, 20, 25, 30],
                index=1,
                help="Jarak dripper dalam selang PE"
            )
            lines_per_bed = st.selectbox(
                "📏 Jumlah Lateral per Bedengan",
                [2, 3, 4],
                index=1,
                help="Jumlah selang PE per bedengan"
            )
        elif irrigation_type == "Sprinkler/Misting":
            nozzle_spacing = st.selectbox(
                "↔️ Jarak Antar Nozzle (meter)",
                [1, 1.5, 2, 2.5, 3],
                index=2
            )
            lines_per_bed = 1
        else:
            nozzle_spacing = 100
            lines_per_bed = 1
        
        st.markdown("### 💰 Biaya Komponen")
        
        price_per_nozzle = st.number_input(
            "💧 Harga per Nozzle/Dripper (Rp)",
            500, 10000, 2500, 100
        )
        
        price_pe_pipe = st.number_input(
            "🔧 Harga Pipa PE per meter (Rp)",
            2000, 20000, 5000, 500
        )
        
        price_mainpipe = st.number_input(
            "🔧 Harga Pipa Utama PVC per meter (Rp)",
            10000, 50000, 25000, 1000
        )
        
        mainpipe_length = st.number_input(
            "📏 Panjang Pipa Utama (meter)",
            10, 200, 50, 5
        )
        
        price_pump = st.number_input(
            "⚙️ Harga Pompa (Rp)",
            500000, 5000000, 1500000, 100000
        )
        
        price_filter = st.number_input(
            "🔧 Harga Filter & Fitting (Rp)",
            200000, 2000000, 500000, 50000
        )
    
    with col_res:
        st.markdown("### 📊 Hasil Perhitungan Irigasi")
        
        # Get data from session
        num_beds = data.get('num_beds', 12)
        bed_length = data.get('bed_length', 25)
        total_bed_area = data.get('total_bed_area', 300)
        
        # Calculate nozzles
        if irrigation_type == "Drip Irrigation":
            nozzles_per_line = int((bed_length * 100) / nozzle_spacing)
            nozzles_per_bed = nozzles_per_line * lines_per_bed
            total_nozzles = nozzles_per_bed * num_beds
            pe_length_per_bed = bed_length * lines_per_bed
            total_pe_length = pe_length_per_bed * num_beds
        elif irrigation_type == "Sprinkler/Misting":
            nozzles_per_bed = int(bed_length / nozzle_spacing) + 1
            total_nozzles = nozzles_per_bed * num_beds
            total_pe_length = bed_length * num_beds
        else:
            total_nozzles = 0
            total_pe_length = 0
        
        # Costs
        cost_nozzles = total_nozzles * price_per_nozzle
        cost_pe = total_pe_length * price_pe_pipe
        cost_mainpipe = mainpipe_length * price_mainpipe
        total_irrigation_cost = cost_nozzles + cost_pe + cost_mainpipe + price_pump + price_filter
        
        # Update session state
        st.session_state.krisan_data['nozzle_count'] = total_nozzles
        st.session_state.krisan_data['irrigation_cost'] = total_irrigation_cost
        
        # Display
        st.metric("💧 Total Nozzle/Dripper", f"{total_nozzles:,}")
        st.metric("📏 Total Pipa PE", f"{total_pe_length:.0f} meter")
        
        st.markdown("---")
        
        st.markdown("**💰 Rincian Biaya Irigasi:**")
        
        irr_breakdown = pd.DataFrame({
            "Komponen": ["Nozzle/Dripper", "Pipa PE", "Pipa Utama PVC", "Pompa", "Filter & Fitting"],
            "Biaya": [cost_nozzles, cost_pe, cost_mainpipe, price_pump, price_filter]
        })
        
        for _, row in irr_breakdown.iterrows():
            st.markdown(f"- {row['Komponen']}: **Rp {row['Biaya']:,.0f}**")
        
        st.markdown("---")
        st.metric("💰 **TOTAL BIAYA IRIGASI**", f"Rp {total_irrigation_cost:,.0f}")
        
        cost_per_m2 = total_irrigation_cost / total_bed_area if total_bed_area > 0 else 0
        st.caption(f"Biaya per m²: Rp {cost_per_m2:,.0f}")

# ==================== TAB 3: RAB LENGKAP ====================
with tab3:
    st.subheader("💰 Rencana Anggaran Biaya (RAB) Lengkap")
    
    # Sync badge
    data = st.session_state.krisan_data
    st.markdown(f"""
    <div class="sync-badge">
        📊 <strong>Data Tersinkronisasi dari Tab Lain:</strong><br>
        🌱 Populasi: <strong>{data.get('total_plants', 0):,}</strong> tanaman | 
        Luas: <strong>{data.get('total_bed_area', 0):.1f}</strong> m²<br>
        💧 Irigasi: <strong>{data.get('nozzle_count', 0):,}</strong> nozzle | 
        Biaya Instalasi: <strong>Rp {data.get('irrigation_cost', 0):,.0f}</strong>
    </div>
    """, unsafe_allow_html=True)
    
    col_rab1, col_rab2 = st.columns([1, 1])
    
    with col_rab1:
        st.markdown("### 🏗️ A. Investasi Awal (Modal Tetap)")
        
        with st.expander("📐 Konstruksi Greenhouse", expanded=True):
            greenhouse_area = st.number_input("Luas Greenhouse (m²)", 100, 5000, 400, 50)
            cost_gh_per_m2 = st.number_input("Biaya per m² (Rp)", 100000, 500000, 250000, 10000)
            cost_greenhouse = greenhouse_area * cost_gh_per_m2
            st.metric("Subtotal Greenhouse", f"Rp {cost_greenhouse:,.0f}")
        
        with st.expander("💧 Sistem Irigasi (dari Tab 2)"):
            irrigation_cost = data.get('irrigation_cost', 7500000)
            st.metric("Subtotal Irigasi", f"Rp {irrigation_cost:,.0f}")
        
        with st.expander("💡 Sistem Lampu (Photoperiod)"):
            num_lamps = st.number_input("Jumlah Lampu", 10, 200, 50, 5)
            cost_per_lamp = st.number_input("Harga per Lampu (Rp)", 50000, 500000, 150000, 10000)
            cost_installation = st.number_input("Biaya Instalasi Listrik (Rp)", 500000, 5000000, 2000000, 100000)
            cost_lighting = (num_lamps * cost_per_lamp) + cost_installation
            st.metric("Subtotal Lampu", f"Rp {cost_lighting:,.0f}")
        
        with st.expander("🌑 Plastik Hitam (Shading)"):
            shading_area = st.number_input("Luas Shading (m²)", 100, 5000, int(data.get('total_bed_area', 300)), 50)
            cost_shading_per_m2 = st.number_input("Harga Plastik per m² (Rp)", 5000, 30000, 15000, 1000)
            cost_shading = shading_area * cost_shading_per_m2
            st.metric("Subtotal Shading", f"Rp {cost_shading:,.0f}")
        
        with st.expander("🔧 Peralatan Lain"):
            cost_tools = st.number_input("Peralatan (gunting, ember, dll)", 1000000, 10000000, 3000000, 500000)
            st.metric("Subtotal Peralatan", f"Rp {cost_tools:,.0f}")
        
        total_investment = cost_greenhouse + irrigation_cost + cost_lighting + cost_shading + cost_tools
        
        st.markdown("---")
        st.metric("💼 **TOTAL INVESTASI AWAL**", f"Rp {total_investment:,.0f}")
    
    with col_rab2:
        st.markdown("### 💵 B. Biaya Operasional (per Siklus)")
        
        total_plants = data.get('total_plants', 20000)
        total_bed_area = data.get('total_bed_area', 300)
        
        with st.expander("🌱 Bibit/Stek", expanded=True):
            cost_cutting = st.number_input("Harga per Stek (Rp)", 200, 1000, 400, 50)
            cost_cuttings_total = total_plants * cost_cutting
            st.metric("Subtotal Bibit", f"Rp {cost_cuttings_total:,.0f}", f"{total_plants:,} stek")
        
        with st.expander("🧪 Pupuk"):
            cost_fertilizer_m2 = st.number_input("Biaya Pupuk per m² (Rp)", 1000, 10000, 3000, 200)
            cost_fertilizer = total_bed_area * cost_fertilizer_m2
            st.metric("Subtotal Pupuk", f"Rp {cost_fertilizer:,.0f}")
        
        with st.expander("🛡️ Pestisida"):
            cost_pesticide_m2 = st.number_input("Biaya Pestisida per m² (Rp)", 500, 5000, 2000, 200)
            cost_pesticide = total_bed_area * cost_pesticide_m2
            st.metric("Subtotal Pestisida", f"Rp {cost_pesticide:,.0f}")
        
        with st.expander("👷 Tenaga Kerja"):
            labor_daily = st.number_input("Upah Harian (Rp)", 50000, 150000, 80000, 5000)
            labor_days = st.number_input("Hari Kerja per Siklus", 60, 120, 90, 5)
            cost_labor = labor_daily * labor_days
            st.metric("Subtotal Tenaga Kerja", f"Rp {cost_labor:,.0f}")
        
        with st.expander("⚡ Listrik"):
            cost_electricity = st.number_input("Biaya Listrik per Bulan (Rp)", 200000, 2000000, 600000, 50000)
            months_per_cycle = 4
            cost_electricity_total = cost_electricity * months_per_cycle
            st.metric("Subtotal Listrik", f"Rp {cost_electricity_total:,.0f}", f"{months_per_cycle} bulan")
        
        with st.expander("📦 Lain-lain"):
            cost_other = st.number_input("Biaya Lain-lain (Rp)", 0, 5000000, 500000, 100000)
            st.metric("Subtotal Lainnya", f"Rp {cost_other:,.0f}")
        
        total_operational = cost_cuttings_total + cost_fertilizer + cost_pesticide + cost_labor + cost_electricity_total + cost_other
        
        # Save RAB estimates to session state for sync with Jurnal Harian
        st.session_state.krisan_data['rab_bibit'] = cost_cuttings_total
        st.session_state.krisan_data['rab_pupuk'] = cost_fertilizer
        st.session_state.krisan_data['rab_pestisida'] = cost_pesticide
        st.session_state.krisan_data['rab_tenaga_kerja'] = cost_labor
        st.session_state.krisan_data['rab_listrik'] = cost_electricity_total
        st.session_state.krisan_data['rab_lainnya'] = cost_other
        st.session_state.krisan_data['rab_total_operational'] = total_operational
        
        st.markdown("---")
        st.metric("💵 **TOTAL OPERASIONAL/SIKLUS**", f"Rp {total_operational:,.0f}")
    
    # SUMMARY
    st.markdown("---")
    st.subheader("📊 Ringkasan RAB & Proyeksi Keuntungan")
    
    col_sum1, col_sum2, col_sum3 = st.columns(3)
    
    total_stems = data.get('total_stems', 50000)
    
    with col_sum1:
        st.markdown("**📥 Pendapatan**")
        selling_price = st.number_input("Harga Jual (Rp/tangkai)", 5000, 25000, 12000, 500)
        cycles_per_year = st.selectbox("Siklus/Tahun", [2, 3], index=1)
        
        revenue_cycle = total_stems * selling_price
        revenue_year = revenue_cycle * cycles_per_year
        
        st.metric("Pendapatan/Siklus", f"Rp {revenue_cycle:,.0f}")
        st.metric("Pendapatan/Tahun", f"Rp {revenue_year:,.0f}")
    
    with col_sum2:
        st.markdown("**📤 Total Biaya**")
        operational_year = total_operational * cycles_per_year
        
        st.metric("Operasional/Siklus", f"Rp {total_operational:,.0f}")
        st.metric("Operasional/Tahun", f"Rp {operational_year:,.0f}")
        st.metric("Investasi Awal", f"Rp {total_investment:,.0f}")
    
    with col_sum3:
        st.markdown("**💰 Profit & ROI**")
        profit_cycle = revenue_cycle - total_operational
        profit_year = profit_cycle * cycles_per_year
        roi = (profit_year / total_investment * 100) if total_investment > 0 else 0
        payback = (total_investment / profit_year) if profit_year > 0 else 999
        
        st.metric("Profit/Siklus", f"Rp {profit_cycle:,.0f}",
                  delta_color="normal" if profit_cycle > 0 else "inverse")
        st.metric("Profit/Tahun", f"Rp {profit_year:,.0f}",
                  delta_color="normal" if profit_year > 0 else "inverse")
        st.metric("ROI", f"{roi:.1f}%/tahun")
        st.metric("Payback Period", f"{payback:.1f} tahun")

# ==================== TAB 4: AI OPTIMASI ====================
with tab4:
    st.subheader("🤖 AI Optimasi & Rekomendasi")
    
    data = st.session_state.krisan_data
    
    st.markdown(f"""
    <div class="sync-badge">
        📊 <strong>Analisis berdasarkan data Anda:</strong><br>
        🌱 {data.get('total_plants', 0):,} tanaman | 
        🌸 {data.get('total_stems', 0):,} tangkai | 
        📐 {data.get('total_bed_area', 0):.1f} m²
    </div>
    """, unsafe_allow_html=True)
    
    # AI Analysis
    total_plants = data.get('total_plants', 20000)
    total_stems = data.get('total_stems', 50000)
    total_bed_area = data.get('total_bed_area', 300)
    nozzle_count = data.get('nozzle_count', 1000)
    
    density = total_plants / total_bed_area if total_bed_area > 0 else 0
    
    st.markdown("### 🎯 Analisis & Rekomendasi")
    
    recommendations = []
    
    # Density analysis
    if density < 50:
        recommendations.append({
            "type": "warning",
            "title": "📊 Densitas Rendah",
            "desc": f"Densitas {density:.1f}/m² di bawah optimal (64/m²). Pertimbangkan mengurangi jarak tanam untuk meningkatkan produktivitas."
        })
    elif density > 80:
        recommendations.append({
            "type": "warning", 
            "title": "📊 Densitas Terlalu Tinggi",
            "desc": f"Densitas {density:.1f}/m² terlalu padat. Risiko: sirkulasi udara buruk, penyakit mudah menyebar. Kurangi baris atau tambah jarak tanam."
        })
    else:
        recommendations.append({
            "type": "success",
            "title": "✅ Densitas Optimal",
            "desc": f"Densitas {density:.1f}/m² sudah dalam range optimal (50-80/m²)."
        })
    
    # Irrigation analysis
    plants_per_nozzle = total_plants / nozzle_count if nozzle_count > 0 else 0
    if plants_per_nozzle > 25:
        recommendations.append({
            "type": "warning",
            "title": "💧 Nozzle Kurang",
            "desc": f"Ratio {plants_per_nozzle:.0f} tanaman/nozzle terlalu tinggi. Tambahkan nozzle untuk distribusi air merata."
        })
    elif nozzle_count > 0:
        recommendations.append({
            "type": "success",
            "title": "✅ Irigasi Memadai",
            "desc": f"Ratio {plants_per_nozzle:.0f} tanaman/nozzle sudah baik."
        })
    
    # Production optimization
    recommendations.append({
        "type": "info",
        "title": "💡 Tips Meningkatkan Produksi",
        "desc": """
        - Pinching yang tepat bisa meningkatkan tangkai/tanaman dari 3.5 ke 4-5
        - Photoperiod ketat (14 jam gelap) untuk pembungaan optimal
        - Suhu malam 15-18°C untuk warna bunga lebih intens
        """
    })
    
    # Market timing
    recommendations.append({
        "type": "info",
        "title": "📅 Timing Pasar",
        "desc": """
        **Peak Demand:** Valentine (Feb), Imlek (Jan-Feb), Mother's Day (Mei)
        **Strategi:** Tanam mundur 105 hari dari peak untuk panen tepat waktu.
        """
    })
    
    # Display recommendations
    for rec in recommendations:
        if rec["type"] == "success":
            st.success(f"**{rec['title']}**\n\n{rec['desc']}")
        elif rec["type"] == "warning":
            st.warning(f"**{rec['title']}**\n\n{rec['desc']}")
        else:
            st.info(f"**{rec['title']}**\n\n{rec['desc']}")
    
    # Profit optimization scenarios
    st.markdown("---")
    st.markdown("### 📈 Skenario Optimasi Profit")
    
    scenarios = pd.DataFrame({
        "Skenario": ["Kondisi Saat Ini", "Optimasi Densitas", "Tingkatkan Survival", "Premium Market"],
        "Tanaman": [total_plants, int(total_plants * 1.2), total_plants, total_plants],
        "Survival": [85, 85, 92, 85],
        "Harga": [12000, 12000, 12000, 18000],
        "Tangkai/Tanaman": [3.5, 3.5, 3.5, 3.5]
    })
    
    scenarios["Tangkai"] = (scenarios["Tanaman"] * scenarios["Survival"] / 100 * scenarios["Tangkai/Tanaman"]).astype(int)
    scenarios["Pendapatan"] = scenarios["Tangkai"] * scenarios["Harga"]
    scenarios["Pendapatan (Rp)"] = scenarios["Pendapatan"].apply(lambda x: f"Rp {x:,.0f}")
    
    # Calculate potential increase
    base_revenue = scenarios.iloc[0]["Pendapatan"]
    scenarios["Peningkatan"] = ((scenarios["Pendapatan"] - base_revenue) / base_revenue * 100).apply(lambda x: f"+{x:.1f}%" if x > 0 else "-")
    
    st.dataframe(
        scenarios[["Skenario", "Tanaman", "Survival", "Harga", "Tangkai", "Pendapatan (Rp)", "Peningkatan"]],
        use_container_width=True,
        hide_index=True
    )

# Footer
st.markdown("---")
st.caption("🌸 Budidaya Krisan Pro - Kalkulator Lengkap dengan Sinkronisasi Data")

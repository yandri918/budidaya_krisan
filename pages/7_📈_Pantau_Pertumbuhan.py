import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random
import requests
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Pantau Pertumbuhan", page_icon="📈", layout="wide")

# CSS Custom
st.markdown("""
<style>
    .growth-card {
        background-color: #f0fdf4;
        border: 1px solid #bbf7d0;
        border-radius: 10px;
        padding: 1.5rem;
        text-align: center;
    }
    .metric-value {
        font_size: 2rem;
        font-weight: bold;
        color: #15803d;
    }
    .metric-label {
        color: #64748b;
        font-size: 0.9rem;
    }
    .status-badge-ok {
        background-color: #dcfce7;
        color: #166534;
        padding: 0.2rem 0.6rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .status-badge-warning {
        background-color: #fef9c3;
        color: #854d0e;
        padding: 0.2rem 0.6rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .status-badge-danger {
        background-color: #fee2e2;
        color: #991b1b;
        padding: 0.2rem 0.6rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .weather-widget {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

st.title("📈 Pantau Pertumbuhan & AI Analysis")
st.info("Monitor perkembangan tanaman mingguan dan dapatkan rekomendasi budidaya cerdas berbasis AI.")

# Initialize session state for growth data
if 'growth_data' not in st.session_state:
    st.session_state.growth_data = []

# Fetch Weather Function
def get_open_meteo_weather(lat, lon):
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,rain,surface_pressure,wind_speed_10m&timezone=auto"
        response = requests.get(url)
        data = response.json()
        return data['current']
    except Exception as e:
        st.error(f"Gagal mengambil data cuaca: {e}")
        return None

# ==================== DATA INPUT ====================
with st.sidebar:
    st.header("📝 Input Data Pemantauan")
    
    # Get house list
    if 'house_database' in st.session_state and st.session_state.house_database:
        house_options = [h['name'] for h in st.session_state.house_database.values()]
    else:
        house_options = ["House 1", "House 2", "House 3"]
        
    input_house = st.selectbox("🏠 Pilih House", house_options)
    input_date = st.date_input("📅 Tanggal Cek", datetime.now())
    
    # Calculate HST estimation based on planting date (simulated if no data)
    start_date = datetime.now() - timedelta(days=28) # Assume 4 weeks ago
    hst_est = (pandas_date := pd.to_datetime(input_date) - pd.to_datetime(start_date)).days
    hst_est = max(1, hst_est)
    
    input_week = st.number_input("📅 Minggu ke- (HST)", 1, 16, 4, help="Hari Setelah Tanam (dalam minggu)")
    
    st.markdown("---")
    st.markdown("### 📍 Lokasi Kebun (Open-Meteo)")
    
    # Initialize lat/lon in session state if not exist
    if 'map_lat' not in st.session_state:
        st.session_state.map_lat = -6.80
    if 'map_lon' not in st.session_state:
        st.session_state.map_lon = 107.60

    # Input widgets linked to session state
    lat = st.number_input("Latitude", value=st.session_state.map_lat, format="%.4f", key="input_lat")
    lon = st.number_input("Longitude", value=st.session_state.map_lon, format="%.4f", key="input_lon")
    
    # Sync input changes back to map state
    st.session_state.map_lat = lat
    st.session_state.map_lon = lon
    
    current_weather = None
    if st.button("📡 Ambil Data Cuaca Real-time"):
        current_weather = get_open_meteo_weather(lat, lon)
        if current_weather:
            st.session_state.weather_cache = current_weather
            st.success("Data Open-Meteo berhasil diambil!")
            
    # Interactive Map
    st.caption("Klik pada peta untuk pilih lokasi:")
    with st.expander("🗺️ Lihat Peta Lokasi", expanded=True):
        m = folium.Map(location=[st.session_state.map_lat, st.session_state.map_lon], zoom_start=13)
        m.add_child(folium.LatLngPopup()) # Enable click popup
        
        folium.Marker(
            [st.session_state.map_lat, st.session_state.map_lon], 
            popup="Lokasi Kebun", 
            tooltip="Kebun Krisan",
            icon=folium.Icon(color="red", icon="home")
        ).add_to(m)
        
        # Capture map clicks
        map_data = st_folium(m, height=250, width=280)

    # Update state if map is clicked (Click-to-Pick Logic)
    if map_data and map_data.get("last_clicked"):
        clicked_lat = map_data["last_clicked"]["lat"]
        clicked_lon = map_data["last_clicked"]["lng"]
        
        # Only rerun if location actually changed to prevent loop
        if abs(clicked_lat - st.session_state.map_lat) > 0.0001 or abs(clicked_lon - st.session_state.map_lon) > 0.0001:
            st.session_state.map_lat = clicked_lat
            st.session_state.map_lon = clicked_lon
            st.rerun()
    
    # Use cached weather if available logic
    default_temp = 24.5
    default_humid = 75
    
    if 'weather_cache' in st.session_state:
        weather = st.session_state.weather_cache
        default_temp = float(weather.get('temperature_2m', 24.5))
        default_humid = int(weather.get('relative_humidity_2m', 75))

    st.markdown("---")
    st.markdown("### 🌱 Parameter Tanaman")
    
    in_height = st.number_input("Tinggi Tanaman (cm)", 0.0, 150.0, 25.0, step=0.5)
    in_leaves = st.number_input("Jumlah Daun (helai)", 0, 50, 12, step=1)
    in_diameter = st.number_input("Diameter Batang (mm)", 0.0, 10.0, 4.5, step=0.1)
    
    st.markdown("---")
    st.markdown("### 🌡️ Parameter Lingkungan")
    
    in_temp = st.number_input("Suhu Rata-rata (°C)", 10.0, 40.0, default_temp, step=0.1)
    in_humidity = st.number_input("Kelembaban (%)", 0, 100, default_humid, step=1)
    
    if st.button("💾 Simpan Data", type="primary", use_container_width=True):
        new_record = {
            "house": input_house,
            "date": input_date.strftime("%Y-%m-%d"),
            "week": input_week,
            "height": in_height,
            "leaves": in_leaves,
            "diameter": in_diameter,
            "temp": in_temp,
            "humidity": in_humidity
        }
        st.session_state.growth_data.append(new_record)
        st.success("Data berhasil disimpan!")

# ==================== MAIN CONTENT ====================

# Layout
col_main, col_ai = st.columns([2, 1])

# --- STANDARD GROWTH DATA (IDEAL) ---
# Standard growth curve for Chrysanthemum
standards = {
    1: {'h': 5, 'l': 4}, 2: {'h': 10, 'l': 6}, 3: {'h': 18, 'l': 9}, 
    4: {'h': 28, 'l': 12}, 5: {'h': 40, 'l': 16}, 6: {'h': 55, 'l': 20},
    7: {'h': 70, 'l': 24}, 8: {'h': 85, 'l': 28}, 9: {'h': 95, 'l': 30},
    10: {'h': 100, 'l': 32}, 11: {'h': 105, 'l': 34}, 12: {'h': 105, 'l': 34}
}

with col_main:
    st.subheader(f"📊 Grafik Pertumbuhan {input_house}")
    
    # Weather Widget
    if 'weather_cache' in st.session_state:
        w = st.session_state.weather_cache
        st.markdown(f"""
        <div class="weather-widget">
            <div style="font-weight:bold; font-size:1.1rem; margin-bottom:5px;">🌤️ Cuaca Real-time (Open-Meteo)</div>
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <span style="font-size:2rem; font-weight:bold;">{w.get('temperature_2m')}°C</span><br>
                    <span>Kelembaban: {w.get('relative_humidity_2m')}%</span>
                </div>
                <div style="text-align:right;">
                    <span>Hujan: {w.get('rain')} mm</span><br>
                    <span>Angin: {w.get('wind_speed_10m')} km/h</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Filter data for selected house
    house_data = [d for d in st.session_state.growth_data if d['house'] == input_house]
    
    if house_data:
        df_house = pd.DataFrame(house_data).sort_values('week')
        
        # Prepare comparison data
        weeks = list(range(1, 13))
        ideal_heights = [standards.get(w, {'h': 0})['h'] for w in weeks]
        ideal_leaves = [standards.get(w, {'l': 0})['l'] for w in weeks]
        
        # Chart 1: Growth Chart (Actual vs Ideal)
        fig_growth = go.Figure()
        
        # Ideal Line
        fig_growth.add_trace(go.Scatter(
            x=weeks, y=ideal_heights, 
            mode='lines', name='Standar Ideal',
            line=dict(color='#94a3b8', width=2, dash='dash')
        ))
        
        # Actual Line
        fig_growth.add_trace(go.Scatter(
            x=df_house['week'], y=df_house['height'], 
            mode='lines+markers', name='Aktual',
            line=dict(color='#10b981', width=4),
            marker=dict(size=8)
        ))
        
        fig_growth.update_layout(
            title="Tinggi Tanaman (cm)",
            xaxis_title="Minggu ke-",
            yaxis_title="Tinggi (cm)",
            height=350,
            legend=dict(orientation="h", y=1.1)
        )
        
        st.plotly_chart(fig_growth, use_container_width=True)
        
        # Chart 2: Leaves & Physics
        c1, c2 = st.columns(2)
        with c1:
            # Create comparison for leaves
            # We need to map actual weeks to ideal weeks
            df_comp = pd.DataFrame({
                'Minggu': weeks,
                'Ideal': ideal_leaves
            })
            # Merge with actual data
            actual_leaves_map = dict(zip(df_house['week'], df_house['leaves']))
            df_comp['Aktual'] = df_comp['Minggu'].map(actual_leaves_map)
            
            fig_leaves = go.Figure()
            fig_leaves.add_trace(go.Bar(
                x=df_comp['Minggu'], y=df_comp['Ideal'],
                name='Ideal', marker_color='#cbd5e1'
            ))
            fig_leaves.add_trace(go.Bar(
                x=df_comp['Minggu'], y=df_comp['Aktual'],
                name='Aktual', marker_color='#22c55e'
            ))
            
            fig_leaves.update_layout(title="Jumlah Daun", height=250, margin=dict(t=30, b=0, l=0, r=0))
            st.plotly_chart(fig_leaves, use_container_width=True)
            
        with c2:
            fig_env = px.line(df_house, x='week', y=['temp', 'humidity'], title='Kondisi Lingkungan')
            fig_env.update_layout(height=250, margin=dict(t=30, b=0, l=0, r=0))
            st.plotly_chart(fig_env, use_container_width=True)

    else:
        st.warning(f"Belum ada data pemantauan untuk {input_house}. Silakan input data di sidebar.")
        
        # Show dummy example chart
        st.markdown("#### Contoh Grafik Ideal")
        weeks = list(range(1, 13))
        ideal_heights = [standards.get(w, {'h': 0})['h'] for w in weeks]
        
        fig_dummy = go.Figure()
        fig_dummy.add_trace(go.Scatter(
            x=weeks, y=ideal_heights, 
            mode='lines', name='Standar Ideal',
            line=dict(color='#94a3b8', width=2, dash='dash')
        ))
        st.plotly_chart(fig_dummy, use_container_width=True)

# ==================== AI ANALYSIS ====================
with col_ai:
    st.markdown("### 🧠 AI Analysis")
    st.markdown("Analisis pertumbuhan & rekomendasi tindakan.")
    
    # Logic AI Simulation
    def analyze_plant_health(week, height, leaves, diameter):
        std = standards.get(week, {'h': 100, 'l': 30})
        
        # Check height
        height_diff = (height - std['h']) / std['h'] * 100
        
        if height_diff < -15:
            status = "Stunted (Kerdil)"
            color = "status-badge-danger"
            advice = [
                "⚠️ **Kurang Nitrogen/Air:** Cek kelembaban tanah dan EC media.",
                "💡 **Kurang Cahaya:** Tambah durasi penyinaran malam hari.",
                "💊 **Rekomendasi:** Aplikasi pupuk daun High N (32-10-10) segera."
            ]
        elif height_diff > 15:
            status = "Etiolasi (Terlalu Tinggi)"
            color = "status-badge-warning"
            advice = [
                "⚠️ **Kelebihan N/Kurang Cahaya:** Batang terlalu panjang dan lemah.",
                "💡 **Jarak Tanam:** Pastikan tidak terlalu rapat.",
                "💊 **Rekomendasi:** Berikan MKP/Kalium, kurangi Urea."
            ]
        else:
            status = "Normal (Sehat)"
            color = "status-badge-ok"
            advice = [
                "✅ Pertumbuhan sesuai target.",
                "💧 Lanjutkan jadwal fertigasi standar.",
                "🔍 Monitor hama thrips/aphids rutin."
            ]
            
        return status, color, advice

    # Display Analysis
    if st.session_state.growth_data:
        # Get latest data for selected house
        latest = [d for d in st.session_state.growth_data if d['house'] == input_house]
        if latest:
            last_record = sorted(latest, key=lambda x: x['week'])[-1]
            
            w_curr = last_record['week']
            h_curr = last_record['height']
            l_curr = last_record['leaves']
            d_curr = last_record['diameter']
            temp_curr = last_record.get('temp', 24)
            humid_curr = last_record.get('humidity', 75)
            
            # Run "AI"
            status, color_css, ai_advice = analyze_plant_health(w_curr, h_curr, l_curr, d_curr)
            
            st.markdown(f"""
            <div class="growth-card">
                <div class="metric-label">Status {input_house} (Minggu {w_curr})</div>
                <div class="{color_css}" style="display:inline-block; margin: 0.5rem 0;">{status}</div>
                <div style="font-size: 2.5rem; margin: 0.5rem 0;">{h_curr} cm</div>
                <div class="metric-label">Target: {standards.get(w_curr, {}).get('h', '-')} cm</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("#### 🤖 Rekomendasi AI:")
            for tip in ai_advice:
                st.markdown(f"- {tip}")
            
            st.markdown("---")
            st.markdown("#### 🌡️ Analisis Lingkungan")
            
            # Agro-climate analysis
            env_status = []
            
            # Temp Analysis
            if temp_curr > 28:
                env_status.append(f"⚠️ **Suhu Panas ({temp_curr}°C):** Risiko bunga kecil/pudar. Nyalakan misting siang hari.")
            elif temp_curr < 15:
                env_status.append(f"❄️ **Suhu Dingin ({temp_curr}°C):** Pertumbuhan melambat. Tutup screen malam hari.")
            else:
                env_status.append(f"✅ **Suhu Ideal ({temp_curr}°C)**")
                
            # Humidity Analysis
            if humid_curr > 90:
                env_status.append(f"💦 **Lembab ({humid_curr}%):** Risiko jamur karat putih! Tingkatkan sirkulasi udara.")
            elif humid_curr < 60:
                env_status.append(f"🌵 **Kering ({humid_curr}%):** Risiko layu. Lakukan penyiraman lantai.")
            else:
                env_status.append(f"✅ **Kelembaban Ideal ({humid_curr}%)**")
            
            for status in env_status:
                st.markdown(f"{status}")

            st.markdown("---")
            st.markdown(f"**Diameter Batang:** {d_curr} mm")
            if d_curr < 3.0 and w_curr > 4:
                st.warning("⚠️ Batang terlalu kecil! Risiko patah saat berbunga.")
            else:
                st.success("✅ Diameter batang kokoh.")
                
        else:
            st.info("Pilih house lain atau input data.")
    else:
        st.info("Input data mingguan pertama Anda untuk melihat analisis AI.")

# Footer
st.markdown("---")
st.caption("🌸 Budidaya Krisan Pro - Pantau Pertumbuhan & AI")

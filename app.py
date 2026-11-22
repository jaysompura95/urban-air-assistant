"""
Urban Air Quality Assistant - Enhanced Edition
GenAI Winter Smog Defense, Indoor Air Quality Hacks & Community Action Network
"""

import streamlit as st
import pandas as pd
import altair as alt
import pydeck as pdk
import datetime
from typing import Dict, Any

from api_service import (
    PRESET_CITIES, geocode_city, get_air_quality, get_aqi_category
)
from impact_calculator import (
    calculate_personal_exposure, calculate_cadr_and_ach, calculate_community_multiplier
)
from iaq_hacks import get_all_hacks, get_hack_by_id
from routines_generator import generate_personalized_routine
from community_hub import get_community_initiatives, calculate_carpool_savings
from genai_engine import ask_genai, PERSONAS

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Urban Air Quality Assistant | Winter Smog & Community Shield",
    page_icon="🌬️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Ultra-Modern Dark Glassmorphism Styling
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Background & Global Palette */
    .stApp {
        background: radial-gradient(circle at 10% 20%, #0d131f 0%, #080c14 90%);
        color: #f1f5f9;
    }
    
    /* Hero Banner */
    .hero-banner {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.9) 100%);
        border: 1px solid rgba(59, 130, 246, 0.3);
        border-radius: 16px;
        padding: 24px 28px;
        margin-bottom: 20px;
        backdrop-filter: blur(16px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
    }
    
    /* Live Pulse Dot */
    .live-pulse {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background-color: #ef4444;
        box-shadow: 0 0 10px #ef4444;
        animation: pulse 1.8s infinite;
        margin-right: 8px;
    }
    @keyframes pulse {
        0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7); }
        70% { transform: scale(1.15); box-shadow: 0 0 0 8px rgba(239, 68, 68, 0); }
        100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
    }
    
    /* Glassmorphism Metric Card */
    .glass-card {
        background: rgba(30, 41, 59, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 16px 20px;
        backdrop-filter: blur(12px);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .glass-card:hover {
        transform: translateY(-2px);
        border-color: rgba(59, 130, 246, 0.4);
    }
    
    /* Badges */
    .badge-pill {
        display: inline-block;
        padding: 6px 14px;
        border-radius: 30px;
        font-weight: 700;
        font-size: 0.85rem;
        letter-spacing: 0.5px;
    }
    
    /* Timeline item */
    .timeline-node {
        border-left: 3px solid #3b82f6;
        padding-left: 20px;
        margin-bottom: 24px;
        position: relative;
    }
    .timeline-node::before {
        content: "";
        position: absolute;
        left: -9px;
        top: 2px;
        width: 15px;
        height: 15px;
        border-radius: 50%;
        background-color: #3b82f6;
        box-shadow: 0 0 8px #3b82f6;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Sidebar Configuration
# ---------------------------------------------------------
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1534088568595-a066f410bcda?w=400&auto=format&fit=crop&q=80", use_container_width=True)
    st.markdown("## 🌬️ **Urban Air Assistant**")
    st.caption("GenAI Winter Smog Defense & Community Shield")
    
    st.markdown("---")
    st.subheader("📍 Location Settings")
    
    loc_mode = st.radio("Choose Location:", ["Global Smog Hotspots", "Search Any City"], index=0)
    
    if loc_mode == "Global Smog Hotspots":
        selected_city_name = st.selectbox("Select City Hotspot:", list(PRESET_CITIES.keys()), index=0)
        lat = PRESET_CITIES[selected_city_name]["lat"]
        lon = PRESET_CITIES[selected_city_name]["lon"]
        st.info(PRESET_CITIES[selected_city_name]["desc"])
    else:
        query_text = st.text_input("Enter City / Neighborhood:", "Salt Lake City")
        results = geocode_city(query_text) if query_text else []
        if results:
            city_options = {r["display"]: r for r in results}
            chosen_display = st.selectbox("Matching Cities:", list(city_options.keys()))
            chosen_obj = city_options[chosen_display]
            selected_city_name = chosen_obj["display"]
            lat, lon = chosen_obj["lat"], chosen_obj["lon"]
        else:
            selected_city_name = "New Delhi, India"
            lat, lon = PRESET_CITIES["New Delhi, India"]["lat"], PRESET_CITIES["New Delhi, India"]["lon"]
            st.caption("Type any city name worldwide to search.")

    st.markdown(f"**Coordinates:** `{lat:.4f}, {lon:.4f}`")
    
    st.markdown("---")
    st.subheader("👨‍👩‍👧‍👦 Household Profile")
    lifestyle_choice = st.selectbox(
        "Family Profile:",
        [
            "Family with Young Children",
            "Vulnerable (Asthma / Seniors / COPD)",
            "Urban Working Commuter",
            "Remote Worker / Freelancer",
            "Community / Neighborhood Champion"
        ],
        index=0
    )
    
    commute_mode = st.selectbox(
        "Primary Commute Mode:",
        [
            "Public Metro / Electric Bus",
            "Carpool / Rideshare (3-4 persons)",
            "Solo Gasoline / Diesel Car",
            "Bicycle / E-Bike with N95",
            "Remote Work / Zero Commute"
        ],
        index=0
    )
    
    roundtrip_km = st.slider("Daily Commute Distance (km):", min_value=2, max_value=60, value=18, step=2)
    
    heating_choice = st.selectbox(
        "Heating & Cooking Setup:",
        [
            "Electric Heat Pump / Induction Stove",
            "Gas Stove / Piped Gas Heating",
            "Electric Ceramic Space Heater",
            "Wood Fireplace / Biomass Chulha"
        ],
        index=0
    )
    
    st.markdown("---")
    st.subheader("🤖 GenAI Configuration")
    persona_choice = st.selectbox("AI Advisor Persona:", list(PERSONAS.keys()), index=0)
    api_key_input = st.text_input("Google Gemini API Key (Optional):", type="password", help="Leave blank to use the built-in domain reasoning engine.")
    if api_key_input:
        st.success("Custom Gemini API Key active!")
    else:
        st.caption("⚡ Built-in Expert Reasoning Engine active (100% functional offline).")

# ---------------------------------------------------------
# Real-Time Data Fetching
# ---------------------------------------------------------
@st.cache_data(ttl=300)
def fetch_air_data(latitude: float, longitude: float):
    return get_air_quality(latitude, longitude)

data = fetch_air_data(lat, lon)
if not data or not data.get("current_aq"):
    st.error("Atmospheric telemetry temporarily unavailable. Please retry or pick another city.")
    st.stop()

current_aq = data["current_aq"]
current_w = data.get("current_weather", {})
hourly_aq = data.get("hourly_aq", {})
inversion_info = data.get("inversion_risk", {})
best_window_info = data.get("optimal_outdoor_window", {})

pm25 = current_aq.get("pm2_5", 50.0)
pm10 = current_aq.get("pm10", 80.0)
us_aqi = int(current_aq.get("us_aqi") or 100)
category = get_aqi_category(us_aqi)

# ---------------------------------------------------------
# Hero Banner & Dynamic Status Header
# ---------------------------------------------------------
st.markdown(f"""
<div class="hero-banner">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
        <div>
            <div style="font-size: 0.82rem; text-transform: uppercase; letter-spacing: 1.5px; color: #60a5fa; font-weight: 700; margin-bottom: 4px;">
                <span class="live-pulse"></span>LIVE ATMOSPHERIC TELEMETRY &bull; OPEN-METEO SYNC
            </div>
            <h1 style="margin: 0; font-size: 2.3rem; font-weight: 800; color: #ffffff;">
                🌬️ Urban Air Quality Assistant
            </h1>
            <p style="margin: 6px 0 0 0; color: #94a3b8; font-size: 1.05rem;">
                GenAI Winter Smog Defense, Indoor Air Quality Hacks & Community Action Network
            </p>
        </div>
        <div style="text-align: right; margin-top: 10px;">
            <span class="badge-pill" style="background-color: {category['bg']}; color: {category['color']}; font-size: 1.15rem;">
                {category['badge']} &bull; AQI {us_aqi}
            </span>
            <div style="color: #cbd5e1; font-size: 0.88rem; margin-top: 8px;">
                📍 <strong>{selected_city_name}</strong> &bull; Telemetry: {current_aq.get('time', 'Just now')}
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Thermal Inversion Alert Banner
st.markdown(f"""
<div style="background-color: {inversion_info['color']}18; border-left: 6px solid {inversion_info['color']}; border-radius: 10px; padding: 14px 20px; margin-bottom: 22px; backdrop-filter: blur(8px);">
    <strong style="color: {inversion_info['color']}; font-size: 1.05rem;">⚠️ {inversion_info['level']} (Inversion Index: {inversion_info['score']}/100)</strong>
    <p style="margin: 4px 0 0 0; color: #e2e8f0; font-size: 0.95rem;">
        {inversion_info['advice']}
    </p>
    <div style="margin-top: 6px; font-size: 0.85rem; color: #94a3b8;">
        🔬 <strong>Atmospheric Drivers:</strong> {', '.join(inversion_info['factors']) if inversion_info['factors'] else 'Active atmospheric boundary layer dispersion.'}
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Application Tabs
# ---------------------------------------------------------
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🌐 Live Smog & Radar",
    "📅 24h Shield Routine",
    "🛠️ IAQ Hacks & DIY Lab",
    "📊 Direct Impact Ledger",
    "🤝 Community Hub",
    "💬 Aura GenAI Assistant"
])

# =========================================================
# TAB 1: Live Smog & Geospatial Radar
# =========================================================
with tab1:
    st.subheader(f"📊 Real-Time Atmospheric Diagnostics ({selected_city_name})")
    
    k1, k2, k3, k4, k5 = st.columns(5)
    with k1:
        st.metric("Air Quality Index", f"{us_aqi} US AQI", delta=category["label"], delta_color="inverse" if us_aqi > 100 else "normal")
    with k2:
        st.metric("PM2.5 (Fine Soot)", f"{pm25:.1f} µg/m³", delta=f"{(pm25 / 15.0):.1f}x WHO Limit", delta_color="inverse" if pm25 > 15 else "normal")
    with k3:
        st.metric("PM10 (Coarse Dust)", f"{pm10:.1f} µg/m³", delta="Inhalable Aerosols")
    with k4:
        temp = current_w.get("temperature_2m", 15)
        st.metric("Temperature", f"{temp:.1f} °C", delta="Trapping smog" if temp < 14 else "Convective", delta_color="inverse" if temp < 14 else "normal")
    with k5:
        wind = current_w.get("wind_speed_10m", 5)
        st.metric("Wind Speed", f"{wind:.1f} km/h", delta="Stagnant Air" if wind < 6 else "Active Mix", delta_color="normal" if wind >= 8 else "inverse")

    st.markdown("---")
    
    col_chart, col_side = st.columns([2, 1])
    
    with col_chart:
        st.markdown("#### 📈 48-Hour Forecast & Particulate Curve")
        times = hourly_aq.get("time", [])
        pm25_vals = hourly_aq.get("pm2_5", [])
        aqi_vals = hourly_aq.get("us_aqi", [])
        
        if times and pm25_vals:
            df_chart = pd.DataFrame({
                "Timestamp": [t.replace("T", " ") for t in times[:48]],
                "PM2.5 (µg/m³)": pm25_vals[:48],
                "US AQI": aqi_vals[:48] if aqi_vals else [0]*48
            })
            
            line_chart = alt.Chart(df_chart).mark_area(
                line={'color': '#ef4444', 'strokeWidth': 2},
                color=alt.Gradient(
                    gradient='linear',
                    stops=[
                        alt.GradientStop(color='rgba(239, 68, 68, 0.55)', offset=0),
                        alt.GradientStop(color='rgba(239, 68, 68, 0.05)', offset=1)
                    ],
                    x1=1, x2=1, y1=1, y2=0
                )
            ).encode(
                x=alt.X('Timestamp:N', title='Time', axis=alt.Axis(labelAngle=-45, values=df_chart['Timestamp'].iloc[::4])),
                y=alt.Y('PM2.5 (µg/m³):Q', title='PM2.5 Concentration (µg/m³)'),
                tooltip=['Timestamp', 'PM2.5 (µg/m³)', 'US AQI']
            ).properties(height=320)
            
            who_line = alt.Chart(pd.DataFrame({'y': [15]})).mark_rule(color='#10b981', strokeDash=[4, 4]).encode(y='y:Q')
            st.altair_chart(line_chart + who_line, use_container_width=True)
            st.caption("🟢 Green dashed line = WHO Safe 24-Hour PM2.5 Guideline (15 µg/m³).")
    
    with col_side:
        st.markdown("#### ☀️ Safest Outdoor Air Slot")
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #064e3b 0%, #022c22 100%); border: 1px solid #10b981; border-radius: 14px; padding: 20px; color: #ecfdf5;">
            <div style="font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1.2px; color: #6ee7b7; font-weight: 700;">
                OPTIMAL FRESH AIR SLOT
            </div>
            <div style="font-size: 1.9rem; font-weight: 800; margin: 8px 0; color: #ffffff;">
                ⏰ {best_window_info.get('window_str', '1:00 PM - 3:30 PM')}
            </div>
            <p style="font-size: 0.92rem; margin: 0 0 12px 0; color: #d1fae5;">
                {best_window_info.get('tip', 'Solar heating lifts the inversion layer.')}
            </p>
            <div style="background: rgba(0, 0, 0, 0.25); border-radius: 8px; padding: 10px 14px; font-size: 0.85rem; color: #a7f3d0;">
                ✔ 12-min cross-draft CO2 purge<br/>
                ✔ Child outdoor recess slot<br/>
                ✔ Essential grocery errands
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### 🌍 Global Winter Smog Hotspots 3D Radar")
    st.caption("Interactive geospatial map comparing real-time winter pollution basins worldwide.")
    
    # 3D Pydeck Globe Map
    map_data = []
    for city_key, meta in PRESET_CITIES.items():
        # High smog cities get red/purple; lower get yellow/green
        if "Delhi" in city_key or "Lahore" in city_key:
            col = [239, 68, 68, 220]
            radius = 120000
        elif "Beijing" in city_key or "Kraków" in city_key or "Salt Lake" in city_key:
            col = [249, 115, 22, 220]
            radius = 90000
        else:
            col = [234, 179, 8, 220]
            radius = 70000
        map_data.append({
            "name": city_key,
            "lat": meta["lat"],
            "lon": meta["lon"],
            "desc": meta["desc"],
            "color": col,
            "radius": radius
        })
    
    df_map = pd.DataFrame(map_data)
    
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=df_map,
        get_position=["lon", "lat"],
        get_color="color",
        get_radius="radius",
        pickable=True,
        auto_highlight=True
    )
    
    view_state = pdk.ViewState(
        latitude=lat,
        longitude=lon,
        zoom=2.2,
        pitch=30
    )
    
    deck = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={"text": "{name}\n{desc}"},
        map_style="mapbox://styles/mapbox/dark-v10"
    )
    st.pydeck_chart(deck)

# =========================================================
# TAB 2: Personalized 24h Shield Routine
# =========================================================
with tab2:
    st.subheader(f"📅 24-Hour Smog Shield Routine: {lifestyle_choice}")
    st.caption(f"Optimized for {selected_city_name} &bull; Commute: {commute_mode} &bull; Heating: {heating_choice}")
    
    routine = generate_personalized_routine(
        city_name=selected_city_name,
        aqi=us_aqi,
        pm25=pm25,
        inversion_level=inversion_info["level"],
        optimal_window_str=best_window_info.get("window_str", "1:00 PM - 3:30 PM"),
        lifestyle=lifestyle_choice,
        commute_mode=commute_mode,
        heating_type=heating_choice
    )
    
    col_tl, col_chk = st.columns([2, 1])
    
    with col_tl:
        st.markdown("#### 🕒 Dynamic Timeline & Actions")
        for item in routine["timeline"]:
            st.markdown(f"""
            <div class="timeline-node" style="border-left-color: {item['color']};">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <strong style="color: {item['color']}; font-size: 1.15rem;">{item['time']} &mdash; {item['title']}</strong>
                    <span class="badge-pill" style="background-color: {item['color']}25; color: {item['color']}; font-size: 0.8rem;">{item['tag']}</span>
                </div>
                <div style="margin-top: 10px;">
                    <strong style="color: #60a5fa; font-size: 0.92rem;">🛡️ Health Shield:</strong>
                    <ul style="margin: 4px 0 8px 18px; color: #cbd5e1; font-size: 0.92rem;">
                        {''.join([f"<li>{act}</li>" for act in item['shield_actions']])}
                    </ul>
                    <strong style="color: #34d399; font-size: 0.92rem;">🌱 Low-Emission Habit:</strong>
                    <ul style="margin: 4px 0 8px 18px; color: #cbd5e1; font-size: 0.92rem;">
                        {''.join([f"<li>{act}</li>" for act in item['green_actions']])}
                    </ul>
                    <div style="background-color: rgba(255, 255, 255, 0.05); border-left: 3px solid #38bdf8; padding: 6px 14px; border-radius: 4px; font-size: 0.85rem; color: #e2e8f0;">
                        💡 <strong>Direct Impact:</strong> {item['impact_benefit']}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with col_chk:
        st.markdown("#### 🎙️ Morning 60-Second Audio Script")
        st.markdown(f"""
        <div style="background: #1e293b; border: 1px solid #475569; border-radius: 12px; padding: 16px; margin-bottom: 20px;">
            <div style="color: #38bdf8; font-weight: 700; font-size: 0.95rem; margin-bottom: 6px;">
                📻 Parent & Commuter Radio Briefing:
            </div>
            <p style="font-style: italic; font-size: 0.88rem; color: #cbd5e1; margin: 0;">
                "Good morning! Today in {selected_city_name}, AQI is at {us_aqi} ({category['label']}). 
                Thermal inversion is compressing soot right now, so keep windows sealed until {best_window_info.get('window_str', '1:00 PM')}. 
                Ensure N95 masks for children on their way to school, set car air to internal recirculation, and run your bedroom DIY air purifiers. 
                Stay safe and breathe clean!"
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("#### ✅ Today's Smog Shield Checklist")
        completed_count = 0
        for chk in routine["quick_checklist"]:
            if st.checkbox(chk, value=False):
                completed_count += 1
        
        st.progress(completed_count / len(routine["quick_checklist"]), text=f"Shield Readiness: {completed_count}/{len(routine['quick_checklist'])} Completed")
            
        st.markdown("---")
        st.markdown("#### 📥 Family Action Card")
        action_card_md = f"""# 🌬️ Family Smog Shield Action Card
**Date:** {datetime.date.today().strftime('%B %d, %Y')} | **Location:** {selected_city_name}
**Air Quality:** AQI {us_aqi} ({category['label']}) | **PM2.5:** {pm25:.1f} µg/m³
**Household Archetype:** {lifestyle_choice}

### 🔒 Three Golden Rules for Today:
1. **Windows CLOSED** before 12:30 PM and after 3:30 PM.
2. **Fresh Air Window:** {best_window_info.get('window_str', '1:00 PM - 3:30 PM')} (15-min flush only).
3. **N95 Masks** on for all family members stepping outside.
4. **Kitchen:** Cook on rear burners with exhaust on high.
5. **Bedrooms:** DIY Corsi-Rosenthal / HEPA purifiers running continuously.
"""
        st.download_button(
            label="📄 Download Action Card (Markdown)",
            data=action_card_md,
            file_name=f"smog_action_card_{datetime.date.today().strftime('%Y%m%d')}.md",
            mime="text/markdown"
        )

# =========================================================
# TAB 3: Indoor Air Quality (IAQ) Hacks & DIY Lab
# =========================================================
with tab3:
    st.subheader("🛠️ Indoor Air Quality (IAQ) Engineering Lab")
    st.caption("Open-source fluid dynamics hacks that purify indoor air faster and cheaper than commercial HEPA units.")
    
    st.markdown("### 🌀 Interactive DIY Corsi-Rosenthal Box Designer")
    
    cr_col1, cr_col2 = st.columns([1, 1])
    with cr_col1:
        room_sqft = st.number_input("Room Floor Area (sq ft):", min_value=100, max_value=1200, value=300, step=50)
        ceiling_h = st.number_input("Ceiling Height (feet):", min_value=7.0, max_value=15.0, value=9.0, step=0.5)
        fan_speed_sel = st.selectbox("Box Fan Speed Setting:", ["Medium (Balanced)", "High (Maximum Smog Purge)", "Low (Ultra-Quiet)"], index=0)
        filter_count = st.slider("Filter Count (Wedge vs Cube):", min_value=2, max_value=5, value=4)
        merv_val = st.radio("Filter Grade:", [13, 11], index=0, format_func=lambda x: f"MERV {x} ({'Captures 85-90% PM2.5' if x==13 else 'Captures ~65% PM2.5'})")
    
    cadr_res = calculate_cadr_and_ach(room_sqft, ceiling_h, filter_count, fan_speed_sel, merv_val)
    
    # Filter life calculation based on local PM2.5
    filter_life_days = max(30, int(180 - (pm25 * 0.4)))
    
    with cr_col2:
        st.markdown(f"""
        <div style="background: #1e293b; border: 1px solid #475569; border-radius: 14px; padding: 22px;">
            <div style="font-size: 0.85rem; text-transform: uppercase; color: #94a3b8; font-weight: 700; letter-spacing: 1px;">
                CALCULATED CLEAN AIR DELIVERY RATE
            </div>
            <div style="font-size: 2.3rem; font-weight: 800; color: #38bdf8; margin: 4px 0;">
                {cadr_res['effective_cadr_cfm']} CFM
            </div>
            <div style="font-size: 1.1rem; color: #f1f5f9; margin-bottom: 12px;">
                Air Changes per Hour (ACH): <strong style="color: {cadr_res['ach_color']};">{cadr_res['ach']} ACH</strong>
            </div>
            <div style="background-color: {cadr_res['ach_color']}22; border-left: 4px solid {cadr_res['ach_color']}; padding: 8px 14px; border-radius: 4px; margin-bottom: 14px;">
                <span style="color: {cadr_res['ach_color']}; font-weight: 700;">{cadr_res['ach_rating']}</span>
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; font-size: 0.92rem; color: #cbd5e1;">
                <div>⏱️ 90% Clearance: <strong>{cadr_res['t_90_mins']} mins</strong></div>
                <div>⚡ 99% Clearance: <strong>{cadr_res['t_99_mins']} mins</strong></div>
                <div>💰 Build Cost: <strong>${cadr_res['diy_cost_usd']}</strong></div>
                <div>🏷️ Commercial HEPA: <strong>${cadr_res['commercial_cost_usd']}</strong></div>
                <div>📅 Est. Filter Life: <strong>~{filter_life_days} days</strong> (in {selected_city_name} smog)</div>
                <div>💵 Total Savings: <strong style="color: #34d399;">${cadr_res['savings_usd']}</strong></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 📐 Visual Schematic: The Cardboard Shroud Advantage")
    st.markdown("""
    ```
          ┌───────────────────────────────────┐
          │     15" Circular Cardboard Shroud │  <-- Eliminates corner backpressure eddy vortexes
          │            ┌─────────────┐        │      BOOSTS CLEAN AIRFLOW BY +40%!
          │            │  (O) FAN (O)│        │
          │            └─────────────┘        │
    ┌─────┴───────────────────────────────────┴─────┐
    │  MERV 13 Filter  │   MERV 13 Filter   │ Filter│  <-- Air sucked inwards through 4 sides
    │ (Arrows point IN)│ (Arrows point IN)  │       │      40+ sq ft of surface media
    └───────────────────────────────────────────────┘
    ```
    """)
    
    st.markdown("---")
    st.markdown("### 📚 6 Scientifically Proven IAQ Hacks")
    hacks = get_all_hacks()
    for hack in hacks:
        with st.expander(f"{hack['title']} — [{hack['category']}] (Efficacy: {hack['efficacy']})", expanded=(hack['id'] == 'corsi_rosenthal')):
            h_c1, h_c2 = st.columns([2, 1])
            with h_c1:
                st.markdown(f"**Summary:** {hack['summary']}")
                st.markdown(f"**🔬 The Science:** {hack['why_it_works']}")
                st.markdown("**🛠️ Step-by-Step Instructions:**")
                for s in hack["step_by_step"]:
                    st.markdown(f"- {s}")
            with h_c2:
                st.markdown(f"""
                <div style="background: #0f172a; border: 1px solid #334155; border-radius: 10px; padding: 16px;">
                    <div style="color: #38bdf8; font-weight: 700; margin-bottom: 8px;">📋 Specs:</div>
                    <div style="font-size: 0.88rem; color: #cbd5e1; margin-bottom: 4px;">• <strong>Cost:</strong> {hack['cost']}</div>
                    <div style="font-size: 0.88rem; color: #cbd5e1; margin-bottom: 4px;">• <strong>Difficulty:</strong> {hack['difficulty']}</div>
                    <div style="font-size: 0.88rem; color: #cbd5e1; margin-bottom: 8px;">• <strong>Efficacy:</strong> {hack['efficacy']}</div>
                    <hr style="border-color: #334155; margin: 10px 0;">
                    <div style="font-size: 0.84rem; color: #94a3b8;"><strong>💡 Pro Tip:</strong> {hack['scientific_tip']}</div>
                </div>
                """, unsafe_allow_html=True)

# =========================================================
# TAB 4: Direct Impact Ledger & What-If Simulator
# =========================================================
with tab4:
    st.subheader("📊 Direct Impact Ledger: Quantifying Your Choices")
    st.caption("Peer-reviewed mathematical modeling of lung particulate reduction, cigarette equivalents, and carbon savings.")
    
    # Personal Exposure
    exposure = calculate_personal_exposure(
        outdoor_pm25=pm25,
        has_iaq_filter=True,
        wears_n95_commute=True,
        follows_window_protocol=True,
        profile_type=lifestyle_choice,
        commute_mode=commute_mode,
        roundtrip_km=roundtrip_km
    )
    
    st.markdown("#### 👤 Your Household's Daily Shield Impact")
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric(
            label="Avoided Inhaled PM2.5",
            value=f"{exposure['avoided_inhaled_mg']:.2f} mg",
            delta=f"-{exposure['reduction_pct']:.0f}% Exposure",
            delta_color="normal"
        )
    with m2:
        st.metric(
            label="Passive Cigarettes Avoided",
            value=f"{exposure['avoided_cigs']:.1f} cigs/day",
            delta=f"From {exposure['baseline_cigs']:.1f} down to {exposure['mitigated_cigs']:.1f}",
            delta_color="normal"
        )
    with m3:
        st.metric(
            label="Commute CO2 Saved",
            value=f"{exposure['saved_co2_kg']:.2f} kg",
            delta="Daily Reduction"
        )
    with m4:
        st.metric(
            label="Tailpipe Particulates Prevented",
            value=f"{exposure['saved_tailpipe_pm_g']:.2f} g",
            delta="Street-level PM"
        )

    st.markdown("---")
    
    st.markdown("#### 🧪 Interactive \"What-If\" Smog Severity Simulator")
    st.caption("Drag the slider to simulate what happens to your family's lungs and choices during severe smog spikes.")
    
    sim_pm25 = st.slider("Simulate Outdoor PM2.5 (µg/m³):", min_value=20, max_value=600, value=int(pm25), step=10)
    sim_exposure = calculate_personal_exposure(
        outdoor_pm25=float(sim_pm25),
        has_iaq_filter=True,
        wears_n95_commute=True,
        follows_window_protocol=True,
        profile_type=lifestyle_choice,
        commute_mode=commute_mode,
        roundtrip_km=roundtrip_km
    )
    
    sc1, sc2, sc3 = st.columns(3)
    with sc1:
        st.metric("Simulated Baseline Exposure (No Shield)", f"{sim_exposure['baseline_cigs']:.1f} Cigarettes/day", delta="High Danger", delta_color="inverse")
    with sc2:
        st.metric("Exposure with Aura Shield", f"{sim_exposure['mitigated_cigs']:.1f} Cigarettes/day", delta=f"-{sim_exposure['reduction_pct']:.0f}%", delta_color="normal")
    with sc3:
        st.metric("Toxic PM2.5 Prevented from Lungs", f"{sim_exposure['avoided_inhaled_mg']:.2f} mg / day", delta="Protected")

    st.markdown("---")
    st.markdown("#### 🏘️ Community Collective Impact Multiplier")
    community_size = st.slider("Neighborhood Size (Households participating):", min_value=20, max_value=2000, value=250, step=10)
    comm_res = calculate_community_multiplier(
        exposure['saved_co2_kg'],
        exposure['avoided_inhaled_ug'] / 1000.0,
        community_size
    )
    
    cm1, cm2, cm3, cm4 = st.columns(4)
    with cm1:
        st.metric("Total CO2 Prevented / Month", f"{comm_res['total_co2_tonnes_month']:.1f} Tonnes")
    with cm2:
        st.metric("Total PM2.5 Prevented / Month", f"{comm_res['total_pm25_kg_month']:.1f} kg")
    with cm3:
        st.metric("Prevented Pediatric Asthma ER Visits", f"~{comm_res['prevented_er_visits_season']:.0f} visits/season")
    with cm4:
        st.metric("Equivalent Trees Planted", f"{comm_res['trees_equivalent']} Trees")

# =========================================================
# TAB 5: Community Hub & Anti-Burning Initiatives
# =========================================================
with tab5:
    st.subheader("🤝 Community Winter Smog Action Hub")
    st.caption("Neighborhood initiatives to eradicate open biomass burning, school transit smog, and vulnerable equity.")
    
    initiatives = get_community_initiatives()
    for init in initiatives:
        with st.expander(f"📢 {init['title']} — [{init['badge']}]", expanded=(init['id'] == 'anti_burning')):
            st.markdown(f"**The Problem:** {init['the_problem']}")
            st.markdown("**The Community Solution:**")
            for sol in init["the_solution"]:
                st.markdown(f"- {sol}")
            if "reporting_template" in init:
                st.markdown("**📋 Instant Copy-Paste Society/Municipal Report Template:**")
                st.code(init["reporting_template"], language="markdown")
            if "impact_metric" in init:
                st.success(f"🎯 Verified Community Impact: {init['impact_metric']}")
                
    st.markdown("---")
    st.markdown("### 🚌 School Carpool & Bus Pod Calculator")
    st.caption("Calculate the exact pollution and cost savings of grouping 3-5 neighborhood families into a shared school run.")
    
    cp_c1, cp_c2 = st.columns([1, 1])
    with cp_c1:
        num_fams = st.slider("Number of Families in Carpool Pod:", min_value=2, max_value=6, value=4)
        one_way_km = st.slider("One-Way Distance to School (km):", min_value=2.0, max_value=25.0, value=7.5, step=0.5)
        school_days = st.slider("School Days per Month:", min_value=15, max_value=25, value=22)
    
    carpool_data = calculate_carpool_savings(num_fams, one_way_km, school_days)
    
    with cp_c2:
        st.markdown(f"""
        <div style="background: #1e293b; border: 1px solid #3b82f6; border-radius: 12px; padding: 22px;">
            <div style="color: #60a5fa; font-weight: 700; font-size: 1.1rem; margin-bottom: 8px;">
                🚗 Monthly Carpool Pod Impact ({num_fams} Families)
            </div>
            <div style="font-size: 2rem; font-weight: 800; color: #10b981;">
                -{carpool_data['saved_co2_kg']} kg CO2 / Month
            </div>
            <div style="color: #cbd5e1; margin-top: 8px; font-size: 0.95rem; line-height: 1.6;">
                • Eliminates <strong>{carpool_data['saved_km_month']} km</strong> of cold-engine vehicle idling.<br>
                • Prevents <strong>{carpool_data['saved_pm25_g']} grams</strong> of toxic tailpipe soot at school gates.<br>
                • Saves <strong>${carpool_data['saved_fuel_usd']}</strong> total in monthly fuel costs.<br>
                • <strong style="color: #38bdf8;">${carpool_data['savings_per_family_usd']} saved per family</strong> each month!
            </div>
        </div>
        """, unsafe_allow_html=True)

# =========================================================
# TAB 6: Aura GenAI Air Quality Assistant
# =========================================================
with tab6:
    st.subheader("💬 Aura — Your GenAI Urban Air Quality Advisor")
    st.caption(f"Currently advising as: **{persona_choice}** | Context: {selected_city_name} (AQI: {us_aqi}, PM2.5: {pm25} µg/m³)")
    
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = [
            {
                "role": "assistant",
                "content": f"Hello! I'm Aura, your Urban Air Quality Assistant. I'm actively monitoring the winter smog conditions in **{selected_city_name}** (AQI: **{us_aqi}**, PM2.5: **{pm25} µg/m³**). How can I help your family or community today? You can ask me about DIY air purifiers, child lung protection, ventilation schedules, or low-emission commute shifts."
            }
        ]
    
    st.markdown("**Suggested Quick Questions for Aura:**")
    q_col1, q_col2, q_col3 = st.columns(3)
    with q_col1:
        if st.button("🧒 Plan a zero-smog school routine for children"):
            st.session_state.temp_prompt = "How do I plan a safe zero-smog morning routine for my school-age children in today's conditions?"
    with q_col2:
        if st.button("🛠️ Step-by-step $65 Corsi-Rosenthal build"):
            st.session_state.temp_prompt = "Give me the step-by-step instructions and materials checklist to build a Corsi-Rosenthal clean air box for my 300 sq ft room."
    with q_col3:
        if st.button("🔥 Clean heating alternatives to prevent indoor smoke"):
            st.session_state.temp_prompt = "What are the best low-emission heating and cooking alternatives to avoid indoor particulate spikes this winter?"

    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
    user_query = st.chat_input("Ask Aura anything about smog, IAQ hacks, routines, or emissions...")
    
    if "temp_prompt" in st.session_state and st.session_state.temp_prompt:
        user_query = st.session_state.temp_prompt
        st.session_state.temp_prompt = None

    if user_query:
        st.session_state.chat_messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)
            
        with st.chat_message("assistant"):
            with st.spinner("Aura is analyzing atmospheric data and generating recommendations..."):
                response_text = ask_genai(
                    query=user_query,
                    city_name=selected_city_name,
                    aqi=us_aqi,
                    aqi_label=category["label"],
                    pm25=pm25,
                    pm10=pm10,
                    inversion_status=inversion_info["level"],
                    optimal_window=best_window_info.get("window_str", "1:00 PM - 3:30 PM"),
                    persona_key=persona_choice,
                    api_key=api_key_input,
                    chat_history=st.session_state.chat_messages
                )
                st.markdown(response_text)
                st.session_state.chat_messages.append({"role": "assistant", "content": response_text})

# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 0.88rem; padding: 12px 0;">
    <strong>Urban Air Quality Assistant</strong> &bull; Developed by <strong>Jay Sompura</strong> for the Winter Smog Hackathon<br>
    Powered by Open-Meteo Global Air Quality API & Google GenAI Architecture
</div>
""", unsafe_allow_html=True)

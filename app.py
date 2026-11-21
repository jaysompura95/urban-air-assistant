"""
Urban Air Quality Assistant - Streamlit Application
A GenAI-powered assistant helping families and communities navigate severe winter smog.
"""

import streamlit as st
import pandas as pd
import altair as alt
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
# Custom Modern UI Styling
# ---------------------------------------------------------
st.markdown("""
<style>
    /* Global Font & Theme Tuning */
    .main {
        background-color: #0d1117;
        color: #e6edf3;
    }
    .metric-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7), rgba(15, 23, 42, 0.8));
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        margin-bottom: 12px;
    }
    .hero-container {
        background: linear-gradient(135deg, #1e1e38 0%, #0f172a 100%);
        border: 1px solid #3b82f6;
        border-radius: 14px;
        padding: 24px;
        margin-bottom: 24px;
    }
    .hack-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 10px;
        padding: 18px;
        margin-bottom: 14px;
        transition: transform 0.2s ease;
    }
    .hack-card:hover {
        border-color: #58a6ff;
    }
    .badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.82rem;
    }
    .timeline-item {
        border-left: 3px solid #3b82f6;
        padding-left: 18px;
        margin-bottom: 22px;
        position: relative;
    }
    .timeline-item::before {
        content: "";
        position: absolute;
        left: -8px;
        top: 2px;
        width: 14px;
        height: 14px;
        border-radius: 50%;
        background-color: #3b82f6;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Sidebar Controls & Configuration
# ---------------------------------------------------------
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1534088568595-a066f410bcda?w=400&auto=format&fit=crop&q=80", use_container_width=True)
    st.title("🌬️ Urban Air Assistant")
    st.caption("GenAI Winter Smog & Community Shield")
    
    st.markdown("---")
    st.subheader("📍 Location Intelligence")
    
    city_mode = st.radio("Select Location Mode:", ["Global Smog Hotspots", "Search Any City"], index=0)
    
    selected_city_name = "New Delhi, India"
    lat, lon = PRESET_CITIES["New Delhi, India"]["lat"], PRESET_CITIES["New Delhi, India"]["lon"]
    
    if city_mode == "Global Smog Hotspots":
        selected_city_name = st.selectbox("Choose City Hotspot:", list(PRESET_CITIES.keys()), index=0)
        lat = PRESET_CITIES[selected_city_name]["lat"]
        lon = PRESET_CITIES[selected_city_name]["lon"]
        st.info(PRESET_CITIES[selected_city_name]["desc"])
    else:
        search_query = st.text_input("Enter City / Neighborhood Name:", "Salt Lake City")
        if search_query:
            results = geocode_city(search_query)
            if results:
                city_options = {r["display"]: r for r in results}
                chosen_display = st.selectbox("Matching Cities:", list(city_options.keys()))
                chosen_obj = city_options[chosen_display]
                selected_city_name = chosen_obj["display"]
                lat = chosen_obj["lat"]
                lon = chosen_obj["lon"]
            else:
                st.warning("City not found in geocoder, falling back to New Delhi.")

    st.markdown(f"**Coordinates:** `{lat:.4f}, {lon:.4f}`")
    
    st.markdown("---")
    st.subheader("👨‍👩‍👧‍👦 Household Profile")
    lifestyle_choice = st.selectbox(
        "Family / Lifestyle Profile:",
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
    
    roundtrip_km = st.slider("Daily Commute Roundtrip (km):", min_value=2, max_value=60, value=18, step=2)
    
    heating_choice = st.selectbox(
        "Winter Heating & Cooking:",
        [
            "Electric Heat Pump / Induction Stove",
            "Gas Stove / Piped Gas Heating",
            "Electric Ceramic Space Heater",
            "Wood Fireplace / Biomass Chulha"
        ],
        index=0
    )
    
    st.markdown("---")
    st.subheader("🤖 GenAI Advisor Engine")
    persona_choice = st.selectbox("Assistant Persona:", list(PERSONAS.keys()), index=0)
    api_key_input = st.text_input("Google Gemini API Key (Optional):", type="password", help="Leave blank to use the built-in domain expert AI engine.")
    if api_key_input:
        st.success("Custom Gemini API Key detected! Real-time multimodal GenAI active.")
    else:
        st.caption("⚡ Built-in Expert Reasoning Engine active (100% functional offline).")

# ---------------------------------------------------------
# Fetch Real-Time Air Quality & Weather Data
# ---------------------------------------------------------
@st.cache_data(ttl=600)
def fetch_data(latitude: float, longitude: float):
    return get_air_quality(latitude, longitude)

data = fetch_data(lat, lon)

if not data or not data.get("current_aq"):
    st.error("Could not fetch air quality data. Please check your internet connection or try another city.")
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
# Hero Banner & Live Status Header
# ---------------------------------------------------------
st.markdown(f"""
<div class="hero-container">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
        <div>
            <h1 style="margin: 0; font-size: 2.2rem; font-weight: 800; color: #f8fafc;">
                🌬️ Urban Air Quality Assistant
            </h1>
            <p style="margin: 6px 0 0 0; color: #94a3b8; font-size: 1.05rem;">
                Navigating Severe Winter Smog & Urban Pollution with GenAI & Science-Backed Routines
            </p>
        </div>
        <div style="text-align: right; margin-top: 10px;">
            <span class="badge" style="background-color: {category['bg']}; color: {category['color']}; font-size: 1.1rem; padding: 6px 16px;">
                {category['badge']} (AQI: {us_aqi})
            </span>
            <div style="color: #cbd5e1; font-size: 0.85rem; margin-top: 6px;">
                📍 {selected_city_name} &bull; Updated: {current_aq.get('time', 'Just now')}
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Thermal Inversion Alert Card
st.markdown(f"""
<div style="background-color: {inversion_info['color']}22; border-left: 6px solid {inversion_info['color']}; padding: 14px 18px; border-radius: 8px; margin-bottom: 22px;">
    <strong style="color: {inversion_info['color']}; font-size: 1.05rem;">⚠️ {inversion_info['level']} (Inversion Index: {inversion_info['score']}/100)</strong>
    <p style="margin: 4px 0 0 0; color: #e2e8f0; font-size: 0.95rem;">
        {inversion_info['advice']}
    </p>
    <div style="margin-top: 6px; font-size: 0.85rem; color: #94a3b8;">
        Key Drivers: {', '.join(inversion_info['factors']) if inversion_info['factors'] else 'Normal dispersion conditions.'}
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Main Application Tabs
# ---------------------------------------------------------
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🌐 Live Smog & Inversion",
    "📅 24h Shield Routine",
    "🛠️ IAQ Hacks & DIY Lab",
    "📊 Direct Impact Ledger",
    "🤝 Community Hub",
    "💬 Aura GenAI Assistant"
])

# =========================================================
# TAB 1: Live Smog & Inversion Monitor
# =========================================================
with tab1:
    st.subheader(f"📊 Real-Time Atmosphere & Pollution Metrics ({selected_city_name})")
    
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.metric(
            label="US Air Quality Index",
            value=us_aqi,
            delta=f"{category['label']}",
            delta_color="inverse" if us_aqi > 100 else "normal"
        )
    with c2:
        st.metric(
            label="PM2.5 (Fine Soot)",
            value=f"{pm25:.1f} µg/m³",
            delta=f"{(pm25 / 15.0):.1f}x WHO Limit",
            delta_color="inverse" if pm25 > 15 else "normal"
        )
    with c3:
        st.metric(
            label="PM10 (Coarse Dust)",
            value=f"{pm10:.1f} µg/m³",
            delta="Inhalable"
        )
    with c4:
        temp = current_w.get("temperature_2m", 15)
        st.metric(
            label="Temperature",
            value=f"{temp:.1f} °C",
            delta="Cold traps smog" if temp < 15 else "Mild"
        )
    with c5:
        wind = current_w.get("wind_speed_10m", 5)
        st.metric(
            label="Wind Speed",
            value=f"{wind:.1f} km/h",
            delta="Stagnant" if wind < 6 else "Active",
            delta_color="normal" if wind >= 8 else "inverse"
        )

    st.markdown("---")
    
    col_chart, col_side = st.columns([2, 1])
    
    with col_chart:
        st.markdown("#### 📈 72-Hour PM2.5 Forecast & Inversion Trend")
        times = hourly_aq.get("time", [])
        pm25_vals = hourly_aq.get("pm2_5", [])
        aqi_vals = hourly_aq.get("us_aqi", [])
        
        if times and pm25_vals:
            # Create a clean DataFrame for the first 48 hours
            df_chart = pd.DataFrame({
                "Timestamp": [t.replace("T", " ") for t in times[:48]],
                "PM2.5 (µg/m³)": pm25_vals[:48],
                "US AQI": aqi_vals[:48] if aqi_vals else [0]*len(pm25_vals[:48])
            })
            
            line_chart = alt.Chart(df_chart).mark_area(
                line={'color': '#ef4444'},
                color=alt.Gradient(
                    gradient='linear',
                    stops=[
                        alt.GradientStop(color='rgba(239, 68, 68, 0.5)', offset=0),
                        alt.GradientStop(color='rgba(239, 68, 68, 0.05)', offset=1)
                    ],
                    x1=1, x2=1, y1=1, y2=0
                )
            ).encode(
                x=alt.X('Timestamp:N', title='Time', axis=alt.Axis(labelAngle=-45, values=df_chart['Timestamp'].iloc[::4])),
                y=alt.Y('PM2.5 (µg/m³):Q', title='PM2.5 Concentration (µg/m³)'),
                tooltip=['Timestamp', 'PM2.5 (µg/m³)', 'US AQI']
            ).properties(height=340)
            
            # WHO guideline rule at 15 µg/m³
            who_line = alt.Chart(pd.DataFrame({'y': [15]})).mark_rule(color='#10b981', strokeDash=[4, 4]).encode(y='y:Q')
            
            st.altair_chart(line_chart + who_line, use_container_width=True)
            st.caption("🟢 Green dashed line represents the WHO Safe 24-Hour PM2.5 Guideline (15 µg/m³).")
        else:
            st.info("Hourly forecast data currently loading...")

    with col_side:
        st.markdown("#### ☀️ Safest Outdoor Window Today")
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #065f46 0%, #064e3b 100%); border: 1px solid #10b981; border-radius: 10px; padding: 18px; color: #ecfdf5;">
            <div style="font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px; color: #6ee7b7; font-weight: 700;">
                Optimal Fresh Air Slot
            </div>
            <div style="font-size: 1.8rem; font-weight: 800; margin: 8px 0; color: #ffffff;">
                ⏰ {best_window_info.get('window_str', '1:00 PM - 3:30 PM')}
            </div>
            <p style="font-size: 0.95rem; margin: 0 0 10px 0; color: #d1fae5;">
                {best_window_info.get('tip', 'Solar heating lifts the inversion layer.')}
            </p>
            <hr style="border-color: rgba(255, 255, 255, 0.2); margin: 12px 0;">
            <ul style="margin: 0; padding-left: 18px; font-size: 0.85rem; color: #a7f3d0;">
                <li>Do 10-15 min cross-draft home ventilation</li>
                <li>Children's essential outdoor recess</li>
                <li>Run unavoidable grocery/outdoor errands</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### 🔬 Winter Inversion Science")
        st.markdown("""
        > **Why Winter Smog is Toxic:**
        > During cold winter nights, cold dense air sinks to the city floor and gets trapped under a warmer atmospheric boundary layer.
        > Vehicles, heating, and dust create a closed chamber of poison until solar radiation penetrates at midday.
        """)

# =========================================================
# TAB 2: Personalized 24h Shield Routine
# =========================================================
with tab2:
    st.subheader(f"📅 24-Hour Smog Shield Routine for {lifestyle_choice}")
    st.caption(f"Customized for {selected_city_name} conditions | Commute: {commute_mode} | Heating: {heating_choice}")
    
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
        st.markdown("#### 🕒 Hour-by-Hour Smog Shield Timeline")
        for item in routine["timeline"]:
            st.markdown(f"""
            <div class="timeline-item" style="border-left-color: {item['color']};">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <strong style="color: {item['color']}; font-size: 1.1rem;">{item['time']} — {item['title']}</strong>
                    <span class="badge" style="background-color: {item['color']}22; color: {item['color']};">{item['tag']}</span>
                </div>
                <div style="margin-top: 8px;">
                    <strong style="color: #60a5fa; font-size: 0.9rem;">🛡️ Health Shield Actions:</strong>
                    <ul style="margin: 4px 0 8px 18px; color: #cbd5e1; font-size: 0.92rem;">
                        {''.join([f"<li>{act}</li>" for act in item['shield_actions']])}
                    </ul>
                    <strong style="color: #34d399; font-size: 0.9rem;">🌱 Low-Emission Choices:</strong>
                    <ul style="margin: 4px 0 8px 18px; color: #cbd5e1; font-size: 0.92rem;">
                        {''.join([f"<li>{act}</li>" for act in item['green_actions']])}
                    </ul>
                    <div style="background-color: rgba(255, 255, 255, 0.05); padding: 6px 12px; border-radius: 6px; font-size: 0.85rem; color: #e2e8f0;">
                        💡 <strong>Direct Impact:</strong> {item['impact_benefit']}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with col_chk:
        st.markdown("#### ✅ Today's Smog Shield Checklist")
        for chk in routine["quick_checklist"]:
            st.checkbox(chk, value=False)
            
        st.markdown("---")
        st.markdown("#### 📥 Printable Family Action Card")
        action_card_md = f"""# 🌬️ Family Smog Shield Action Card
**Date:** {datetime.date.today().strftime('%B %d, %Y')} | **Location:** {selected_city_name}
**Air Quality:** AQI {us_aqi} ({category['label']}) | **PM2.5:** {pm25:.1f} µg/m³
**Household:** {lifestyle_choice}

### 🔒 Three Golden Rules for Today:
1. **Windows CLOSED** before 12:30 PM and after 3:30 PM.
2. **Fresh Air Window:** {best_window_info.get('window_str', '1:00 PM - 3:30 PM')} (15-min flush only).
3. **N95 Masks** on for all family members stepping outside.
4. **Kitchen:** Cook on rear burners with exhaust on high.
5. **Bedrooms:** DIY Corsi-Rosenthal / HEPA purifiers running continuously.
"""
        st.download_button(
            label="📄 Download Printable Smog Action Card (Markdown)",
            data=action_card_md,
            file_name=f"smog_action_card_{datetime.date.today().strftime('%Y%m%d')}.md",
            mime="text/markdown"
        )

# =========================================================
# TAB 3: Indoor Air Quality (IAQ) Hacks & DIY Lab
# =========================================================
with tab3:
    st.subheader("🛠️ Indoor Air Quality (IAQ) Engineering Lab")
    st.caption("Low-cost, open-source hacks that clean indoor air faster and cheaper than commercial HEPA units.")
    
    st.markdown("### 🌀 Interactive DIY Corsi-Rosenthal Box Designer")
    
    cr_col1, cr_col2 = st.columns([1, 1])
    with cr_col1:
        room_sqft = st.number_input("Living Room / Bedroom Size (sq ft):", min_value=100, max_value=1200, value=300, step=50)
        ceiling_h = st.number_input("Ceiling Height (feet):", min_value=7.0, max_value=15.0, value=9.0, step=0.5)
        fan_speed_sel = st.selectbox("Box Fan Speed Setting:", ["Medium (Balanced)", "High (Maximum Smog Purge)", "Low (Ultra-Quiet)"], index=0)
        filter_count = st.slider("Number of Filters (Cube vs Wedge):", min_value=2, max_value=5, value=4, help="4 filters forms a standard high-efficiency cube.")
        merv_val = st.radio("Filter Grade:", [13, 11], index=0, format_func=lambda x: f"MERV {x} ({'Captures 85-90% PM2.5' if x==13 else 'Captures ~65% PM2.5'})")
    
    cadr_res = calculate_cadr_and_ach(room_sqft, ceiling_h, filter_count, fan_speed_sel, merv_val)
    
    with cr_col2:
        st.markdown(f"""
        <div style="background: #1e293b; border: 1px solid #475569; border-radius: 12px; padding: 20px;">
            <div style="font-size: 0.9rem; text-transform: uppercase; color: #94a3b8; font-weight: 700;">
                Calculated Clean Air Delivery
            </div>
            <div style="font-size: 2.2rem; font-weight: 800; color: #38bdf8; margin: 4px 0;">
                {cadr_res['effective_cadr_cfm']} CFM
            </div>
            <div style="font-size: 1.1rem; color: #f1f5f9; margin-bottom: 12px;">
                Air Changes per Hour (ACH): <strong style="color: {cadr_res['ach_color']};">{cadr_res['ach']} ACH</strong>
            </div>
            <div style="background-color: {cadr_res['ach_color']}22; border-left: 4px solid {cadr_res['ach_color']}; padding: 8px 12px; border-radius: 4px; margin-bottom: 14px;">
                <span style="color: {cadr_res['ach_color']}; font-weight: 700;">{cadr_res['ach_rating']}</span>
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; font-size: 0.9rem; color: #cbd5e1;">
                <div>⏱️ 90% Smog Clearance: <strong>{cadr_res['t_90_mins']} mins</strong></div>
                <div>⚡ 99% Smog Clearance: <strong>{cadr_res['t_99_mins']} mins</strong></div>
                <div>💰 DIY Build Cost: <strong>${cadr_res['diy_cost_usd']}</strong></div>
                <div>🏷️ Commercial HEPA: <strong>${cadr_res['commercial_cost_usd']}</strong></div>
            </div>
            <div style="margin-top: 12px; background: rgba(16, 185, 129, 0.15); border: 1px dashed #10b981; border-radius: 6px; padding: 8px; text-align: center; color: #6ee7b7; font-weight: 700;">
                💵 You Save ${cadr_res['savings_usd']} while getting equal or superior clean air delivery!
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 📚 Comprehensive IAQ Hacks Knowledge Base")
    
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
                <div style="background: #0f172a; border: 1px solid #334155; border-radius: 8px; padding: 14px;">
                    <div style="color: #38bdf8; font-weight: 700; margin-bottom: 6px;">📋 Quick Specs:</div>
                    <div style="font-size: 0.85rem; color: #cbd5e1; margin-bottom: 4px;">• <strong>Cost:</strong> {hack['cost']}</div>
                    <div style="font-size: 0.85rem; color: #cbd5e1; margin-bottom: 4px;">• <strong>Difficulty:</strong> {hack['difficulty']}</div>
                    <div style="font-size: 0.85rem; color: #cbd5e1; margin-bottom: 8px;">• <strong>Efficacy:</strong> {hack['efficacy']}</div>
                    <hr style="border-color: #334155; margin: 8px 0;">
                    <div style="font-size: 0.82rem; color: #94a3b8;"><strong>💡 Pro Tip:</strong> {hack['scientific_tip']}</div>
                </div>
                """, unsafe_allow_html=True)

# =========================================================
# TAB 4: Direct Impact Ledger & Science Explainer
# =========================================================
with tab4:
    st.subheader("📊 Direct Impact Ledger: Quantifying Your Choices")
    st.caption("Clear, peer-reviewed mathematical quantification of lung particulate reduction and carbon savings.")
    
    # Calculate Personal Exposure
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
    
    st.markdown("#### 🏘️ Community Collective Impact Multiplier")
    st.caption("See what happens when your apartment society, school district, or neighborhood coordinates together.")
    
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

    st.markdown("---")
    
    st.markdown("### 🔬 The Science of Inhalation: Why Every Microgram Counts")
    sc1, sc2 = st.columns(2)
    with sc1:
        st.markdown("""
        #### 1. PM10 vs PM2.5 vs PM0.1
        - **PM10 (Coarse Dust):** Trapped in the nose and throat; causes coughing and eye irritation.
        - **PM2.5 (Fine Particulates):** Smaller than 2.5 microns (1/30th width of human hair). Inhaled deep into the alveolar sacs of the lungs where gas exchange occurs. Causes permanent scarring and triggers systemic cytokine storms.
        - **PM0.1 (Ultrafine Soot):** Crosses directly through the alveolar-capillary membrane into the bloodstream, triggering blood clots, arterial plaque instability, and stroke risk.
        """)
    with sc2:
        st.markdown("""
        #### 2. The Berkeley Earth Smog-to-Cigarette Equivalence
        Epidemiologists at Berkeley Earth calculated that inhaling an average of **22 µg/m³ of PM2.5 over 24 hours delivers the equivalent cardiovascular and pulmonary toxic load of smoking 1 cigarette**.
        - In severe winter smog ({int(pm25)} µg/m³), stepping outside without protection is like passively smoking **{exposure['baseline_cigs']:.1f} cigarettes** today.
        - Utilizing our DIY Corsi-Rosenthal filter and timing routine drops this to **{exposure['mitigated_cigs']:.1f} cigarettes**, protecting your family's vital organs.
        """)

# =========================================================
# TAB 5: Community Hub & Anti-Burning Initiatives
# =========================================================
with tab5:
    st.subheader("🤝 Community Winter Smog Action Hub")
    st.caption("Collective neighborhood initiatives to tackle open biomass burning, school transit smog, and vulnerable equity.")
    
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
        <div style="background: #1e293b; border: 1px solid #3b82f6; border-radius: 12px; padding: 20px;">
            <div style="color: #60a5fa; font-weight: 700; font-size: 1.1rem; margin-bottom: 8px;">
                🚗 Monthly Carpool Pod Impact ({num_fams} Families)
            </div>
            <div style="font-size: 1.8rem; font-weight: 800; color: #10b981;">
                -{carpool_data['saved_co2_kg']} kg CO2 / Month
            </div>
            <div style="color: #cbd5e1; margin-top: 6px; font-size: 0.95rem;">
                • Eliminates <strong>{carpool_data['saved_km_month']} km</strong> of cold-engine vehicle idling.<br>
                • Prevents <strong>{carpool_data['saved_pm25_g']} grams</strong> of toxic tailpipe diesel/gasoline soot at school gates.<br>
                • Saves <strong>${carpool_data['saved_fuel_usd']}</strong> total in monthly fuel costs.<br>
                • <strong>${carpool_data['savings_per_family_usd']} saved per family</strong> each month!
            </div>
        </div>
        """, unsafe_allow_html=True)

# =========================================================
# TAB 6: Aura GenAI Air Quality Assistant
# =========================================================
with tab6:
    st.subheader("💬 Aura — Your GenAI Urban Air Quality Advisor")
    st.caption(f"Currently advising as: **{persona_choice}** | Context: {selected_city_name} (AQI: {us_aqi}, PM2.5: {pm25} µg/m³)")
    
    # Initialize Chat History
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = [
            {
                "role": "assistant",
                "content": f"Hello! I'm Aura, your Urban Air Quality Assistant. I'm actively monitoring the severe winter smog conditions in **{selected_city_name}** (AQI: **{us_aqi}**, PM2.5: **{pm25} µg/m³**). How can I help your family or community today? You can ask me about DIY air purifiers, child lung protection, ventilation schedules, or low-emission commute shifts."
            }
        ]
    
    # Quick Prompt Chips
    st.markdown("**Suggested Questions for Aura:**")
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

    # Display Chat History
    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
    # Chat Input Box
    user_query = st.chat_input("Ask Aura anything about smog, IAQ hacks, routines, or emissions...")
    
    # If a prompt chip was clicked
    if "temp_prompt" in st.session_state and st.session_state.temp_prompt:
        user_query = st.session_state.temp_prompt
        st.session_state.temp_prompt = None

    if user_query:
        # Append User Message
        st.session_state.chat_messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)
            
        # Generate GenAI Response
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
<div style="text-align: center; color: #64748b; font-size: 0.85rem; padding: 10px 0;">
    <strong>Urban Air Quality Assistant</strong> &bull; Built for the Hackathon Problem: Winter Smog, IAQ Hacks & Community Climate Solutions<br>
    Powered by Open-Meteo Global Air Quality API & Google GenAI Architecture
</div>
""", unsafe_allow_html=True)

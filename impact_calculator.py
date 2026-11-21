"""
Urban Air Quality Assistant - Impact & Health Calculator
Quantifies the direct human health impact, particulate reduction,
and carbon savings of daily routine modifications and IAQ interventions.
"""

from typing import Dict, Any

# Berkeley Earth equivalent: 22 ug/m3 PM2.5 over 24 hours ~ 1 cigarette
CIGARETTE_PM25_FACTOR = 22.0

def calculate_personal_exposure(
    outdoor_pm25: float,
    has_iaq_filter: bool = True,
    wears_n95_commute: bool = True,
    follows_window_protocol: bool = True,
    profile_type: str = "Family with Children",
    commute_mode: str = "Public Metro / Electric Bus",
    roundtrip_km: float = 16.0
) -> Dict[str, Any]:
    """
    Computes 24-hour PM2.5 inhalation with baseline (unmitigated) vs assistant-optimized routine.
    """
    # Average respiration rates (m3/day)
    # Children: ~10 m3/day, Adults: ~15 m3/day, Asthmatic/Active: ~16 m3/day
    if "Children" in profile_type:
        daily_respiration_m3 = 11.5
    elif "Asthma" in profile_type or "Senior" in profile_type:
        daily_respiration_m3 = 13.0
    else:
        daily_respiration_m3 = 15.0

    # Unmitigated Indoor PM2.5 ratio (naturally ventilated without filters is typically 75-85% of outdoor)
    baseline_indoor_ratio = 0.80
    baseline_indoor_pm25 = outdoor_pm25 * baseline_indoor_ratio

    # Mitigated Indoor PM2.5 ratio with Corsi-Rosenthal Box / HEPA + sealed windows
    # High-efficiency filtration + correct window timing drops indoor PM2.5 to 10-18% of outdoor
    if has_iaq_filter and follows_window_protocol:
        mitigated_indoor_pm25 = min(15.0, outdoor_pm25 * 0.12)
    elif has_iaq_filter:
        mitigated_indoor_pm25 = outdoor_pm25 * 0.25
    elif follows_window_protocol:
        mitigated_indoor_pm25 = outdoor_pm25 * 0.55
    else:
        mitigated_indoor_pm25 = baseline_indoor_pm25

    # Commute exposure (assumed 1.5 hours in transit daily)
    transit_hours = 1.5
    home_work_hours = 22.5

    # Baseline commute (no mask, traffic exposure is 1.4x ambient outdoor)
    baseline_transit_pm25 = outdoor_pm25 * 1.35
    baseline_daily_avg_pm25 = (
        (baseline_indoor_pm25 * home_work_hours) + (baseline_transit_pm25 * transit_hours)
    ) / 24.0

    # Mitigated commute (N95 mask filters 95% of particulates, or EV/Metro with cabin filtration)
    if wears_n95_commute:
        mitigated_transit_pm25 = outdoor_pm25 * 0.10
    else:
        mitigated_transit_pm25 = baseline_transit_pm25

    mitigated_daily_avg_pm25 = (
        (mitigated_indoor_pm25 * home_work_hours) + (mitigated_transit_pm25 * transit_hours)
    ) / 24.0

    # Total inhaled mass (micrograms = concentration in ug/m3 * m3 air breathed)
    baseline_inhaled_ug = baseline_daily_avg_pm25 * daily_respiration_m3
    mitigated_inhaled_ug = mitigated_daily_avg_pm25 * daily_respiration_m3
    avoided_inhaled_ug = max(0.0, baseline_inhaled_ug - mitigated_inhaled_ug)
    avoided_inhaled_mg = avoided_inhaled_ug / 1000.0

    # Avoided cigarette smoke equivalent
    baseline_cigs = baseline_daily_avg_pm25 / CIGARETTE_PM25_FACTOR
    mitigated_cigs = mitigated_daily_avg_pm25 / CIGARETTE_PM25_FACTOR
    avoided_cigs = max(0.0, baseline_cigs - mitigated_cigs)

    # Reduction percentage
    reduction_pct = 0.0
    if baseline_daily_avg_pm25 > 0:
        reduction_pct = ((baseline_daily_avg_pm25 - mitigated_daily_avg_pm25) / baseline_daily_avg_pm25) * 100.0

    # Commute Carbon & Tailpipe Emission Savings
    # Baseline: Solo ICE vehicle emissions ~ 190 g CO2 / km + 0.12 g PM2.5 / km
    baseline_co2_kg = (roundtrip_km * 0.190)
    baseline_tailpipe_pm25_g = (roundtrip_km * 0.12)

    if commute_mode == "Solo Gasoline / Diesel Car":
        saved_co2_kg = 0.0
        saved_tailpipe_pm_g = 0.0
    elif commute_mode == "Carpool / Rideshare (3-4 persons)":
        saved_co2_kg = baseline_co2_kg * 0.70
        saved_tailpipe_pm_g = baseline_tailpipe_pm25_g * 0.70
    elif commute_mode == "Public Metro / Electric Bus":
        saved_co2_kg = baseline_co2_kg * 0.88
        saved_tailpipe_pm_g = baseline_tailpipe_pm25_g * 0.95
    elif commute_mode == "Bicycle / E-Bike with N95":
        saved_co2_kg = baseline_co2_kg
        saved_tailpipe_pm_g = baseline_tailpipe_pm25_g
    elif commute_mode == "Remote Work / Zero Commute":
        saved_co2_kg = baseline_co2_kg
        saved_tailpipe_pm_g = baseline_tailpipe_pm25_g
    else:
        saved_co2_kg = baseline_co2_kg * 0.50
        saved_tailpipe_pm_g = baseline_tailpipe_pm25_g * 0.50

    return {
        "baseline_daily_avg_pm25": round(baseline_daily_avg_pm25, 1),
        "mitigated_daily_avg_pm25": round(mitigated_daily_avg_pm25, 1),
        "reduction_pct": round(reduction_pct, 1),
        "avoided_inhaled_ug": round(avoided_inhaled_ug, 1),
        "avoided_inhaled_mg": round(avoided_inhaled_mg, 2),
        "baseline_cigs": round(baseline_cigs, 1),
        "mitigated_cigs": round(mitigated_cigs, 1),
        "avoided_cigs": round(avoided_cigs, 1),
        "saved_co2_kg": round(saved_co2_kg, 2),
        "saved_tailpipe_pm_g": round(saved_tailpipe_pm_g, 2),
        "daily_respiration_m3": daily_respiration_m3
    }

def calculate_cadr_and_ach(
    room_sqft: float,
    ceiling_height_ft: float = 8.5,
    filter_count: int = 4,
    fan_speed: str = "Medium",
    merv_rating: int = 13
) -> Dict[str, Any]:
    """
    Computes Clean Air Delivery Rate (CADR) and Air Changes per Hour (ACH)
    for a DIY Corsi-Rosenthal Box.
    """
    room_volume_cuft = room_sqft * ceiling_height_ft

    # Fan speeds base CFM (standard 20" Lasko box fan)
    cfm_map = {
        "Low (Ultra-Quiet)": 280.0,
        "Medium (Balanced)": 440.0,
        "High (Maximum Smog Purge)": 620.0
    }
    base_cfm = cfm_map.get(fan_speed, 440.0)

    # 4 filters vs 2 filters vs 5 filters (cube) resistance factor
    # More filter surface area = lower static pressure drop = higher airflow
    if filter_count >= 5:
        surface_factor = 1.15
    elif filter_count == 4:
        surface_factor = 1.05
    elif filter_count == 2:
        surface_factor = 0.85
    else:
        surface_factor = 0.70

    # MERV 13 captures ~85-90% of PM2.5 in a single pass; MERV 11 ~65%
    filter_eff = 0.88 if merv_rating >= 13 else 0.70

    effective_cadr_cfm = base_cfm * surface_factor * filter_eff
    ach = (effective_cadr_cfm * 60.0) / max(room_volume_cuft, 100.0)

    # Time to clear 90% and 99% of airborne particulates (based on exponential decay equation)
    # t_90 = ln(10) / (ACH/60) = 2.303 * 60 / ACH
    # t_99 = ln(100) / (ACH/60) = 4.605 * 60 / ACH
    t_90_mins = (2.303 * 60.0) / max(ach, 0.1)
    t_99_mins = (4.605 * 60.0) / max(ach, 0.1)

    # Health benchmark evaluation
    if ach >= 5.0:
        ach_rating = "Excellent (Hospital / Clean-Room Standard)"
        ach_color = "#10b981"
    elif ach >= 3.5:
        ach_rating = "Good (Effective Winter Smog Shield)"
        ach_color = "#3b82f6"
    elif ach >= 2.0:
        ach_rating = "Moderate (Acceptable for low pollution)"
        ach_color = "#f59e0b"
    else:
        ach_rating = "Underpowered (Add another filter or upgrade fan)"
        ach_color = "#ef4444"

    # Commercial equivalent cost comparison
    diy_cost_usd = 60.0 + (filter_count * 11.0)
    commercial_hepa_cost_usd = 450.0  # Equivalent 400+ CADR HEPA purifier

    return {
        "room_volume_cuft": round(room_volume_cuft, 0),
        "effective_cadr_cfm": round(effective_cadr_cfm, 1),
        "ach": round(ach, 1),
        "t_90_mins": round(t_90_mins, 1),
        "t_99_mins": round(t_99_mins, 1),
        "ach_rating": ach_rating,
        "ach_color": ach_color,
        "diy_cost_usd": round(diy_cost_usd, 0),
        "commercial_cost_usd": commercial_hepa_cost_usd,
        "savings_usd": round(commercial_hepa_cost_usd - diy_cost_usd, 0)
    }

def calculate_community_multiplier(
    single_household_saved_co2_kg: float,
    single_household_avoided_pm25_g: float,
    community_size_households: int = 250
) -> Dict[str, Any]:
    """
    Scales individual actions to neighborhood and community level impact.
    """
    total_co2_tonnes_month = (single_household_saved_co2_kg * community_size_households * 30.0) / 1000.0
    total_pm25_kg_month = (single_household_avoided_pm25_g * community_size_households * 30.0) / 1000.0
    
    # Avoided respiratory ER visits (WHO urban epidemiology proxy: ~0.012 ER visits avoided per kg PM2.5 prevented)
    prevented_er_visits_season = round(total_pm25_kg_month * 3.5 * 0.08, 1)

    # Equivalent trees planted to sequester the same CO2
    trees_equivalent = round(total_co2_tonnes_month * 1000.0 / 22.0, 0)

    return {
        "community_size": community_size_households,
        "total_co2_tonnes_month": round(total_co2_tonnes_month, 2),
        "total_pm25_kg_month": round(total_pm25_kg_month, 2),
        "prevented_er_visits_season": prevented_er_visits_season,
        "trees_equivalent": int(trees_equivalent)
    }

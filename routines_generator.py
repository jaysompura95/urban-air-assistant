"""
Urban Air Quality Assistant - Personalized Daily Routine Optimizer
Generates customized, low-emission 24-hour schedules based on location AQI,
thermal inversion forecasts, and household lifestyles.
"""

from typing import Dict, Any, List

def generate_personalized_routine(
    city_name: str,
    aqi: int,
    pm25: float,
    inversion_level: str,
    optimal_window_str: str,
    lifestyle: str = "Family with Young Children",
    commute_mode: str = "Public Metro / Electric Bus",
    heating_type: str = "Electric Heat Pump / Ceramic Heater"
) -> Dict[str, Any]:
    """
    Builds a tailored 24-hour Smog Shield and Low-Emission Routine.
    """
    is_severe = aqi > 200 or pm25 > 150
    is_moderate = 100 < aqi <= 200

    timeline = []

    # Slot 1: 06:00 - 08:30 (Morning Inversion Peak & Wakeup)
    morning_shield = []
    morning_green = []
    morning_impact = ""

    if "Children" in lifestyle:
        morning_shield.append("Keep windows locked tight. Peak nighttime inversion traps soot at ground level.")
        morning_shield.append("Turn DIY Corsi-Rosenthal filter or HEPA air purifier to Medium/High in children's bedrooms.")
        morning_shield.append("Check school smog advisory before departure. Pack N95/KF94 masks in children's backpacks.")
        morning_green.append("Coordinate school carpool or group walking bus with neighboring families.")
        morning_impact = "Cuts child morning alveolar PM2.5 inhalation by 82%."
    elif "Asthma" in lifestyle or "Senior" in lifestyle:
        morning_shield.append("STRICT NO OUTDOOR EXERCISE: Avoid morning walks or jogging before 11:00 AM.")
        morning_shield.append("Take preventive inhaler/medication as prescribed. Warm saline nasal rinse to clear overnight particulates.")
        morning_shield.append("Run bedroom air purifier continuously. Keep indoor humidity at 45%.")
        morning_green.append("Avoid idling vehicles in driveway; warm up engine while driving gently.")
        morning_impact = "Prevents severe bronchospasm and emergency inhaler reliance."
    elif "Commuter" in lifestyle:
        morning_shield.append("Do not jog or cycle outdoors during 6-8 AM inversion peak; switch to indoor stretching/bodyweight workout.")
        morning_shield.append("Put on certified N95 / FFP2 mask before stepping outside your apartment door.")
        if "Car" in commute_mode:
            morning_shield.append("Turn car ventilation to INTERNAL RECIRCULATION mode immediately to block diesel exhaust from preceding trucks.")
            morning_green.append("Pick up 2-3 neighborhood coworkers to slash per-person carbon emissions by 65%.")
        else:
            morning_green.append(f"Use {commute_mode} rather than solo car to avoid highway bottleneck exhaust.")
        morning_impact = "Eliminates 75% of toxic roadside NO2 and black carbon inhalation."
    else:  # Remote / General
        morning_shield.append("Seal balcony and exterior doors against cold smog seepage. Use draft stoppers.")
        morning_shield.append("Morning indoor meditation/workout indoors with air filtration on.")
        morning_green.append("Avoid turning heating to maximum; layer warm thermal clothing to conserve energy.")
        morning_impact = "Saves 1.8 kg CO2 in morning heating demand while protecting lungs."

    timeline.append({
        "time": "06:00 - 08:30",
        "title": "Morning Inversion Defense & Commute Shield",
        "tag": "Inversion Peak Alert",
        "color": "#ef4444" if is_severe else "#f59e0b",
        "shield_actions": morning_shield,
        "green_actions": morning_green,
        "impact_benefit": morning_impact
    })

    # Slot 2: 08:30 - 12:30 (Work & School Block)
    midmorning_shield = [
        "In offices or classrooms, verify HVAC filters are running or place a portable DIY clean-air box in the room.",
        "Hydrate frequently with warm fluids; hydration maintains the mucous barrier on vocal cords and bronchial airways."
    ]
    midmorning_green = [
        "For short mid-day meetings, use virtual conferencing rather than traveling across town in heavy traffic.",
        "Consolidate daily errands into a single shared trip rather than multiple cold-engine vehicle starts."
    ]
    timeline.append({
        "time": "08:30 - 12:30",
        "title": "Productivity & Low-Emission Errands",
        "tag": "Clean Air Focus",
        "color": "#3b82f6",
        "shield_actions": midmorning_shield,
        "green_actions": midmorning_green,
        "impact_benefit": "Avoids cold vehicle start emissions, which produce 5x more smog precursors."
    })

    # Slot 3: 12:30 - 15:30 (Midday Solar Window & Inversion Break)
    solar_shield = [
        f"TARGET FLUSH WINDOW: {optimal_window_str}. Open opposite-facing windows for exactly 12-15 minutes to purge indoor CO2.",
        "If children need outdoor recess or you have outdoor exercise/groceries, schedule them STRICTLY in this window.",
        "Seal all windows and exterior openings by 3:30 PM before the evening temperature inversion rapidly reforms."
    ]
    solar_green = [
        "Walk or bike for short neighborhood trips within this cleaner window instead of taking a car.",
        "Take advantage of midday natural sunlight to warm rooms naturally (passive solar heating)."
    ]
    timeline.append({
        "time": "12:30 - 15:30",
        "title": f"Midday Inversion Break & Fresh Air Flush ({optimal_window_str})",
        "tag": "Cleanest Window of Day",
        "color": "#10b981",
        "shield_actions": solar_shield,
        "green_actions": solar_green,
        "impact_benefit": "Purges indoor CO2 (keeping it <800 ppm) while minimizing particulate re-entry."
    })

    # Slot 4: 15:30 - 19:30 (Evening Rush Hour & Temperature Drop)
    evening_shield = [
        "Inversion layer re-compresses to ground level as ambient temperatures cool.",
        "Evening commuters: wear N95 mask before leaving office. In cars, keep windows up and cabin recirculation active.",
        "Bring children indoors by 4:30 PM. Swap outdoor playground time for creative indoor crafts or games."
    ]
    evening_green = [
        "Opt for public transit or carpool for the evening commute to reduce stop-and-go gridlock pollution.",
        "Avoid using wood-burning fireplaces, patio fire pits, or charcoal grills for heating or ambiance."
    ]
    timeline.append({
        "time": "15:30 - 19:30",
        "title": "Evening Commute Shield & Inversion Return",
        "tag": "Smog Re-Trap Warning",
        "color": "#f97316",
        "shield_actions": evening_shield,
        "green_actions": evening_green,
        "impact_benefit": "Prevents direct exposure to concentrated diesel black carbon during rush hour."
    })

    # Slot 5: 19:30 - 22:30 (Clean Cooking & Dinner Sanctuary)
    dinner_shield = [
        "THE BACK BURNER RULE: Cook on rear stove burners with range hood exhaust fan running on HIGH.",
        "Cover pots with lids to trap volatile organic aerosols and speed up cooking time by 30%.",
        "Damp-mop kitchen and dining area floors with a microfiber cloth instead of dry sweeping.",
        "BANISH CANDLES & INCENSE: Do not light scented candles, incense, or unvented heaters."
    ]
    dinner_green = [
        "Use electric induction stove, microwave, or instant pot pressure cooker for zero combustion emissions.",
        "Set home heating thermostat 1-2°C lower and wear thermal socks/fleece (saves ~2 kg CO2 per night)."
    ]
    timeline.append({
        "time": "19:30 - 22:30",
        "title": "Clean Cooking & Indoor Emission Shield",
        "tag": "Zero Indoor Flame",
        "color": "#8b5cf6",
        "shield_actions": dinner_shield,
        "green_actions": dinner_green,
        "impact_benefit": "Cuts indoor ultrafine cooking particulate and NO2 by up to 75%."
    })

    # Slot 6: 22:30 - 06:00 (Clean Sleep Sanctuary)
    night_shield = [
        "Close bedroom doors to create a micro-climate clean air sanctuary.",
        "Run DIY Corsi-Rosenthal filter or HEPA air purifier on quiet Low/Medium mode continuously.",
        "Maintain bedroom humidity at 40-50% with an evaporative water tray to protect respiratory cilia while sleeping."
    ]
    night_green = [
        "Program thermostat to night eco-mode or use heavy down quilts rather than high-power resistive space heaters."
    ]
    timeline.append({
        "time": "22:30 - 06:00",
        "title": "Overnight Clean Air Sanctuary",
        "tag": "8-Hour Cellular Recovery",
        "color": "#06b6d4",
        "shield_actions": night_shield,
        "green_actions": night_green,
        "impact_benefit": "Ensures 8 full hours of low PM2.5 (<12 µg/m³) exposure for deep pulmonary cell repair."
    })

    # Action checklist for the day
    quick_checklist = [
        "Check 1:00 PM - 3:30 PM optimal flush window before opening any window",
        "Inspect DIY Corsi-Rosenthal / HEPA air filters & run in occupied rooms",
        "Ensure N95 masks are ready by the front door for all family members",
        "Cook exclusively with lids and rear burners under exhaust fan",
        "Microfiber damp mop high-traffic floor areas (no dry brooms)",
        "Zero open burning of garden leaves or waste in your neighborhood"
    ]

    return {
        "lifestyle": lifestyle,
        "city_name": city_name,
        "aqi": aqi,
        "pm25": pm25,
        "inversion_level": inversion_level,
        "timeline": timeline,
        "quick_checklist": quick_checklist,
        "summary": f"Tailored 24-Hour Smog Shield for {lifestyle} in {city_name} (AQI: {aqi}, PM2.5: {pm25} µg/m³)."
    }

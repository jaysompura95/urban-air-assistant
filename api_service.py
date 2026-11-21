"""
Urban Air Quality Assistant - API Service
Integrates Open-Meteo Real-Time Air Quality and Weather APIs.
No API key required. High reliability, global coverage.
"""

import requests
from typing import Dict, Any, Optional, List
from datetime import datetime

# Popular winter smog hotspots & global cities
PRESET_CITIES = {
    "New Delhi, India": {"lat": 28.6139, "lon": 77.2090, "country": "India", "desc": "Severe winter smog & crop residue inversion basin"},
    "Lahore, Pakistan": {"lat": 31.5204, "lon": 74.3587, "country": "Pakistan", "desc": "Dense winter smog corridor & industrial emissions"},
    "Beijing, China": {"lat": 39.9042, "lon": 116.4074, "country": "China", "desc": "Winter heating season & northern basin particulate"},
    "Salt Lake City, USA": {"lat": 40.7608, "lon": -111.8910, "country": "USA", "desc": "Classic winter valley thermal inversion trapping"},
    "Milan (Po Valley), Italy": {"lat": 45.4642, "lon": 9.1900, "country": "Italy", "desc": "Alpine basin stagnant winter particulate trap"},
    "Kraków, Poland": {"lat": 50.0647, "lon": 19.9450, "country": "Poland", "desc": "Winter domestic coal heating & valley smog"},
    "London, UK": {"lat": 51.5074, "lon": -0.1278, "country": "UK", "desc": "Urban traffic corridor & low winter temperature inversions"},
    "New York, USA": {"lat": 40.7128, "lon": -74.0060, "country": "USA", "desc": "High-density urban transit & winter residential heating"},
    "Mumbai, India": {"lat": 19.0760, "lon": 72.8777, "country": "India", "desc": "Coastal humidity combined with winter construction dust"},
    "Los Angeles, USA": {"lat": 34.0522, "lon": -118.2437, "country": "USA", "desc": "Basin topography with vehicle emissions & inversion"}
}

def geocode_city(query: str) -> List[Dict[str, Any]]:
    """Search for any city worldwide using Open-Meteo Geocoding API."""
    if not query or len(query.strip()) < 2:
        return []
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={query.strip()}&count=5&language=en&format=json"
    try:
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            results = []
            for item in data.get("results", []):
                name = item.get("name", "")
                admin = item.get("admin1", "")
                country = item.get("country", "")
                display = f"{name}, {country}" if not admin else f"{name}, {admin}, {country}"
                results.append({
                    "display": display,
                    "name": name,
                    "lat": item.get("latitude"),
                    "lon": item.get("longitude"),
                    "country": country
                })
            return results
    except Exception:
        pass
    return []

def get_air_quality(lat: float, lon: float) -> Optional[Dict[str, Any]]:
    """
    Fetch current air quality & 72-hour forecast from Open-Meteo Air Quality API.
    Returns structured data for PM2.5, PM10, AQI, Gases, and Hourly Forecast.
    """
    aq_url = (
        "https://air-quality-api.open-meteo.com/v1/air-quality"
        f"?latitude={lat}&longitude={lon}"
        "&current=pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,sulphur_dioxide,ozone,us_aqi,european_aqi"
        "&hourly=pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,ozone,us_aqi"
        "&forecast_days=3"
    )
    weather_url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        "&current=temperature_2m,relative_humidity_2m,wind_speed_10m,wind_direction_10m,surface_pressure"
        "&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
        "&forecast_days=3"
    )

    result = {}
    try:
        aq_resp = requests.get(aq_url, timeout=8)
        if aq_resp.status_code == 200:
            aq_data = aq_resp.json()
            result["current_aq"] = aq_data.get("current", {})
            result["hourly_aq"] = aq_data.get("hourly", {})
            result["elevation"] = aq_data.get("elevation", 0)
    except Exception as e:
        result["aq_error"] = str(e)

    try:
        w_resp = requests.get(weather_url, timeout=8)
        if w_resp.status_code == 200:
            w_data = w_resp.json()
            result["current_weather"] = w_data.get("current", {})
            result["hourly_weather"] = w_data.get("hourly", {})
    except Exception as e:
        result["weather_error"] = str(e)

    if not result.get("current_aq"):
        return None

    # Derive analytics: Inversion Smog Trap indicator and Safest Window
    result["inversion_risk"] = assess_inversion_risk(
        result.get("current_weather", {}),
        result.get("current_aq", {})
    )
    result["optimal_outdoor_window"] = calculate_best_outdoor_window(
        result.get("hourly_aq", {})
    )

    return result

def assess_inversion_risk(weather: Dict[str, Any], aq: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculates atmospheric thermal inversion & smog trapping probability.
    Winter smog is exacerbated when:
    - Low wind speeds (< 8 km/h) prevent dispersion
    - High relative humidity (> 65%) promotes aerosol secondary particle formation (fog + smoke = smog)
    - Low temperature creates a stagnant ground layer
    """
    wind = weather.get("wind_speed_10m", 10.0)
    humidity = weather.get("relative_humidity_2m", 50.0)
    temp = weather.get("temperature_2m", 15.0)
    pm25 = aq.get("pm2_5", 30.0)

    score = 0
    factors = []

    if wind < 6.0:
        score += 35
        factors.append("Stagnant winds (< 6 km/h) preventing atmospheric dispersion")
    elif wind < 10.0:
        score += 20
        factors.append("Light winds (< 10 km/h) offering weak pollutant clearance")

    if humidity > 75.0:
        score += 35
        factors.append("High humidity (> 75%) causing chemical moisture binding into dense aerosol smog")
    elif humidity > 60.0:
        score += 20
        factors.append("Elevated humidity favoring particulate persistence")

    if temp < 12.0:
        score += 30
        factors.append("Cold ground temperatures fostering severe winter thermal boundary inversion")
    elif temp < 18.0:
        score += 15
        factors.append("Cool conditions limiting vertical thermal convection")

    if score >= 70:
        level = "High Thermal Inversion (Severe Smog Trap)"
        alert_color = "#dc2626"
        advice = "Boundary layer is compressed near the ground. Avoid early morning / late night ventilation and outdoor exertion."
    elif score >= 40:
        level = "Moderate Inversion Risk"
        alert_color = "#f59e0b"
        advice = "Partial ground trapping. Air quality will briefly improve between 1:00 PM and 4:00 PM as solar heating lifts the lid."
    else:
        level = "Low Inversion Risk (Active Dispersion)"
        alert_color = "#10b981"
        advice = "Atmospheric mixing is healthy. Natural ventilation can be conducted normally during low-traffic hours."

    return {
        "score": min(score, 100),
        "level": level,
        "color": alert_color,
        "advice": advice,
        "factors": factors
    }

def calculate_best_outdoor_window(hourly_aq: Dict[str, Any]) -> Dict[str, Any]:
    """Finds the cleanest 2-to-3 hour window in the next 24 hours based on PM2.5 forecast."""
    times = hourly_aq.get("time", [])
    pm25_series = hourly_aq.get("pm2_5", [])

    if not times or not pm25_series or len(times) < 24:
        return {
            "window_str": "1:00 PM - 3:30 PM",
            "avg_pm25": 45.0,
            "tip": "Afternoon solar peak typically lifts the winter inversion layer."
        }

    # Analyze the first 24 hours
    window_scores = []
    for i in range(len(times[:24]) - 2):
        chunk = pm25_series[i:i+3]
        if all(v is not None for v in chunk):
            avg_pm = sum(chunk) / 3.0
            start_t = times[i].split("T")[-1]
            end_t = times[i+2].split("T")[-1]
            window_scores.append((avg_pm, f"{start_t} - {end_t}", times[i]))

    if not window_scores:
        return {
            "window_str": "1:00 PM - 4:00 PM",
            "avg_pm25": 50.0,
            "tip": "Mid-day warmth provides temporary dispersal relief."
        }

    window_scores.sort(key=lambda x: x[0])
    best = window_scores[0]

    return {
        "window_str": best[1],
        "avg_pm25": round(best[0], 1),
        "start_iso": best[2],
        "tip": f"Projected lowest PM2.5 of the day (~{round(best[0], 1)} µg/m³). Best time for essential school transit, grocery trips, or quick 15-min air flush."
    }

def get_aqi_category(us_aqi: int) -> Dict[str, Any]:
    """Return health category, color, and standard safety precautions for a given US AQI."""
    if us_aqi <= 50:
        return {
            "label": "Good",
            "color": "#10b981",
            "bg": "#d1fae5",
            "badge": "🟢 Good",
            "health_risk": "Low",
            "desc": "Air quality is considered satisfactory, and air pollution poses little or no risk."
        }
    elif us_aqi <= 100:
        return {
            "label": "Moderate",
            "color": "#eab308",
            "bg": "#fef9c3",
            "badge": "🟡 Moderate",
            "health_risk": "Mild",
            "desc": "Acceptable air quality; unusually sensitive people should consider limiting prolonged outdoor exertion."
        }
    elif us_aqi <= 150:
        return {
            "label": "Unhealthy for Sensitive Groups",
            "color": "#f97316",
            "bg": "#ffedd5",
            "badge": "🟠 Sensitive Alert",
            "health_risk": "Moderate",
            "desc": "Children, the elderly, and individuals with respiratory/cardiac disease should reduce prolonged outdoor heavy exertion."
        }
    elif us_aqi <= 200:
        return {
            "label": "Unhealthy",
            "color": "#ef4444",
            "bg": "#fee2e2",
            "badge": "🔴 Unhealthy",
            "health_risk": "High",
            "desc": "Everyone may begin to experience health effects; members of sensitive groups may experience more serious health effects."
        }
    elif us_aqi <= 300:
        return {
            "label": "Very Unhealthy",
            "color": "#a855f7",
            "bg": "#f3e8ff",
            "badge": "🟣 Very Unhealthy",
            "health_risk": "Very High",
            "desc": "Health alert: The risk of health effects is substantially increased for everyone. Avoid outdoor physical activity."
        }
    else:
        return {
            "label": "Hazardous (Severe Smog Emergency)",
            "color": "#881337",
            "bg": "#ffe4e6",
            "badge": "☠️ Hazardous Emergency",
            "health_risk": "Critical / Emergency",
            "desc": "Emergency warning: The entire population is likely to be affected. Close all windows, run DIY/HEPA filters, wear N95 outdoors."
        }

"""
Urban Air Quality Assistant - Community Smog Action Hub
Empowers neighborhoods, housing societies, and community groups to take collective action
against severe winter smog, open biomass burning, and transit emissions.
"""

from typing import Dict, Any, List

COMMUNITY_INITIATIVES = [
    {
        "id": "anti_burning",
        "title": "Community Leaf & Biomass Composting (Stop Open Burning)",
        "badge": "Immediate Smog Prevention",
        "summary": "Eliminate the single largest source of localized evening winter smog spikes.",
        "the_problem": (
            "During winter, sweepers and residents frequently gather fallen dry leaves, dead twigs, and plastic "
            "waste into piles and ignite them. Smoldering wet/dry leaf biomass produces dense plumes of toxic polycyclic "
            "aromatic hydrocarbons (PAH), black carbon, and carbon monoxide. A single 10 kg leaf pile burn produces "
            "the equivalent PM2.5 of driving an old diesel truck for over 400 miles, right under bedroom windows!"
        ),
        "the_solution": [
            "1. Microbial Leaf Trenching: Dig a simple 3x3 ft shallow trench in the community garden. Pack dry leaves into the trench and spray with a natural microbial decomposition solution (or watered-down compost accelerator). Decomposes into rich organic black gold in 4-6 weeks.",
            "2. Shaded Winter Mulching: Scatter crushed leaves around tree bases and flower beds. This locks in winter soil moisture, suppresses weeds, and insulates tree root systems against frost.",
            "3. Security Guard Warming Kit: Security guards often burn waste for warmth during freezing night shifts. Provide the guard post with an energy-efficient ceramic electric heater or a high-grade insulated thermos and thermal jackets to eliminate open night fires."
        ],
        "reporting_template": (
            "URGENT SMOG HAZARD REPORT: Open waste burning observed at [Location / Street Name]. "
            "Open combustion of leaves/waste during winter thermal inversion violates environmental guidelines "
            "and creates severe respiratory hazards for nearby children and seniors. Please dispatch maintenance/enforcement "
            "immediately to douse the fire and provide leaf composting bags."
        )
    },
    {
        "id": "community_air_shelter",
        "title": "Community Clean Air Sanctuary (Clean Bubble)",
        "badge": "Neighborhood Equity",
        "summary": "Turn a local community hall, clubhouse, or library into an emergency clean-air haven.",
        "the_problem": (
            "In severe smog emergencies (AQI > 300), not all community members can afford multiple commercial HEPA "
            "purifiers or have airtight modern homes. Elderly residents, daily wage outdoor workers, and children "
            "are exposed to extreme indoor particulate infiltration."
        ),
        "the_solution": [
            "1. Identify Central Space: Select a communal room (society clubhouse, library reading room, senior center) with solid doors and windows.",
            "2. Deploy 2-3 DIY Corsi-Rosenthal Boxes: With $150 total community funding, install three 4-filter CR boxes. This generates 1,300+ CFM of clean air, easily maintaining <25 µg/m³ PM2.5 in a 1,200 sq ft hall.",
            "3. Setup Work/Study Stations: Allow children to study and remote workers to work in the clean bubble during peak smog days.",
            "4. Free N95 Mask Dispensary: Place a box of certified N95 masks at the entrance for anyone who must commute or work outdoors."
        ],
        "impact_metric": "Maintains an indoor AQI < 50 for up to 60 neighborhood residents simultaneously."
    },
    {
        "id": "school_carpool_rotation",
        "title": "Zero-Idling School Transit & Carpool Rotation",
        "badge": "Child Lung Protection",
        "summary": "Eliminate the morning school gate diesel and gasoline toxic smog cloud.",
        "the_problem": (
            "Between 7:30 AM and 8:30 AM, hundreds of parents arrive at school gates in individual cars, frequently "
            "leaving engines idling while waiting. Because this coincides with the peak morning winter thermal inversion, "
            "tailpipe exhaust cannot rise or disperse. Ground-level NO2 and PM2.5 around school gates frequently spike above 450 µg/m³—exactly "
            "at the height where 6-to-12-year-old children are breathing."
        ),
        "the_solution": [
            "1. 4-Family Carpool Pod: Group 4 neighboring families whose children attend the same school. Rotate driving duties so 1 vehicle replaces 4 daily trips.",
            "2. Strict 'No-Idling' School Zone: Advocate with the school administration to enforce a mandatory engine turn-off rule within 200 meters of the school entrance.",
            "3. Walking School Bus (Cleaner Days): When AQI drops below 100, organize a supervised neighborhood walking group with parents rotating chaperone duties."
        ],
        "impact_metric": "Saves 72% of transit emissions and cuts school gate tailpipe particulate density by over 60%."
    }
]

def get_community_initiatives() -> List[Dict[str, Any]]:
    return COMMUNITY_INITIATIVES

def calculate_carpool_savings(
    num_families: int = 4,
    distance_km_one_way: float = 7.5,
    days_per_month: int = 22
) -> Dict[str, Any]:
    """
    Computes emissions and fuel savings for a school or neighborhood commute carpool pod.
    """
    # Round trip per day per family = distance * 2
    roundtrip_km = distance_km_one_way * 2.0
    
    # Without carpool: each family drives separately
    baseline_km_month = num_families * roundtrip_km * days_per_month
    
    # With carpool: only 1 car drives per day
    carpool_km_month = 1.0 * roundtrip_km * days_per_month
    
    saved_km_month = baseline_km_month - carpool_km_month
    
    # Avg gasoline car emissions ~ 185g CO2 / km, ~ 0.08g PM2.5 / km
    saved_co2_kg = (saved_km_month * 0.185)
    saved_pm25_g = (saved_km_month * 0.08)
    
    # Fuel savings (assumed 12 km/liter at $1.20 / liter)
    saved_liters = saved_km_month / 12.0
    saved_fuel_usd = saved_liters * 1.20
    savings_per_family = saved_fuel_usd / max(num_families, 1)

    return {
        "num_families": num_families,
        "saved_km_month": round(saved_km_month, 0),
        "saved_co2_kg": round(saved_co2_kg, 1),
        "saved_pm25_g": round(saved_pm25_g, 1),
        "saved_liters": round(saved_liters, 1),
        "saved_fuel_usd": round(saved_fuel_usd, 0),
        "savings_per_family_usd": round(savings_per_family, 0)
    }

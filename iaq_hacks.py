"""
Urban Air Quality Assistant - Indoor Air Quality (IAQ) Hacks & Engineering Blueprints
Comprehensive, science-backed indoor pollution mitigation methods.
"""

from typing import List, Dict, Any

IAQ_HACKS_DATABASE = [
    {
        "id": "corsi_rosenthal",
        "title": "DIY Corsi-Rosenthal Clean Air Box",
        "category": "High-Efficiency Filtration",
        "efficacy": "85% - 95% PM2.5 Reduction",
        "cost": "$55 - $75 (vs $400+ Commercial HEPA)",
        "difficulty": "Easy (15 minutes, no tools except duct tape)",
        "summary": "An open-source, scientifically validated air cleaner built with a 20\" box fan and four MERV 13 furnace filters.",
        "why_it_works": (
            "Commercial purifiers have small filter surface areas and loud, restrictive blowers. "
            "A 4-filter Corsi-Rosenthal cube has ~40 square feet of pleated filter media! "
            "This drastically reduces static pressure resistance, allowing a quiet box fan to pump "
            "over 450-600 CFM of purified air—achieving 4 to 6 full air changes per hour (ACH) in typical living spaces."
        ),
        "materials": [
            "1x Standard 20-inch Box Fan ($20-$25)",
            "4x 20x20x2-inch (or 20x20x1-inch) MERV 13 Pleated HVAC Filters ($40-$50 for 4-pack)",
            "1x Heavy-Duty Duct Tape or Gaffer Tape",
            "1x Cardboard Bottom Base (20x20-inch) and Top Shroud (cut from fan shipping box)"
        ],
        "step_by_step": [
            "1. Assemble Filter Cube: Stand the 4 filters in a square on the cardboard base. CRITICAL: Ensure the airflow arrows printed on all 4 filter frames point INWARD toward the center of the box.",
            "2. Tape Seams: Use duct tape to seal all 4 vertical corner joints and tape the bottom edge of all 4 filters to the cardboard base, creating an airtight lower tray.",
            "3. Position Fan: Place the 20-inch box fan on top of the filter cube, facing UPWARDS (blowing clean air toward the ceiling to circulate room air downward through the sides).",
            "4. Tape Fan Perimeter: Thoroughly tape the fan perimeter to the filter tops so no air bypasses the filters.",
            "5. Cut and Install the Secret Weapon (The Cardboard Shroud): Cut a cardboard ring with a 15-inch circular opening and tape it over the front face of the fan. This prevents corner backpressure vortexes and boosts airflow output by +35% to 40%!"
        ],
        "scientific_tip": "Run on Medium speed for whisper-quiet continuous filtration (~42 dB) while maintaining over 400 CFM clean air delivery."
    },
    {
        "id": "inversion_window_flush",
        "title": "Thermal Inversion Window Management Hack",
        "category": "Ventilation Strategy",
        "efficacy": "60% Reduction in Infiltrated Smog",
        "cost": "$0 (Free)",
        "difficulty": "Easy (Schedule Discipline)",
        "summary": "Time your fresh air ventilation strictly to the mid-afternoon solar inversion break.",
        "why_it_works": (
            "During winter nights, the ground rapidly cools, creating a cold boundary layer trapped under "
            "a warmer atmospheric layer above (thermal inversion). Early morning (6:00 AM - 10:00 AM) ground air has the highest "
            "concentration of toxic particulate and soot. Opening windows in the morning fills your home with poison. "
            "Between 1:00 PM and 3:30 PM, solar radiation heats the ground, breaking the inversion and diluting ground pollutants. "
            "A short 12-to-15 minute cross-draft flush during this window expels accumulated indoor carbon dioxide without loading your home with severe smog."
        ),
        "materials": [
            "Timer or smartphone alert set for 1:30 PM",
            "Draft stoppers or rolled towels for base of doors"
        ],
        "step_by_step": [
            "1. Keep all exterior windows and balcony doors sealed tight from 5:00 PM evening until 12:30 PM next afternoon.",
            "2. Check the Urban Air Assistant dashboard at 1:00 PM to verify the mid-day inversion break.",
            "3. Open opposite-facing windows for exactly 10 to 15 minutes to allow cross-ventilation CO2 purge.",
            "4. Seal all windows by 3:30 PM sharp before evening cooling re-establishes the inversion lid.",
            "5. Turn on DIY or HEPA air purifiers immediately after closing windows to rapidly scrub residual incoming particles."
        ],
        "scientific_tip": "Indoor CO2 above 1000 ppm causes brain fog and lethargy; the 1:30 PM flush solves CO2 buildup while preventing winter particulate spikes."
    },
    {
        "id": "kitchen_back_burner",
        "title": "Kitchen Back-Burner & Cooking IAQ Shield",
        "category": "Source Control",
        "efficacy": "Up to 80% Capture of Ultrafine Particles & NO2",
        "cost": "$0 (Free)",
        "difficulty": "Immediate",
        "summary": "Simple cooking layout and exhaust mechanics to eliminate the largest indoor source of NO2 and ultrafine soot.",
        "why_it_works": (
            "Cooking—especially with gas stoves, frying, or searing—generates millions of ultrafine particles (UFP < 100nm) "
            "and nitrogen dioxide (NO2) levels that often exceed WHO outdoor air quality limits by 300%. "
            "Most overhead exhaust range hoods only overhang the rear burners properly. "
            "Fluid dynamic tests prove cooking on back burners captures 75-85% of emissions compared to only 40-50% on front burners."
        ),
        "materials": [
            "Pot lids for frying and boiling",
            "Exhaust hood or window exhaust fan"
        ],
        "step_by_step": [
            "1. Always turn the range hood exhaust on HIGH 1 minute BEFORE striking the flame or heating the pan.",
            "2. Shift frying, searing, and boiling to the REAR BURNERS directly under the exhaust hood intake.",
            "3. Keep lids on pots whenever possible; this cuts volatile aerosol emissions by 65%.",
            "4. Leave the kitchen exhaust fan running for 10 minutes AFTER cooking finishes to clear lingering ultrafine particles.",
            "5. Keep kitchen doors closed to prevent cooking aerosols from migrating into bedrooms and nursery spaces."
        ],
        "scientific_tip": "If replacing appliances, an electric induction cooktop produces ZERO combustion gases (no NO2, no CO) and reduces indoor PM by over 90%."
    },
    {
        "id": "microfiber_wet_mop",
        "title": "Microfiber Damp-Mopping vs Broom Sweeping",
        "category": "Surface Particulate Control",
        "efficacy": "Stops 90% of Toxic Particle Resuspension",
        "cost": "$5 - $10",
        "difficulty": "Easy",
        "summary": "Never use dry brooms or non-HEPA vacuums during winter smog; damp mopping locks particles down.",
        "why_it_works": (
            "Heavy particles (heavy metals, brake dust, road soot) settle onto floors. "
            "Using a standard dry broom or a cheap vacuum without a certified sealed HEPA exhaust acts like an aerosol blower: "
            "it re-suspends settled PM10 and PM2.5 right into your breathing zone (and child crawling zones) for 2 to 4 hours. "
            "A damp electrostatic microfiber mop captures and traps particles without re-aerosolizing them."
        ),
        "materials": [
            "Electrostatic microfiber flat mop",
            "Warm water with mild soap / white vinegar (no toxic artificial chemical fragrances)"
        ],
        "step_by_step": [
            "1. Establish a strict 'Shoes-Off at the Door' quarantine zone. A dual walk-off doormat system traps 85% of street soot outside.",
            "2. Dampen a clean microfiber mop head with warm water until barely moist (not dripping).",
            "3. Mop floors in smooth, single-direction S-strokes without vigorous scrubbing.",
            "4. Rinse the mop pad in a bucket after each room to permanently flush captured toxic particulates down the drain.",
            "5. If using a vacuum cleaner, verify it features a sealed True-HEPA system with rubber gaskets."
        ],
        "scientific_tip": "Toddlers breathe 3x more floor-level resuspended dust per kilogram of body weight than adults."
    },
    {
        "id": "humidity_mucosa_shield",
        "title": "40-50% Relative Humidity Mucosal Shield",
        "category": "Respiratory Defense",
        "efficacy": "Protects Lung Ciliary Clearance by 300%",
        "cost": "$0 - $30",
        "difficulty": "Easy",
        "summary": "Maintain indoor humidity at 40-50% to prevent respiratory mucus desiccation in dry winter smog.",
        "why_it_works": (
            "Winter cold air holds very little moisture. When outdoor air is heated indoors, relative humidity often plunges below 25%. "
            "In dry air, your respiratory mucous membranes dry out, paralyzing the microscopic cilia that sweep PM2.5 and bacteria out of your airways. "
            "Keeping indoor humidity between 40% and 50% preserves your natural lung defense mechanisms."
        ),
        "materials": [
            "Digital hygrometer ($6-$10)",
            "Radiator water trays, shallow ceramic bowls of water, or evaporative humidifier"
        ],
        "step_by_step": [
            "1. Place a digital hygrometer in the living room and bedrooms to monitor relative humidity.",
            "2. Place shallow stainless steel or ceramic bowls of clean water atop warm radiators or near heat vents.",
            "3. If using an ultrasonic humidifier, ALWAYS use distilled or reverse-osmosis (RO) water; tap water minerals are aerosolized into harmful white dust (mineral PM2.5).",
            "4. Target 40% to 50% relative humidity; avoid exceeding 55% to prevent mold spore propagation."
        ],
        "scientific_tip": "A simple bowl of water on a radiator evaporates ~1.5 liters of clean vapor daily with zero electricity cost."
    },
    {
        "id": "scented_hazard_elimination",
        "title": "Banish Indoor Incense, Candles & Chemical Fresheners",
        "category": "Indoor Chemical Toxins",
        "efficacy": "Eliminates Dangerous Indoor VOC & Benzene Spikes",
        "cost": "$0 (Saves Money)",
        "difficulty": "Immediate",
        "summary": "Avoid adding synthetic indoor pollutants when outdoor air is already toxic.",
        "why_it_works": (
            "Burning a single incense stick or paraffin candle releases as much benzene, formaldehyde, and soot "
            "as idling a small combustion engine in an enclosed room. "
            "Synthetic plug-in air fresheners emit terpenes and phthalates that react with indoor ozone to form toxic secondary organic aerosols (SOA). "
            "Clean air smells like NOTHING, not artificial lavender."
        ),
        "materials": [
            "Pot of water with cinnamon sticks, citrus peels, and cloves (simmer pot alternative)"
        ],
        "step_by_step": [
            "1. Discontinue burning incense sticks, mosquito coils, and paraffin candles in enclosed winter spaces.",
            "2. Unplug chemical wall plug-ins and aerosol room sprays.",
            "3. For pleasant natural scents without combustion toxins, simmer a pot of water on the stove with orange peels and cinnamon for 15 minutes."
        ],
        "scientific_tip": "Mosquito coils emit the PM2.5 equivalent of 75 to 137 burning cigarettes; switch to electrical liquid vaporizers or sealed window mesh screens."
    }
]

def get_all_hacks() -> List[Dict[str, Any]]:
    return IAQ_HACKS_DATABASE

def get_hack_by_id(hack_id: str) -> Dict[str, Any]:
    for hack in IAQ_HACKS_DATABASE:
        if hack["id"] == hack_id:
            return hack
    return IAQ_HACKS_DATABASE[0]

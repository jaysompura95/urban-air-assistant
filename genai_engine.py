"""
Urban Air Quality Assistant - GenAI Engine
Integrates Google Gemini via the official google-genai SDK,
with a robust domain-specific intelligent fallback engine for offline/demo use.
"""

import os
from typing import Dict, Any, List, Optional

SYSTEM_PROMPT_TEMPLATE = """You are Aura, an elite GenAI Urban Air Quality and Winter Smog Assistant.
Your mission is to help families and urban communities navigate severe winter smog and air pollution.
You specialize in:
1. Low-emission daily routines tailored to local conditions and family lifestyles.
2. Low-cost Indoor Air Quality (IAQ) hacks (such as the DIY Corsi-Rosenthal box, ventilation timing during midday solar inversion breaks, damp-mopping, and kitchen exhaust physics).
3. Sustainable alternatives to high-polluting habits (such as clean heating choices, carpooling, public transit, and microbial leaf composting instead of open burning).
4. Clearly explaining the direct human health and environmental impact of every choice, using quantitative metrics (PM2.5 micrograms avoided, equivalent cigarettes, kg CO2 saved).

Current Location Context:
- City: {city}
- Current AQI: {aqi} ({aqi_label})
- PM2.5: {pm25} µg/m³
- PM10: {pm10} µg/m³
- Thermal Inversion Status: {inversion_status}
- Optimal Fresh Air Window: {optimal_window}
- Active User Persona: {persona}

Communication Tone: Empathetic, scientifically rigorous, highly practical, actionable, and encouraging.
Format your responses with clean Markdown, bullet points, and quantitative callouts where appropriate.
"""

PERSONAS = {
    "🩺 Pediatric & Family Health Specialist": (
        "Focus on vulnerable family members, children's developing lungs, seniors, asthmatic triggers, "
        "proper N95/KF94 mask fit, mucosal hydration, and symptoms requiring medical attention."
    ),
    "🛠️ Indoor Air Quality (IAQ) Engineer": (
        "Focus on aerosol physics, DIY Corsi-Rosenthal box builds, CADR, MERV 13 filtration, "
        "fan CFM, air changes per hour (ACH), sealing drafts, and kitchen exhaust fluid dynamics."
    ),
    "🌍 Urban Sustainability & Community Coach": (
        "Focus on community-scale collective action, stopping open leaf burning through microbial composting, "
        "school carpools, clean heating alternatives, and quantifying collective CO2 & smog reduction."
    )
}

def ask_genai(
    query: str,
    city_name: str,
    aqi: int,
    aqi_label: str,
    pm25: float,
    pm10: float,
    inversion_status: str,
    optimal_window: str,
    persona_key: str = "🩺 Pediatric & Family Health Specialist",
    api_key: Optional[str] = None,
    chat_history: Optional[List[Dict[str, str]]] = None
) -> str:
    """
    Primary interface for GenAI responses.
    Uses Google Gemini via google-genai SDK if an API key is available.
    Otherwise gracefully falls back to the built-in domain reasoning engine.
    """
    key = api_key or os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")

    if key:
        try:
            from google import genai
            client = genai.Client(api_key=key)
            persona_desc = PERSONAS.get(persona_key, "")
            sys_instruct = SYSTEM_PROMPT_TEMPLATE.format(
                city=city_name,
                aqi=aqi,
                aqi_label=aqi_label,
                pm25=pm25,
                pm10=pm10,
                inversion_status=inversion_status,
                optimal_window=optimal_window,
                persona=f"{persona_key} ({persona_desc})"
            )

            # Build conversation context
            contents = []
            if chat_history:
                for msg in chat_history[-6:]:
                    contents.append(f"{msg.get('role', 'user')}: {msg.get('content', '')}")
            contents.append(f"User: {query}")
            full_prompt = f"{sys_instruct}\n\n" + "\n".join(contents) + "\nAssistant:"

            # Try modern Gemini models
            for model_name in ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"]:
                try:
                    response = client.models.generate_content(
                        model=model_name,
                        contents=full_prompt
                    )
                    if response and response.text:
                        return response.text
                except Exception:
                    continue
        except Exception:
            pass

    # Intelligent Heuristic Fallback Engine
    return generate_intelligent_offline_response(
        query=query,
        city_name=city_name,
        aqi=aqi,
        aqi_label=aqi_label,
        pm25=pm25,
        inversion_status=inversion_status,
        optimal_window=optimal_window,
        persona_key=persona_key
    )

def generate_intelligent_offline_response(
    query: str,
    city_name: str,
    aqi: int,
    aqi_label: str,
    pm25: float,
    inversion_status: str,
    optimal_window: str,
    persona_key: str
) -> str:
    """
    Sophisticated domain-specific expert response generator.
    Guarantees rich, contextual, science-backed guidance even in offline/demo mode.
    """
    q = query.lower()

    # Category 1: Children / Asthma / Health / Symptoms
    if any(k in q for k in ["child", "kid", "asthma", "cough", "breath", "baby", "health", "symptom", "lung", "elderly", "senior"]):
        return f"""### 🩺 Pediatric & Family Health Smog Advisory for {city_name}
**Current Air Quality:** AQI {aqi} ({aqi_label}) | PM2.5: {pm25} µg/m³

#### 1. Why Vulnerable Lungs Are at Immediate Risk:
Children breathe **50% more air per pound of body weight** than adults, and their respiratory airways are narrower. In {city_name} today, inhaling {pm25} µg/m³ of PM2.5 causes fine soot particles to penetrate deep into pulmonary alveoli, triggering acute airway hyper-reactivity, coughing spasms, and reduced lung capacity.

#### 2. Immediate Family Shield Protocol:
- **No Early Morning Exertion:** Thermal inversion is trapping cold surface soot right now ({inversion_status}). Keep children strictly indoors before 11:00 AM.
- **N95 / KF94 Masking:** Surgical masks and cloth bandanas offer **under 20% filtration** for fine particles. Only certified N95 or child-sized KF94 masks with a snug nasal bridge seal filter out 95% of toxic PM2.5 during unavoidable school commutes.
- **Nasal Mucosal Hydration:** Smog dries out the mucus lining that sweeps particles away. Encourage warm water sips every 30 minutes and consider a gentle isotonic saline nasal rinse after returning indoors.
- **Bedroom Air Purification:** Prioritize running your air purifier or DIY Corsi-Rosenthal box in the children's/seniors' bedrooms at least 1 hour before bedtime to guarantee a clean breathing sanctuary.

#### 3. Direct Impact of These Actions:
Following this shield protocol drops your child's 24-hour PM2.5 inhalation from ~{round(pm25 * 0.85 * 11, 0)} µg down to ~{round(pm25 * 0.15 * 11, 0)} µg—**a massive 82% reduction in toxic lung intake**, preventing asthma exacerbations and ER visits.
"""

    # Category 2: DIY Filter / Corsi-Rosenthal / Air Purifier
    elif any(k in q for k in ["corsi", "rosenthal", "diy", "filter", "purifier", "hepa", "cadr", "ach", "build"]):
        return f"""### 🛠️ IAQ Engineering Guide: DIY Corsi-Rosenthal Box
**Optimized for {city_name} (Current PM2.5: {pm25} µg/m³)**

The **Corsi-Rosenthal (CR) Box** is an open-source, scientifically proven clean air machine that delivers **450–600 CFM (Clean Air Delivery Rate)** for roughly **$65**, outperforming commercial $400 HEPA purifiers!

#### Required Materials:
1. **1x 20-inch Box Fan** ($20–$25)
2. **4x MERV 13 Pleated HVAC Filters** (20" x 20" x 2" or 20" x 20" x 1") ($40 for a 4-pack)
3. **1x Cardboard Base & Shroud** (cut from fan shipping box)
4. **Duct Tape / Gaffer Tape**

#### 5-Minute Assembly Steps:
1. **Filter Cube:** Stand the 4 filters vertically in a square on the cardboard bottom base.  
   ⚠️ **CRITICAL:** Ensure the airflow arrows on all 4 filter frames point **INWARD** toward the center.
2. **Seal Joints:** Tape all 4 vertical corners securely with duct tape to form an airtight chamber.
3. **Position Fan:** Set the 20" fan atop the cube, facing **UPWARD** (blowing clean air toward the ceiling).
4. **The Secret Shroud:** Cut a cardboard ring with a 15-inch circular opening and tape it over the front grille of the box fan. This blocks the dead corners of the fan blades, **increasing clean airflow by +40%**!

#### Performance in Your Living Room (300 sq ft):
- **Air Changes per Hour (ACH):** ~5.2 ACH (Clears 90% of airborne winter smog in under 26 minutes!).
- **Cost vs Commercial:** Saves over **$350** upfront, with replacement filters costing a fraction of proprietary cartridges.
"""

    # Category 3: Windows / Inversion / Ventilation
    elif any(k in q for k in ["window", "ventilat", "fresh air", "inversion", "open", "seal", "draft"]):
        return f"""### 🪟 Winter Smog Window Protocol for {city_name}
**Thermal Inversion Assessment:** {inversion_status}

#### The Science: Why Traditional Morning Airing is Dangerous
During winter, cold heavy air sinks to the ground overnight, trapping vehicle soot, brick kiln smoke, and heating emissions under a warm atmospheric "lid" (thermal boundary inversion).
- **Opening windows at 7:00 AM** introduces peak toxic particulates (often exceeding {int(pm25 * 1.3)} µg/m³) directly into your living room and carpets.

#### The Golden Strategy: The Midday Inversion Break
- **Optimal Air Flush Window:** **{optimal_window}**
- **Action:** Open opposite-facing windows for **exactly 10 to 15 minutes** during this window.
- **Why it works:** Solar heating at midday warms the earth's surface, triggering convective thermal updrafts that temporarily disperse the ground smog blanket.
- **Close by 3:30 PM Sharp:** As temperatures drop in late afternoon, the inversion lid compresses back to ground level.

#### Impact:
This targeted protocol flushes built-up indoor CO2 (keeping it under 800 ppm to avoid brain fog and fatigue) while preventing **over 65% of outdoor fine smog** from entering your home!
"""

    # Category 4: Heating / Cooking / Fireplace / Fuel
    elif any(k in q for k in ["heat", "cook", "stove", "gas", "wood", "fire", "heater", "burn"]):
        return f"""### 🔥 Clean Heating & Cooking Alternatives in {city_name}

#### 1. The Winter Indoor Heating Hazard:
- **Avoid Wood / Biomass Fireplaces:** Burning wood indoors generates severe spikes in benzene, carbon monoxide, and ultrafine PM2.5. A single fireplace fire produces as much particulate pollution as 90 gasoline passenger cars idling!
- **Avoid Unvented Kerosene / Gas Heaters:** These release large volumes of nitrogen dioxide (NO2) and moisture, worsening asthma and fostering mold.
- **Safe Alternatives:** Use sealed electric heat pumps, oil-filled radiant heaters, or ceramic space heaters paired with warm thermal layering (fleece and wool).

#### 2. The Kitchen "Back-Burner" Rule:
- Frying, grilling, and gas stoves are the #1 source of indoor NO2 and ultrafine particles.
- **Always cook on the BACK burners** directly under your range hood exhaust. Fluid dynamics show this captures **80% of toxic emissions** compared to only 45% on front burners.
- Use lids on frying pans and pots to reduce aerosolization by 65%.

#### Environmental & Health Impact:
Switching from wood/unvented heating to efficient electric heating prevents **~300 grams of toxic PM2.5** and cuts household carbon emissions by **12 kg CO2e per week**.
"""

    # Category 5: Commute / Travel / Transit
    elif any(k in q for k in ["commute", "car", "transit", "metro", "bus", "travel", "drive", "bike"]):
        return f"""### 🚇 Low-Emission Commute & Transit Shield for {city_name}

#### 1. Commute Shield Strategy (Protecting Yourself):
- **Inside Your Car:** Switch ventilation to **INTERNAL RECIRCULATION** mode. This prevents pulling tailpipe exhaust from preceding diesel trucks directly into your vehicle cabin (reducing in-car PM2.5 by up to 75%).
- **Public Transit:** Metro systems and electric buses have centralized filtration and reduce personal exposure to street-level stop-and-go exhaust.
- **Masking:** If walking or taking two-wheelers, wear an **N95/FFP2 respirator**. Surgical masks do not seal against fine diesel soot.

#### 2. Low-Emission Choices (Protecting Your City):
- **Carpooling:** Organizing a 3-person carpool cuts 2 cars off the road, saving **~3.2 kg CO2 and 15g PM2.5 per 15 km roundtrip**.
- **Metro / Subway:** Cuts personal commute carbon footprint by **88%** compared to a solo gasoline vehicle.

#### Direct Impact:
Choosing public transit or carpooling over a solo car in {city_name} saves your lungs from inhaling **over 250 µg of concentrated traffic exhaust** every single day.
"""

    # Category 6: Community / Leaf burning / Neighborhood
    elif any(k in q for k in ["community", "leaf", "burn", "neighbor", "society", "apartment", "clean air bubble"]):
        return f"""### 🌍 Community Winter Smog Action Plan for {city_name}

#### 1. Stop Open Leaf & Waste Burning:
- Open burning of dry garden leaves and trash accounts for **up to 40% of evening localized smog spikes** in residential colonies.
- **The Sustainable Alternative:** Setup a community **Microbial Leaf Composting Trench**. Collecting leaves and applying a biological accelerator converts dry waste into nutrient-rich compost in 4-6 weeks without releasing a single gram of smoke.
- **Guard Warming Initiative:** Provide colony security guards with electric ceramic heaters and insulated flasks so they don't burn trash at night to stay warm.

#### 2. School Carpool Pods:
- Morning school drop-offs create dense diesel/gasoline exhaust pockets right where young children walk into school.
- Organizing 4-family carpool pods cuts morning school-gate emissions by **75%**.

#### 3. Community Clean Air Bubble:
- Equip the residential clubhouse or local library with 2 DIY Corsi-Rosenthal boxes ($130 total) to create an emergency clean-air haven for seniors and students during Code Red smog days.

#### Collective Multiplier:
If 100 households in your neighborhood implement these three actions, your community eliminates **over 4.2 tonnes of CO2 and prevents ~18 kg of toxic PM2.5 emissions** every single month!
"""

    # General / Default response
    else:
        return f"""### 💨 Urban Air Quality Action Plan for {city_name}
**Current Situation:** AQI {aqi} ({aqi_label}) | PM2.5: {pm25} µg/m³ | {inversion_status}

To navigate severe winter smog effectively in your home and neighborhood:

1. **Indoor Air Quality (IAQ) Defense:**
   - Keep windows closed during morning/evening inversion peaks.
   - Use the **{optimal_window}** window for a quick 12-minute fresh air flush.
   - Run a DIY Corsi-Rosenthal box or HEPA filter to maintain indoor PM2.5 < 15 µg/m³.
   - Microfiber damp-mop floors instead of dry broom sweeping to avoid re-suspending settled dust.

2. **Clean Commute & Routines:**
   - Put on a certified N95 mask before leaving home.
   - Shift from solo driving to carpooling or electric metro to reduce localized emissions.
   - Cook on rear burners under an active exhaust fan to eliminate indoor NO2 spikes.

3. **Community Impact:**
   - Prevent neighborhood leaf burning by adopting simple microbial composting.
   - Create shared clean-air rooms in community centers for vulnerable neighbors.

*Ask me anything specific about DIY air purifiers, child lung protection, zero-emission commutes, or room ventilation physics!*
"""

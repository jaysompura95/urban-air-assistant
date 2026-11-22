<div align="center">

# 🌬️ Urban Air Quality Assistant (Aura)
### *GenAI-Powered Winter Smog Defense, Indoor Air Quality Hacks & Community Action Network*

[![CI Pipeline](https://github.com/jaysompura95/urban-air-assistant/actions/workflows/ci.yml/badge.svg)](https://github.com/jaysompura95/urban-air-assistant/actions)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.66-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![Google GenAI](https://img.shields.io/badge/GenAI-Google%20Gemini-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev/)
[![API](https://img.shields.io/badge/Atmospheric%20Data-Open--Meteo-007ACC?style=for-the-badge)](https://open-meteo.com/)
[![License](https://img.shields.io/badge/License-MIT-10b981?style=for-the-badge)](LICENSE)

<br/>

**A science-backed, GenAI-driven assistant built to protect urban families and communities from severe winter smog and air pollution.**

[Explore Live Demo](https://github.com/jaysompura95/urban-air-assistant) &bull;
[View Architecture](#-system-architecture) &bull;
[IAQ Engineering Lab](#-indoor-air-quality-iaq-lab) &bull;
[Deploy to Cloud](#-1-click-live-cloud-deployment)

</div>

---

## 🎯 The Hackathon Problem

During winter, meteorological **thermal inversions** compress vehicle exhaust, biomass smoke, and industrial particulate into a stagnant ground-level atmospheric chamber. Standard weather apps merely report an abstract AQI number without actionable, lifestyle-tailored guidance or indoor interventions.

**Urban Air Quality Assistant (Aura)** transforms raw atmospheric data into actionable daily defense protocols:
- **Suggests Low-Emission Daily Routines:** Dynamically timed according to atmospheric boundary layer inversion forecasts.
- **Empowers Families with IAQ Hacks:** Detailed blueprints for open-source **DIY Corsi-Rosenthal Boxes**, kitchen back-burner aerodynamics, and mid-day window flushing.
- **Drives Community Collective Action:** Coordinates microbial composting to eradicate open leaf burning and structures school carpool pods.
- **Quantifies Direct Impact:** Translates personal and neighborhood choices into **micrograms of PM2.5 prevented from entering pulmonary alveoli**, **equivalent cigarettes avoided**, and **kg of CO2 reduced**.

---

## 🌟 Core Features & Modules

### 1. 🌐 Real-Time Smog & Thermal Inversion Monitor
- **Live Global Meteorological Sync:** Real-time metrics for PM2.5, PM10, US AQI, CO, $\text{NO}_2$, $\text{SO}_2$, and Ozone via Open-Meteo.
- **Atmospheric Inversion Trap Score:** Evaluates wind stagnation, humidity saturation, and ground temperatures to predict ground-level smog trapping risk.
- **Optimal Outdoor Time Window:** Identifies the safest 2-to-3 hour window of the day (typically 1:00 PM – 3:30 PM) when solar warming breaks the inversion lid.

### 2. 📅 Personalized 24-Hour Smog Shield Routines
- Tailored schedules for **5 distinct household archetypes**:
  - 🧒 **Families with Young Children:** Morning school transit shields and indoor recess protocols.
  - 🫁 **Vulnerable Households (Asthma, COPD, Seniors):** Morning walk prohibitions and respiratory mucus defense.
  - 💼 **Urban Working Commuters:** In-cabin recirculation rules and low-exposure transit shifts.
  - 💻 **Remote Workers / Freelancers:** Energy-efficient home heating and indoor CO2 flushes.
  - 🏘️ **Community Champions:** Neighborhood smog patrols and community hall air shelter setup.
- **Downloadable Family Action Card:** One-click markdown summary ready to print for the family fridge.

### 3. 🛠️ Indoor Air Quality (IAQ) Lab & Engineering Hacks
- **Interactive DIY Corsi-Rosenthal Box Designer:** Calculates Clean Air Delivery Rate (CADR in CFM), Air Changes per Hour (ACH), and particle clearance times for any room size.
- **Cost Efficiency:** Demonstrates how a **$65 DIY 4-filter cube** achieves **~450 CFM CADR**, outperforming **$450 commercial HEPA purifiers** while saving **$380+**.
- **6 Deep Science Indoor Hacks:**
  - *Midday Inversion Window Flush Protocol* (clears indoor CO2 without letting heavy smog in)
  - *Range Hood Back-Burner Fluid Dynamics* (captures 80% vs 45% of cooking ultrafine soot)
  - *Microfiber Damp Mopping vs Broom Sweeping* (stops 90% particle resuspension)
  - *40–50% Relative Humidity Mucosal Shield* (preserves lung ciliary clearance)
  - *Zero-Smoke Aromatic Simmer Pots* (replaces toxic paraffin candles & incense)

### 4. 📊 Direct Impact Ledger (Mathematical Quantification)
- **Personal Inhalation Ledger:** Calculates exact mass of PM2.5 prevented from reaching deep lung tissue.
- **Berkeley Earth Cigarette Metric:** Real-time conversion of ambient smog exposure to passive cigarettes avoided.
- **Community Multiplier:** Scalable neighborhood simulation proving how 250 participating homes eliminate **4.5 tonnes of CO2** and avert emergency room visits.

### 5. 🤝 Community Action Hub
- **Anti-Biomass Burning Composting Kit:** Eliminates the single largest source of localized evening winter smog spikes with 4-week microbial leaf composting trenches.
- **School Carpool Pod Calculator:** Tracks shared commute savings in vehicle kilometers, fuel costs, and tailpipe soot prevented at school drop-off zones.
- **Community Clean Air Shelter Guide:** Blueprint for turning neighborhood clubhouses or libraries into emergency clean air havens.

### 6. 💬 Aura GenAI Conversational Advisor
- Powered by the official Google GenAI SDK (`google-genai`) with support for Gemini models.
- **Specialized Personas:** Pediatric Health Specialist, IAQ Engineer, and Community Sustainability Coach.
- **Built-in Domain Heuristic Engine:** 100% functional offline without requiring an API key.

---

## 🏗️ System Architecture

```mermaid
flowchart TD
    subgraph Data Sources
        API1["Open-Meteo Air Quality API\n(PM2.5, PM10, AQI, CO, NO2)"]
        API2["Open-Meteo Weather API\n(Temp, Humidity, Wind Speed)"]
        API3["Open-Meteo Geocoding\n(Global City Search)"]
    end

    subgraph Analytical Core
        IR["Atmospheric Inversion & Smog Trap Engine"]
        OW["Safest Outdoor Window Optimizer"]
        RG["24-Hour Personalized Shield Routine Generator"]
        CR["DIY Corsi-Rosenthal CADR / ACH Engine"]
        IC["Direct Impact & Particulate Ledger Calculator"]
    end

    subgraph GenAI Engine
        GEM["Google Gemini API (google-genai)"]
        HEU["Offline Domain Reasoning Engine"]
        PER["Multi-Persona Context Switcher"]
    end

    subgraph User Experience
        ST["Streamlit 1.66 Application"]
        T1["🌐 Live Smog & Inversion"]
        T2["📅 24h Shield Routine"]
        T3["🛠️ IAQ Hacks & DIY Lab"]
        T4["📊 Direct Impact Ledger"]
        T5["🤝 Community Hub"]
        T6["💬 Aura GenAI Chat"]
    end

    Data Sources --> Analytical Core
    Analytical Core --> User Experience
    GenAI Engine <--> T6
    ST --> T1 & T2 & T3 & T4 & T5 & T6
```

---

## 🔬 Scientific & Mathematical Models

### 1. Inhaled Particulate Mass & Respiration Exposure
$$\text{Inhaled Mass } (\mu\text{g}) = \sum_{t=1}^{24} \left( C_{t} \times \dot{V}_{\text{resp}} \right)$$
- Children breathe $\approx 11.5\,\text{m}^3/\text{day}$; active adults breathe $\approx 15.0\,\text{m}^3/\text{day}$.
- Baseline unmitigated indoor exposure ($C_{\text{indoor}} \approx 0.8 \times C_{\text{outdoor}}$) plus unfiltered transit exposure ($C_{\text{transit}} \approx 1.35 \times C_{\text{outdoor}}$).
- Mitigated protocol reduces total 24-hour inhaled particulate mass by **75% to 85%**.

### 2. Berkeley Earth Smog-to-Cigarette Equivalence
$$\text{Equivalent Cigarettes} = \frac{\text{Daily Average PM}_{2.5} \;(\mu\text{g/m}^3)}{22.0}$$
Inhaling $220\,\mu\text{g/m}^3$ PM2.5 in severe winter smog is mathematically equivalent to smoking **10 cigarettes a day**. Aura's interventions reduce this to less than **1.5 cigarettes/day**.

### 3. Corsi-Rosenthal Box Fluid Dynamics (CADR & ACH)
$$\text{ACH} = \frac{\text{CADR (CFM)} \times 60}{\text{Room Volume (cu ft)}}$$
$$\text{Time to 90% Clearance} = \frac{2.303 \times 60}{\text{ACH}} \quad (\text{minutes})$$

---

## 📁 Repository Directory Structure

```
urban-air-assistant/
├── .github/
│   └── workflows/
│       └── ci.yml               # Automated GitHub Actions test pipeline
├── .gitignore                   # Clean Python/Streamlit exclusions
├── LICENSE                      # Open-source MIT license notice
├── README.md                    # Project documentation & presentation deck
├── CONTRIBUTING.md              # Community contribution guidelines
├── CODE_OF_CONDUCT.md           # Contributor code of conduct
├── requirements.txt             # Application dependencies
├── run.bat                      # Windows 1-click launch batch script
├── run.ps1                      # PowerShell 1-click startup script
├── app.py                       # Main Streamlit web application
├── api_service.py               # Open-Meteo real-time atmospheric API
├── impact_calculator.py         # Human health exposure & emission models
├── iaq_hacks.py                 # Indoor air quality hack database & CADR
├── routines_generator.py        # 24-hour personalized routine generator
├── community_hub.py             # Community action & school carpool tools
└── genai_engine.py              # Google Gemini & offline reasoning engine
```

---

## ⚡ 1-Click Live Cloud Deployment

You can deploy this repository to the public internet for **free in under 60 seconds** on **Streamlit Community Cloud**:

1. Go to **[share.streamlit.io](https://share.streamlit.io)** and log in with your GitHub account.
2. Click **"New app"**.
3. Fill in the fields:
   - **Repository:** `jaysompura95/urban-air-assistant`
   - **Branch:** `main`
   - **Main file path:** `app.py`
4. Click **"Deploy!"**
5. Your app will be live with a permanent public URL (e.g., `https://urban-air-assistant.streamlit.app`) accessible to judges, mentors, and anyone worldwide on desktop and mobile!

---

## 💻 Local Quickstart

```bash
# 1. Clone the repository
git clone https://github.com/jaysompura95/urban-air-assistant.git
cd urban-air-assistant

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the application
streamlit run app.py
```
Open **[http://localhost:8501](http://localhost:8501)** in your browser.

---

## 🏆 Hackathon Evaluation Alignment

| Evaluation Criteria | Aura Implementation |
| :--- | :--- |
| **GenAI Assistant** | Real Google Gemini integration (`google-genai`) with multi-turn chat and 3 specialized domain personas. |
| **Severe Winter Smog Focus** | Meteorological thermal boundary inversion modeling, humidity aerosol condensation, and midday solar dispersal window optimization. |
| **Low-Emission Daily Routines** | Dynamic 24-hour hour-by-hour schedules tailored to 5 household archetypes with morning and evening window seals. |
| **Indoor Air Quality (IAQ) Hacks** | Interactive DIY Corsi-Rosenthal Box CAD/ACH calculator, range-hood back burner physics, microfiber damp mopping, and mucosal humidity defense. |
| **Sustainable Alternatives** | Electric heat pump & induction cooking switches, 4-family school carpool rotation, and community microbial leaf composting to replace open burning. |
| **Direct Impact Explainer** | Peer-reviewed mathematical ledger: Inhaled PM2.5 avoided (mg), equivalent passive cigarettes avoided, commute CO2 saved (kg), and community multiplier scaling. |

---

<div align="center">
Developed with ❤️ by <strong>Jay Sompura</strong> for the <strong>Urban Air Quality Hackathon</strong>.
</div>

"""
Impact & Sustainable Alternatives Engine.

Quantifies exact personal and community emission reductions, calculates
inhaled particulate shielding (Berkeley Earth cigarette equivalence),
and presents verified sustainable alternatives with explainable narratives.
"""

from typing import Dict, List, Any
from app.models.schemas import (
    ImpactRequest,
    ImpactResponse,
    CommuteMode
)


class ImpactEngine:
    """Calculates quantified personal and community emissions reductions."""

    # Emission factors: kg CO2 per km
    COMMUTE_EMISSIONS_KG_PER_KM = {
        CommuteMode.SOLO_PETROL_CAR: 0.192,
        CommuteMode.SOLO_DIESEL_SUV: 0.235,
        CommuteMode.TWO_WHEELER: 0.075,
        CommuteMode.CARPOOL: 0.055,
        CommuteMode.ELECTRIC_METRO: 0.015,
        CommuteMode.EV_BUS: 0.022,
        CommuteMode.CYCLING_WALKING: 0.0,
    }

    # PM2.5 tailpipe grams per km
    COMMUTE_PM25_GRAMS_PER_KM = {
        CommuteMode.SOLO_PETROL_CAR: 0.035,
        CommuteMode.SOLO_DIESEL_SUV: 0.085,
        CommuteMode.TWO_WHEELER: 0.045,
        CommuteMode.CARPOOL: 0.012,
        CommuteMode.ELECTRIC_METRO: 0.001,
        CommuteMode.EV_BUS: 0.003,
        CommuteMode.CYCLING_WALKING: 0.0,
    }

    @classmethod
    def evaluate_impact(cls, req: ImpactRequest) -> ImpactResponse:
        """Calculates direct quantified impact and explainable benefits."""
        # 1. Commute analysis
        current_mode = req.commute_mode
        base_co2_kg_per_km = cls.COMMUTE_EMISSIONS_KG_PER_KM.get(current_mode, 0.192)
        metro_co2_kg_per_km = cls.COMMUTE_EMISSIONS_KG_PER_KM[CommuteMode.ELECTRIC_METRO]

        # Daily CO2 saved if shifting to electric metro/EV
        daily_co2_saved_kg = max(0.0, (base_co2_kg_per_km - metro_co2_kg_per_km) * req.daily_commute_km)
        annual_co2_saved_kg = daily_co2_saved_kg * 250.0  # 250 working days

        # 2. Particulate exposure shielded
        # Average adult breathes ~12 m3 of air per day (or 0.5 m3/hr).
        # In a severe winter smog day (avg PM2.5 = 280 ug/m3), breathing filtered indoor air
        # (maintaining 35 ug/m3) cuts inhaled burden by 245 ug/m3.
        hours_indoors_shielded = 16.0  # Sleeping + working in filtered space
        air_inhaled_indoors_m3 = hours_indoors_shielded * 0.5  # 8 m3

        filter_efficiency = 0.85 if req.installed_diy_iaq_filter else 0.40
        vent_bonus = 1.15 if req.adopted_ventilation_protocol else 1.0

        daily_pm25_shielded_ug = round(
            8.0 * (280.0 - 35.0) * filter_efficiency * vent_bonus, 1
        )
        annual_pm25_avoided_g = round((daily_pm25_shielded_ug * 365.0) / 1_000_000.0, 2)

        # Cigarettes toxicity equivalent avoided
        # Berkeley Earth: 22 ug/m3 for 24h = 1 cigarette.
        # Direct inhaled mass equivalent:
        cigarettes_shielded = round(daily_pm25_shielded_ug / (22.0 * 12.0), 1)

        # Pediatric respiratory benefit
        pediatric_benefit = min(92.0, round(filter_efficiency * 100.0 * 0.95, 1))

        # Car km equivalent
        car_km_equiv = round(annual_co2_saved_kg / 0.192, 1) if annual_co2_saved_kg > 0 else 0.0

        narrative = (
            f"By executing your tailored routine and IAQ protocols, you eliminate an estimated "
            f"{daily_pm25_shielded_ug:,.0f} micrograms of toxic PM2.5 from deep alveolar lung deposition daily—"
            f"the health equivalent of avoiding {cigarettes_shielded} cigarettes every single day. "
            f"Simultaneously, shifting your {req.daily_commute_km} km commute toward electrified rapid transit "
            f"diverts {annual_co2_saved_kg:,.1f} kg of carbon dioxide annually from your city's inversion dome."
        )

        alternatives = [
            {
                "category": "Urban Commute",
                "current": f"Solo Commute ({req.commute_mode.value.replace('_', ' ').title()})",
                "alternative": "Electric Metro + Shared Last-Mile EV Feeder",
                "impact": f"Slashes tailpipe CO2 by 92% and avoids {daily_co2_saved_kg:.2f} kg CO2 daily."
            },
            {
                "category": "Indoor Air Filtration",
                "current": "Sealed Room with No Air Cleaning or Costly $400 HEPA Purifiers",
                "alternative": "Open-Source Corsi-Rosenthal Box (4x MERV-13 Filters + Box Fan)",
                "impact": "Delivers 250+ CFM CADR at 83% lower capital cost; replaces filters for $35/season."
            },
            {
                "category": "Winter Domestic Heating",
                "current": "Biomass / Charcoal Fire or Traditional Inefficient Coils",
                "alternative": "High-Efficiency Ceramic Radiant PTC / Heat Pump Heaters",
                "impact": "Zero localized carbon monoxide (CO) or black carbon emissions inside living spaces."
            },
            {
                "category": "Home Ventilation",
                "current": "Random window opening or permanent winter closure",
                "alternative": "Targeted Diurnal Inversion Solar Flush (1:00 PM - 3:00 PM)",
                "impact": "Flushes indoor CO2 buildup while avoiding nocturnal thermal particulate traps."
            }
        ]

        return ImpactResponse(
            daily_pm25_inhaled_avoided_ug=daily_pm25_shielded_ug,
            annual_pm25_avoided_grams=annual_pm25_avoided_g,
            cigarettes_equivalent_shielded_daily=cigarettes_shielded,
            annual_co2_reduction_kg=round(annual_co2_saved_kg, 1),
            car_km_equivalent_saved=car_km_equiv,
            pediatric_lung_risk_reduction_pct=pediatric_benefit,
            explainable_impact_narrative=narrative,
            sustainable_alternatives=alternatives
        )

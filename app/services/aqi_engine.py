"""AQI & Thermal Inversion Engine.

Implements standard breakpoint math (CPCB / US EPA standards),
cigarette equivalence (Berkeley Earth methodology), and diurnal thermal
boundary layer inversion modeling.
"""

import math
from typing import ClassVar

from app.data.preset_cities import get_city_profile
from app.models.schemas import (
    AQISnapshot,
    PollutantMetrics,
    ThermalInversionHour,
)


class AQIEngine:
    """Deterministic Air Quality & Thermal Inversion Modeling Engine."""

    # PM2.5 Breakpoints (ug/m3) -> AQI (CPCB / EPA scale)
    PM25_BREAKPOINTS: ClassVar[list[tuple[float, float, int, int]]] = [
        (0.0, 30.0, 0, 50),         # Good
        (30.1, 60.0, 51, 100),      # Satisfactory / Moderate
        (60.1, 90.0, 101, 200),     # Moderate / Sensitive
        (90.1, 120.0, 201, 300),    # Poor / Unhealthy
        (120.1, 250.0, 301, 400),   # Very Poor / Very Unhealthy
        (250.1, 500.0, 401, 500),   # Severe / Hazardous
        (500.1, 800.0, 501, 800),   # Beyond Scale Hazardous
    ]

    @classmethod
    def calculate_pm25_subindex(cls, pm25: float) -> int:
        """Calculate AQI sub-index for PM2.5 using piecewise linear interpolation.

        Args:
            pm25 (float): Particulate concentration in micrograms per cubic meter (ug/m3).

        Returns:
            int: Discrete Air Quality Index value (0 - 999).
        """
        if pm25 <= 0:
            return 0
        for bp_low, bp_high, aqi_low, aqi_high in cls.PM25_BREAKPOINTS:
            if bp_low <= pm25 <= bp_high:
                aqi = ((aqi_high - aqi_low) / (bp_high - bp_low)) * (pm25 - bp_low) + aqi_low
                return round(aqi)
        # Cap above highest breakpoint proportionally
        return int(min(999.0, 500.0 + (pm25 - 500.0) * 0.8))

    @staticmethod
    def get_aqi_category(aqi: int) -> str:
        """Categorize AQI value according to standardized tiers.

        Args:
            aqi (int): Air Quality Index value.

        Returns:
            str: Descriptive tier ("Good", "Satisfactory", "Moderate", "Poor", "Very Poor", "Severe (Hazardous)").
        """
        if aqi <= 50:
            return "Good"
        elif aqi <= 100:
            return "Satisfactory"
        elif aqi <= 200:
            return "Moderate"
        elif aqi <= 300:
            return "Poor"
        elif aqi <= 400:
            return "Very Poor"
        else:
            return "Severe (Hazardous)"

    @staticmethod
    def calculate_cigarette_equivalent(pm25_ug_m3: float) -> float:
        """Calculate daily cigarette inhalation equivalent via Berkeley Earth methodology.

        Formula: Inhaling 22 ug/m3 of PM2.5 over 24 hours delivers particulate
        mass equivalent to smoking approximately 1 cigarette.

        Args:
            pm25_ug_m3 (float): PM2.5 concentration in ug/m3.

        Returns:
            float: Equivalent number of cigarettes smoked per 24 hours.
        """
        return round(pm25_ug_m3 / 22.0, 1)

    @classmethod
    def generate_diurnal_inversion_curve(
        cls,
        base_pm25: float,
        morning_peak: int = 7,
        evening_peak: int = 20,
        temp_c: float = 14.0,
    ) -> list[ThermalInversionHour]:
        """Simulate diurnal winter atmospheric boundary layer (ABL) dynamics.

        Accounts for:
        - Nocturnal radiative cooling trapping pollutants near ground (<150m mixing height).
        - Solar insolation between 12:00 PM and 3:30 PM expanding mixing height (800-1200m).
        - Evening temperature drop triggering renewed inversion layer capping.

        Args:
            base_pm25 (float): Baseline particulate concentration.
            morning_peak (int): Hour of maximum morning radiative inversion. Defaults to 7.
            evening_peak (int): Hour of maximum evening traffic and subsidence inversion. Defaults to 20.
            temp_c (float): Ambient surface temperature in Celsius. Defaults to 14.0.

        Returns:
            list[ThermalInversionHour]: 24-hour hourly trajectory of inversion intensity and ventilation safety.
        """
        curve = []
        for hour in range(24):
            # Diurnal bell curves
            # Morning radiation peak
            dist_morning = min(abs(hour - morning_peak), 24 - abs(hour - morning_peak))
            # Evening traffic + cooling peak
            dist_evening = min(abs(hour - evening_peak), 24 - abs(hour - evening_peak))

            # Afternoon solar maximum (hour 13 - 15)
            afternoon_factor = max(0.0, 1.0 - abs(hour - 14) / 4.0)

            # Inversion intensity: highest at 6-8 AM, lowest at 1-3 PM
            inversion_intensity = (
                85.0 * math.exp(-0.5 * (dist_morning / 2.2) ** 2)
                + 75.0 * math.exp(-0.5 * (dist_evening / 2.5) ** 2)
            )
            inversion_intensity = max(15.0, min(98.0, inversion_intensity - (afternoon_factor * 55.0)))

            # Mixing height inversely proportional to inversion
            mixing_height = round(120.0 + (1.0 - (inversion_intensity / 100.0)) * 950.0)

            # Ground vs upper boundary temperature
            ground_temp = round(temp_c - (3.5 * math.cos((hour - 4) * math.pi / 12.0)), 1)

            # Window ventilation is safe only when mixing height > 550m and smog trap < 45
            is_vent_safe = (mixing_height >= 550 and inversion_intensity < 45 and 12 <= hour <= 16)

            ampm = "AM" if hour < 12 else "PM"
            display_h = hour if hour <= 12 else hour - 12
            if display_h == 0:
                display_h = 12
            label = f"{display_h:02d}:00 {ampm}"

            curve.append(
                ThermalInversionHour(
                    hour=hour,
                    label=label,
                    ground_temp_c=ground_temp,
                    mixing_height_m=mixing_height,
                    smog_trap_index=round(inversion_intensity),
                    ventilation_safe=is_vent_safe,
                )
            )
        return curve

    @classmethod
    def get_snapshot(cls, city_name: str) -> AQISnapshot:
        """Assemble a complete AQI snapshot with atmospheric telemetry and inversion analysis.

        Args:
            city_name (str): Urban center name to evaluate.

        Returns:
            AQISnapshot: Complete air quality snapshot, pollutants, cigarette equivalence, and inversion curve.
        """
        profile = get_city_profile(city_name)
        pm25 = profile["base_pm25"]
        pm10 = profile["base_pm10"]
        aqi = cls.calculate_pm25_subindex(pm25)
        category = cls.get_aqi_category(aqi)
        cigarettes = cls.calculate_cigarette_equivalent(pm25)

        pollutants = PollutantMetrics(
            pm25=pm25,
            pm10=pm10,
            no2=profile["base_no2"],
            co=profile["base_co"],
            o3=profile["base_o3"],
            so2=profile["base_so2"],
            temp_c=profile["temp_c"],
            humidity_pct=profile["humidity_pct"],
        )

        inversion_curve = cls.generate_diurnal_inversion_curve(
            base_pm25=pm25,
            morning_peak=profile.get("morning_peak_hour", 7),
            evening_peak=profile.get("evening_peak_hour", 20),
            temp_c=profile["temp_c"],
        )

        return AQISnapshot(
            city_name=profile["city_name"],
            country=profile["country"],
            aqi=aqi,
            category=category,
            dominant_pollutant="PM2.5",
            pollutants=pollutants,
            cigarette_equivalent=cigarettes,
            thermal_inversion_active=aqi > 200,
            safe_ventilation_window=profile.get("best_vent_window", "1:00 PM - 3:00 PM"),
            health_headline=profile.get("headline", "Winter Inversion Active"),
            vulnerable_warning=profile.get("vulnerable_warning", "Restrict outdoor exposure"),
            inversion_curve=inversion_curve,
        )

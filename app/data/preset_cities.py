"""
Preset atmospheric and smog profiles for major urban winter hotspots.

Provides empirical baselines for PM2.5, PM10, thermal boundary inversion layers,
and diurnal smog dispersion patterns.
"""

from typing import Dict, Any


PRESET_CITIES: Dict[str, Dict[str, Any]] = {
    "Delhi-NCR": {
        "city_name": "Delhi-NCR",
        "country": "India",
        "base_pm25": 385.0,
        "base_pm10": 490.0,
        "base_no2": 82.0,
        "base_co": 3.8,
        "base_o3": 28.0,
        "base_so2": 22.0,
        "temp_c": 13.5,
        "humidity_pct": 78.0,
        "inversion_severity": "EXTREME",
        "morning_peak_hour": 7,
        "evening_peak_hour": 21,
        "best_vent_window": "1:00 PM - 3:00 PM",
        "headline": "Severe Winter Radiation Inversion: Hazardous Smog Blanket Trapped Below 180m",
        "vulnerable_warning": "Immediate high pulmonary risk for children, infants & asthmatics. Zero outdoor physical exertion recommended."
    },
    "Lahore": {
        "city_name": "Lahore",
        "country": "Pakistan",
        "base_pm25": 415.0,
        "base_pm10": 530.0,
        "base_no2": 88.0,
        "base_co": 4.1,
        "base_o3": 25.0,
        "base_so2": 24.0,
        "temp_c": 14.0,
        "humidity_pct": 82.0,
        "inversion_severity": "EXTREME",
        "morning_peak_hour": 6,
        "evening_peak_hour": 20,
        "best_vent_window": "1:30 PM - 3:00 PM",
        "headline": "Transboundary Winter Smog Emergency: Dense Toxic Haze with Extreme PM2.5",
        "vulnerable_warning": "N95 masks mandatory outdoors. Keep windows tightly sealed with foam weatherstripping."
    },
    "Beijing": {
        "city_name": "Beijing",
        "country": "China",
        "base_pm25": 135.0,
        "base_pm10": 210.0,
        "base_no2": 55.0,
        "base_co": 1.9,
        "base_o3": 35.0,
        "base_so2": 15.0,
        "temp_c": 1.5,
        "humidity_pct": 45.0,
        "inversion_severity": "MODERATE_HIGH",
        "morning_peak_hour": 8,
        "evening_peak_hour": 19,
        "best_vent_window": "12:00 PM - 2:00 PM",
        "headline": "Winter District Heating Inversion: Elevated PM2.5 Under Cold High-Pressure Capping",
        "vulnerable_warning": "Air purifiers should operate on Continuous Medium mode in residential nurseries."
    },
    "Salt Lake City": {
        "city_name": "Salt Lake City",
        "country": "USA",
        "base_pm25": 58.0,
        "base_pm10": 85.0,
        "base_no2": 42.0,
        "base_co": 1.2,
        "base_o3": 38.0,
        "base_so2": 8.0,
        "temp_c": -2.0,
        "humidity_pct": 65.0,
        "inversion_severity": "MODERATE",
        "morning_peak_hour": 9,
        "evening_peak_hour": 18,
        "best_vent_window": "2:00 PM - 4:00 PM",
        "headline": "Wasatch Valley Topographic Inversion: Cold Air Trapping Urban Mobile Emissions",
        "vulnerable_warning": "Sensitive groups and asthmatic runners should restrict outdoor cardio to afternoons."
    },
    "London": {
        "city_name": "London",
        "country": "UK",
        "base_pm25": 32.0,
        "base_pm10": 48.0,
        "base_no2": 46.0,
        "base_co": 0.8,
        "base_o3": 42.0,
        "base_so2": 6.0,
        "temp_c": 6.0,
        "humidity_pct": 85.0,
        "inversion_severity": "LOW_MODERATE",
        "morning_peak_hour": 8,
        "evening_peak_hour": 18,
        "best_vent_window": "11:00 AM - 3:00 PM",
        "headline": "Anticyclonic Winter Stagnation: Roadside NO2 Stagnation in Central Low-Emission Zones",
        "vulnerable_warning": "Pedestrians advised to take back-street walking corridors rather than high-idle arterial roads."
    },
    "Mumbai": {
        "city_name": "Mumbai",
        "country": "India",
        "base_pm25": 118.0,
        "base_pm10": 175.0,
        "base_no2": 58.0,
        "base_co": 1.8,
        "base_o3": 32.0,
        "base_so2": 14.0,
        "temp_c": 24.0,
        "humidity_pct": 74.0,
        "inversion_severity": "MODERATE",
        "morning_peak_hour": 8,
        "evening_peak_hour": 20,
        "best_vent_window": "12:30 PM - 3:30 PM",
        "headline": "Coastal Marine Inversion & Urban Dust: Sea-Breeze Reversal Trapping Coastal Smog",
        "vulnerable_warning": "Early morning joggers should wear particulate respirators during low wind-speed hours."
    }
}


def get_city_profile(city_name: str) -> Dict[str, Any]:
    """Retrieves city profile or returns an intelligent parameterized default."""
    for key, data in PRESET_CITIES.items():
        if key.lower() in city_name.lower() or city_name.lower() in key.lower():
            return data
    
    # Sensible fallback for custom cities
    return {
        "city_name": city_name.title(),
        "country": "Global Metro",
        "base_pm25": 165.0,
        "base_pm10": 230.0,
        "base_no2": 52.0,
        "base_co": 2.1,
        "base_o3": 30.0,
        "base_so2": 16.0,
        "temp_c": 12.0,
        "humidity_pct": 72.0,
        "inversion_severity": "MODERATE_HIGH",
        "morning_peak_hour": 7,
        "evening_peak_hour": 20,
        "best_vent_window": "1:00 PM - 3:00 PM",
        "headline": f"Winter Atmospheric Boundary Inversion Active across {city_name.title()}",
        "vulnerable_warning": "Elevated particulate concentrations. Implement indoor IAQ filtration and avoid peak-hour idling corridors."
    }

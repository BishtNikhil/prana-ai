"""PranaAI Atmospheric Data Package.

Provides preset meteorological profiles and urban baseline smog metrics.
"""

from app.data.preset_cities import PRESET_CITIES, get_city_profile

__all__ = [
    "PRESET_CITIES",
    "get_city_profile",
]

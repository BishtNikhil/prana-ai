"""
Unit tests for PranaAI AQI and Thermal Inversion Engine.
"""

import pytest
from app.services.aqi_engine import AQIEngine


def test_pm25_subindex_calculation():
    """Validates piecewise linear interpolation across standard AQI breakpoints."""
    assert AQIEngine.calculate_pm25_subindex(0.0) == 0
    assert AQIEngine.calculate_pm25_subindex(15.0) == 25
    assert AQIEngine.calculate_pm25_subindex(30.0) == 50
    assert AQIEngine.calculate_pm25_subindex(60.0) == 100
    assert AQIEngine.calculate_pm25_subindex(90.0) == 200
    assert AQIEngine.calculate_pm25_subindex(120.0) == 300
    assert AQIEngine.calculate_pm25_subindex(250.0) == 400
    assert AQIEngine.calculate_pm25_subindex(385.0) >= 450


def test_aqi_category_mapping():
    """Verifies that AQI values map to appropriate standardized risk tiers."""
    assert AQIEngine.get_aqi_category(35) == "Good"
    assert AQIEngine.get_aqi_category(75) == "Satisfactory"
    assert AQIEngine.get_aqi_category(150) == "Moderate"
    assert AQIEngine.get_aqi_category(250) == "Poor"
    assert AQIEngine.get_aqi_category(350) == "Very Poor"
    assert AQIEngine.get_aqi_category(450) == "Severe (Hazardous)"


def test_cigarette_equivalent():
    """Tests Berkeley Earth formula: ~22 ug/m3 PM2.5 for 24h = 1 cigarette."""
    assert AQIEngine.calculate_cigarette_equivalent(22.0) == 1.0
    assert AQIEngine.calculate_cigarette_equivalent(44.0) == 2.0
    assert AQIEngine.calculate_cigarette_equivalent(385.0) == 17.5


def test_diurnal_inversion_curve():
    """Checks 24-hour diurnal thermal inversion curve dynamics."""
    curve = AQIEngine.generate_diurnal_inversion_curve(base_pm25=385.0)
    assert len(curve) == 24
    
    # Morning inversion peak (around 6-8 AM) should have higher smog trap index than 1-3 PM
    morning_point = curve[7]
    afternoon_point = curve[14]
    
    assert morning_point.smog_trap_index > afternoon_point.smog_trap_index
    assert morning_point.mixing_height_m < afternoon_point.mixing_height_m
    assert afternoon_point.ventilation_safe is True
    assert morning_point.ventilation_safe is False


def test_get_snapshot_delhi():
    """Verifies full snapshot assembly for Delhi-NCR."""
    snapshot = AQIEngine.get_snapshot("Delhi-NCR")
    assert snapshot.city_name == "Delhi-NCR"
    assert snapshot.aqi >= 400
    assert snapshot.category == "Severe (Hazardous)"
    assert snapshot.thermal_inversion_active is True
    assert len(snapshot.inversion_curve) == 24
    assert snapshot.cigarette_equivalent >= 15.0

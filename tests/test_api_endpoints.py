"""
Integration tests for PranaAI REST API Endpoints and Security Contracts.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check_endpoint():
    """Verifies service health check and telemetry status."""
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "HEALTHY"
    assert "PranaAI" in data["service"]
    assert data["deterministic_fallback_ready"] is True


def test_preset_cities_endpoint():
    """Verifies that preset smog hotspot cities are returned."""
    resp = client.get("/api/aqi/cities")
    assert resp.status_code == 200
    cities = resp.json()
    assert len(cities) >= 5
    city_names = [c["city_name"] for c in cities]
    assert "Delhi-NCR" in city_names
    assert "Lahore" in city_names
    assert "Beijing" in city_names


def test_aqi_snapshot_endpoint():
    """Verifies live AQI snapshot computation for requested city."""
    resp = client.get("/api/aqi/snapshot?city=Delhi-NCR")
    assert resp.status_code == 200
    data = resp.json()
    assert data["city_name"] == "Delhi-NCR"
    assert data["aqi"] > 0
    assert "PM2.5" in data["dominant_pollutant"]
    assert len(data["inversion_curve"]) == 24
    assert data["cigarette_equivalent"] > 0


def test_routine_plan_endpoint():
    """Verifies routine optimization endpoint contract."""
    resp = client.post("/api/routine/plan?city=Delhi-NCR&persona=family_with_kids")
    assert resp.status_code == 200
    data = resp.json()
    assert data["city"] == "Delhi-NCR"
    assert data["persona"] == "family_with_kids"
    assert len(data["steps"]) >= 4
    assert data["total_pm25_saved_ug"] > 0


def test_iaq_calculate_endpoint():
    """Verifies indoor IAQ calculation endpoint."""
    payload = {
        "room_name": "Kids Nursery",
        "length_ft": 14.0,
        "width_ft": 12.0,
        "ceiling_height_ft": 9.5,
        "occupants": 2,
        "has_hepa_purifier": False,
        "smog_entry_risk": "HIGH"
    }
    resp = client.post("/api/iaq/calculate", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["volume_cuft"] > 1000
    assert data["target_cadr_cfm"] > 0
    assert data["corsi_rosenthal_plan"]["filter_count"] == 4


def test_impact_evaluate_endpoint():
    """Verifies quantified personal and community impact evaluation."""
    payload = {
        "daily_commute_km": 24.0,
        "commute_mode": "solo_petrol_car",
        "household_members": 4,
        "winter_heating_source": "ELECTRIC",
        "cooking_style": "HIGH_FRYING",
        "adopted_ventilation_protocol": True,
        "installed_diy_iaq_filter": True
    }
    resp = client.post("/api/impact/evaluate", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["daily_pm25_inhaled_avoided_ug"] > 0
    assert data["annual_co2_reduction_kg"] > 0
    assert data["cigarettes_equivalent_shielded_daily"] > 0
    assert len(data["sustainable_alternatives"]) >= 3


def test_community_grievance_endpoint():
    """Verifies municipal grievance letter and WhatsApp alert synthesis."""
    payload = {
        "issue_type": "garbage_burning",
        "ward_or_colony": "Sector 43, Gurugram",
        "city": "Delhi-NCR",
        "landmark": "Near Community Park boundary wall",
        "frequency": "DAILY_MORNING",
        "impacted_residents": 800
    }
    resp = client.post("/api/community/grievance", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert "The Air (Prevention and Control of Pollution) Act" in data["formal_grievance_letter"]
    assert "COMMUNITY SMOG ALERT" in data["whatsapp_broadcast_message"]
    assert len(data["action_checklist"]) >= 3


def test_chat_endpoint_deterministic_fallback():
    """Verifies GenAI chat copilot functions with 100% reliability via deterministic fallback."""
    payload = {
        "message": "Which mask is best for morning smog in Delhi?",
        "city": "Delhi-NCR",
        "persona": "family_with_kids"
    }
    resp = client.post("/api/chat", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert "N95" in data["reply"] or "mask" in data["reply"].lower()
    assert data["confidence_score"] > 0.8
    assert data["actionable_takeaway"] != ""


def test_owasp_security_headers():
    """Verifies OWASP standard security headers are injected into every HTTP response."""
    resp = client.get("/health")
    assert resp.headers.get("X-Content-Type-Options") == "nosniff"
    assert resp.headers.get("X-Frame-Options") == "DENY"
    assert resp.headers.get("X-XSS-Protection") == "1; mode=block"
    assert "strict-origin" in resp.headers.get("Referrer-Policy")
    assert "X-Response-Time-Ms" in resp.headers
    assert "PranaAI" in resp.headers.get("X-Powered-By")

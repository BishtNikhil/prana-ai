"""
Unit tests for Impact Engine and Community Grievance Service.
"""

import pytest
from app.models.schemas import ImpactRequest, CommuteMode, CommunityGrievanceRequest
from app.services.impact_engine import ImpactEngine
from app.services.community_service import CommunityService


def test_impact_engine_evaluation():
    """Validates emission calculations, cigarette equivalents, and alternatives."""
    req = ImpactRequest(
        daily_commute_km=25.0,
        commute_mode=CommuteMode.SOLO_DIESEL_SUV,
        household_members=4,
        winter_heating_source="ELECTRIC",
        cooking_style="HIGH_FRYING",
        adopted_ventilation_protocol=True,
        installed_diy_iaq_filter=True
    )
    res = ImpactEngine.evaluate_impact(req)

    assert res.daily_pm25_inhaled_avoided_ug > 1000.0
    assert res.annual_pm25_avoided_grams > 0.3
    assert res.cigarettes_equivalent_shielded_daily > 4.0
    assert res.annual_co2_reduction_kg > 1000.0
    assert res.car_km_equivalent_saved > 5000.0
    assert res.pediatric_lung_risk_reduction_pct >= 80.0
    assert "inversion dome" in res.explainable_impact_narrative
    assert len(res.sustainable_alternatives) == 4


def test_community_service_garbage_burning():
    """Validates municipal grievance and WhatsApp alert for open waste burning."""
    req = CommunityGrievanceRequest(
        issue_type="garbage_burning",
        ward_or_colony="Green Park Extension",
        city="Delhi-NCR",
        landmark="Near DDA Community Center",
        frequency="DAILY_MORNING",
        impacted_residents=650
    )
    res = CommunityService.generate_grievance(req)

    assert "The Air (Prevention and Control of Pollution) Act, 1981" in res.legal_statutory_basis
    assert "Green Park Extension" in res.formal_grievance_letter
    assert "650 affected families" in res.formal_grievance_letter
    assert "P0 - CRITICAL EMERGENCY" in res.priority_tier
    assert "🚨 *COMMUNITY SMOG ALERT" in res.whatsapp_broadcast_message
    assert len(res.action_checklist) == 4


def test_community_service_construction_dust():
    """Validates construction dust compliance notice."""
    req = CommunityGrievanceRequest(
        issue_type="construction_dust",
        ward_or_colony="Whitefield",
        city="Bengaluru",
        landmark="Metro Flyover Pillar 140",
        frequency="OCCASIONAL",
        impacted_residents=300
    )
    res = CommunityService.generate_grievance(req)

    assert "Construction and Demolition (C&D) Waste Management Rules" in res.legal_statutory_basis
    assert "Whitefield" in res.formal_grievance_letter
    assert "P1 - HIGH URGENCY" in res.priority_tier

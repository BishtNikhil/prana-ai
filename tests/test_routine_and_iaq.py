"""
Unit tests for PranaAI Routine Optimization and IAQ Engines.
"""

import pytest
from app.models.schemas import PersonaType, IAQRoomRequest
from app.services.routine_engine import RoutineEngine
from app.services.iaq_engine import IAQEngine


def test_routine_plan_all_personas():
    """Validates that daily routine plans are generated cleanly for all 4 personas."""
    personas = [
        PersonaType.FAMILY_WITH_KIDS,
        PersonaType.DAILY_COMMUTER,
        PersonaType.HIGH_RISK_ASTHMA,
        PersonaType.COMMUNITY_LEADER
    ]

    for p in personas:
        plan = RoutineEngine.generate_plan("Delhi-NCR", p)
        assert plan.city == "Delhi-NCR"
        assert plan.persona == p
        assert len(plan.steps) >= 3
        assert plan.total_pm25_saved_ug > 0
        assert plan.cigarettes_toxicity_averted > 0
        assert plan.safe_ventilation_window != ""
        for step in plan.steps:
            assert step.time_window != ""
            assert step.activity_name != ""
            assert step.recommendation != ""
            assert step.scientific_rationale != ""
            assert step.risk_level in ["LOW", "MODERATE", "HIGH", "CRITICAL"]


def test_iaq_room_cadr_calculation():
    """Validates Clean Air Delivery Rate (CADR) formula based on room volume."""
    req = IAQRoomRequest(
        room_name="Master Bedroom",
        length_ft=15.0,
        width_ft=12.0,
        ceiling_height_ft=10.0,
        occupants=2,
        has_hepa_purifier=False,
        smog_entry_risk="HIGH"
    )

    plan = IAQEngine.calculate_room_plan(req)
    # Volume: 15 * 12 * 10 = 1800 cu ft
    assert plan.volume_cuft == 1800.0
    # CADR = (1800 * 5.0) / 60 = 150 CFM
    assert plan.target_cadr_cfm == 150
    assert plan.air_changes_per_hour == 5.0

    # Corsi-Rosenthal Blueprint verification
    assert plan.corsi_rosenthal_plan.box_fan_size_inches == 20
    assert plan.corsi_rosenthal_plan.filter_count == 4
    assert plan.corsi_rosenthal_plan.estimated_cadr_cfm >= 250
    assert plan.corsi_rosenthal_plan.savings_percentage > 80.0
    assert len(plan.corsi_rosenthal_plan.key_steps) >= 5

    # Plants and Hacks verification
    assert len(plan.phytoremediation_plants) >= 3
    assert len(plan.hacks_and_precautions) >= 4
    assert "KITCHEN SMOG PROTOCOL" in plan.kitchen_emission_protocol

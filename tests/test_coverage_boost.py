"""Comprehensive unit tests targeting 100% test coverage across all domain modules.

Verifies edge cases, domain exceptions, deterministic fallback queries,
mocked GenAI API calls, and index serving routes.
"""

import asyncio
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from app.core.exceptions import (
    AQIComputationError,
    GenAIServiceError,
    IAQComputationError,
    InvalidLocationError,
    PranaAIException,
    RoutineConstraintError,
)
from app.data.preset_cities import get_city_profile
from app.main import app, prana_exception_handler
from app.models.schemas import ChatMessageRequest, PersonaType
from app.services.aqi_engine import AQIEngine
from app.services.gemini_service import GeminiService

client = TestClient(app)


def test_domain_exceptions_and_handler():
    """Verify all domain exception classes instantiate and contain structured details."""
    exc1 = PranaAIException("Base error", {"key": "val"})
    assert exc1.message == "Base error"
    assert exc1.details == {"key": "val"}

    exc2 = AQIComputationError("Calculation failed")
    assert isinstance(exc2, PranaAIException)

    exc3 = InvalidLocationError("City not found")
    assert isinstance(exc3, PranaAIException)

    exc4 = RoutineConstraintError("Scheduling conflict")
    assert isinstance(exc4, PranaAIException)

    exc5 = IAQComputationError("CADR error")
    assert isinstance(exc5, PranaAIException)

    exc6 = GenAIServiceError("API quota exhausted")
    assert isinstance(exc6, PranaAIException)

    # Test the exception handler
    response = asyncio.run(prana_exception_handler(None, exc1))
    assert response.status_code == 400


def test_custom_city_profile_fallback():
    """Verify parameterized fallback when querying an unknown or custom city."""
    profile = get_city_profile("Atlantis")
    assert profile["city_name"] == "Atlantis"
    assert profile["country"] == "Global Metro"
    assert profile["base_pm25"] == 165.0
    assert "Inversion Active" in profile["headline"]


def test_aqi_engine_extreme_boundary_cases():
    """Verify negative PM2.5 and beyond-scale values in piecewise interpolation."""
    assert AQIEngine.calculate_pm25_subindex(-10.0) == 0
    # Values above highest breakpoint (800+)
    assert AQIEngine.calculate_pm25_subindex(950.0) >= 500


def test_gemini_service_all_fallback_branches():
    """Verify deterministic fallback engine across all 5 domain query categories."""
    # 1. Purifier / filter
    req1 = ChatMessageRequest(message="What is CADR and which purifier filter to buy?", city="Delhi-NCR")
    res1 = GeminiService.answer_query(req1)
    assert "Corsi-Rosenthal" in res1.reply or "purifier" in res1.reply.lower()

    # 2. Exercise / outdoor sports
    req2 = ChatMessageRequest(message="Can I go for a run or jog outside?", city="Delhi-NCR")
    res2 = GeminiService.answer_query(req2)
    assert "exercise" in res2.reply.lower() or "run" in res2.reply.lower() or "treadmill" in res2.reply.lower()

    # 3. Children / nursery
    req3 = ChatMessageRequest(message="How to protect baby and school kids from smog?", city="Delhi-NCR")
    res3 = GeminiService.answer_query(req3)
    assert "children" in res3.reply.lower() or "nursery" in res3.reply.lower()

    # 4. Indoor Plants
    req4 = ChatMessageRequest(message="Which indoor plants clean toxic air?", city="Delhi-NCR")
    res4 = GeminiService.answer_query(req4)
    assert "Snake Plant" in res4.reply or "NASA" in res4.reply

    # 5. General fallback
    req5 = ChatMessageRequest(message="Tell me general air pollution tips", city="Delhi-NCR")
    res5 = GeminiService.answer_query(req5)
    assert "inversion" in res5.reply.lower()


def test_gemini_service_mocked_api_success():
    """Verify live Gemini API response handling when valid key is provided."""
    req = ChatMessageRequest(
        message="What is the air status?",
        city="Delhi-NCR",
        persona=PersonaType.HIGH_RISK_ASTHMA,
    )
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "candidates": [
            {
                "content": {
                    "parts": [{"text": "Wear an N95 respirator and use HEPA filtration indoors."}]
                }
            }
        ]
    }

    with (
        patch("app.config.config.gemini_api_key", "test-valid-key"),
        patch("requests.post", return_value=mock_resp),
    ):
        res = GeminiService.answer_query(req)
        assert res.source == "gemini_2.5_flash"
        assert "N95" in res.reply


def test_gemini_service_mocked_api_failure_fallback():
    """Verify seamless fallback when live Gemini API call encounters network error."""
    req = ChatMessageRequest(message="General air advice", city="Delhi-NCR")

    with (
        patch("app.config.config.gemini_api_key", "test-key"),
        patch("requests.post", side_effect=RuntimeError("Connection timeout")),
    ):
        res = GeminiService.answer_query(req)
        assert res.source == "prana_deterministic_resilience_engine"


def test_root_index_html_serving():
    """Verify single-page application root route serves static HTML."""
    resp = client.get("/")
    assert resp.status_code == 200
    assert "text/html" in resp.headers.get("content-type", "")

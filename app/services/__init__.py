"""PranaAI Services and Computational Engines Package.

Provides core deterministic algorithms and GenAI services:
- AQIEngine: Air quality subindex, Berkeley Earth cigarette equivalence, and diurnal inversion curves.
- IAQEngine: Indoor clean air sizing, CADR calculations, Corsi-Rosenthal blueprints, phytoremediation.
- RoutineEngine: Persona-tailored 24-hour routine synthesis.
- ImpactEngine: Inhaled particulate shielding, commute emission savings, and sustainable alternatives.
- CommunityService: Legal petition drafting and emergency WhatsApp broadcasts.
- GeminiService: GenAI interaction backed by domain-grounded deterministic fallback.
"""

from app.services.aqi_engine import AQIEngine
from app.services.community_service import CommunityService
from app.services.gemini_service import GeminiService
from app.services.iaq_engine import IAQEngine
from app.services.impact_engine import ImpactEngine
from app.services.routine_engine import RoutineEngine

__all__ = [
    "AQIEngine",
    "CommunityService",
    "GeminiService",
    "IAQEngine",
    "ImpactEngine",
    "RoutineEngine",
]

"""
PranaAI Application Entry Point and API Orchestrator.

Exposes RESTful endpoints for real-time AQI & thermal inversion curves,
low-emission routine planning, indoor IAQ calculations, quantified impact metrics,
community smog sentinels, and resilient GenAI assistance.
"""

import time
from typing import Dict, Any, List
from fastapi import FastAPI, Request, Response, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pathlib import Path

from app.config import config
from app.core.exceptions import PranaAIException
from app.models.schemas import (
    AQISnapshot,
    DailyRoutinePlan,
    PersonaType,
    IAQRoomRequest,
    IAQPlanResponse,
    ImpactRequest,
    ImpactResponse,
    CommunityGrievanceRequest,
    CommunityGrievanceResponse,
    ChatMessageRequest,
    ChatMessageResponse
)
from app.services.aqi_engine import AQIEngine
from app.services.routine_engine import RoutineEngine
from app.services.iaq_engine import IAQEngine
from app.services.impact_engine import ImpactEngine
from app.services.community_service import CommunityService
from app.services.gemini_service import GeminiService
from app.data.preset_cities import PRESET_CITIES

# Resolve Directories
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"

# Initialize FastAPI App
app = FastAPI(
    title=config.app_name,
    version=config.app_version,
    description="Autonomous Urban Air Quality Assistant & Winter Smog Inversion Copilot for PromptWars Challenge 06",
    docs_url="/docs",
    redoc_url="/redoc"
)


# Custom Domain Exception Handler
@app.exception_handler(PranaAIException)
async def prana_exception_handler(request: Request, exc: PranaAIException) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content={
            "error_type": exc.__class__.__name__,
            "message": exc.message,
            "details": exc.details,
        }
    )


# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


# Enterprise Security & Telemetry Middleware
@app.middleware("http")
async def add_security_and_telemetry_headers(request: Request, call_next):
    start_time = time.perf_counter()
    response: Response = await call_next(request)
    duration_ms = round((time.perf_counter() - start_time) * 1000, 2)

    # Telemetry
    response.headers["X-Response-Time-Ms"] = str(duration_ms)
    response.headers["X-Powered-By"] = "PranaAI-FastAPI"

    # OWASP Standard Security Headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"

    return response


# --- REST API Endpoints ---

@app.get("/health", tags=["Telemetry"])
async def health_check() -> Dict[str, Any]:
    """Provides application health, version, and architectural readiness."""
    return {
        "status": "HEALTHY",
        "service": "PranaAI Urban Air Quality Assistant",
        "version": config.app_version,
        "environment": config.environment,
        "gemini_active": bool(config.gemini_api_key),
        "deterministic_fallback_ready": True,
        "timestamp": time.time()
    }


@app.get("/api/aqi/cities", tags=["Air Quality"])
async def list_preset_cities() -> List[Dict[str, Any]]:
    """Returns directory of preset urban smog hotspot profiles."""
    return [
        {
            "city_name": v["city_name"],
            "country": v["country"],
            "base_pm25": v["base_pm25"],
            "inversion_severity": v["inversion_severity"],
            "safe_window": v["best_vent_window"]
        }
        for v in PRESET_CITIES.values()
    ]


@app.get("/api/aqi/snapshot", response_model=AQISnapshot, tags=["Air Quality"])
async def get_aqi_snapshot(city: str = Query("Delhi-NCR", description="City name")) -> AQISnapshot:
    """Computes real-time AQI, cigarette equivalents, and 24-hr diurnal thermal inversion curve."""
    return AQIEngine.get_snapshot(city)


@app.post("/api/routine/plan", response_model=DailyRoutinePlan, tags=["Routine Optimization"])
async def plan_daily_routine(
    city: str = Query("Delhi-NCR"),
    persona: PersonaType = Query(PersonaType.FAMILY_WITH_KIDS)
) -> DailyRoutinePlan:
    """Synthesizes a personalized, low-emission daily routine based on diurnal smog curves."""
    return RoutineEngine.generate_plan(city, persona)


@app.post("/api/iaq/calculate", response_model=IAQPlanResponse, tags=["Indoor Air Quality"])
async def calculate_iaq_plan(req: IAQRoomRequest) -> IAQPlanResponse:
    """Calculates CADR requirements, Corsi-Rosenthal DIY filter specs, and botanical bio-filters."""
    return IAQEngine.calculate_room_plan(req)


@app.post("/api/impact/evaluate", response_model=ImpactResponse, tags=["Eco-Telemetry"])
async def evaluate_impact(req: ImpactRequest) -> ImpactResponse:
    """Computes direct quantified personal and community emission reductions."""
    return ImpactEngine.evaluate_impact(req)


@app.post("/api/community/grievance", response_model=CommunityGrievanceResponse, tags=["Community Sentinel"])
async def generate_community_grievance(req: CommunityGrievanceRequest) -> CommunityGrievanceResponse:
    """Generates a formal municipal grievance letter and community WhatsApp broadcast."""
    return CommunityService.generate_grievance(req)


@app.post("/api/chat", response_model=ChatMessageResponse, tags=["GenAI Assistant"])
async def chat_with_assistant(req: ChatMessageRequest) -> ChatMessageResponse:
    """Consults Prāṇa AI for science-backed air pollution and lifestyle advice."""
    return GeminiService.answer_query(req)


# --- Static Files & Root Single Page Application ---

if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/", include_in_schema=False)
async def serve_index():
    """Serves the main single page web application."""
    index_file = STATIC_DIR / "index.html"
    if index_file.exists():
        return FileResponse(str(index_file))
    # Fallback to root index.html if present
    root_index = BASE_DIR / "index.html"
    if root_index.exists():
        return FileResponse(str(root_index))
    return JSONResponse(
        content={"message": "PranaAI API operational. Please build UI in static/index.html"},
        status_code=200
    )

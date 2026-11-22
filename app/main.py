"""PranaAI Application Entry Point and API Orchestrator.

Exposes RESTful endpoints for real-time AQI & thermal inversion curves,
low-emission routine planning, indoor IAQ calculations, quantified impact metrics,
community smog sentinels, and resilient GenAI assistance.
"""

import time
from collections.abc import Awaitable, Callable
from pathlib import Path
from typing import Annotated, Any

from fastapi import FastAPI, Query, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from app.config import config
from app.core.exceptions import PranaAIException
from app.data.preset_cities import PRESET_CITIES
from app.models.schemas import (
    AQISnapshot,
    ChatMessageRequest,
    ChatMessageResponse,
    CommunityGrievanceRequest,
    CommunityGrievanceResponse,
    DailyRoutinePlan,
    IAQPlanResponse,
    IAQRoomRequest,
    ImpactRequest,
    ImpactResponse,
    PersonaType,
)
from app.services.aqi_engine import AQIEngine
from app.services.community_service import CommunityService
from app.services.gemini_service import GeminiService
from app.services.iaq_engine import IAQEngine
from app.services.impact_engine import ImpactEngine
from app.services.routine_engine import RoutineEngine

# Resolve Directories
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"

# Initialize FastAPI App
app = FastAPI(
    title=config.app_name,
    version=config.app_version,
    description="Autonomous Urban Air Quality Assistant & Winter Smog Inversion Copilot for PromptWars Challenge 06",
    docs_url="/docs",
    redoc_url="/redoc",
)


# Custom Domain Exception Handler
@app.exception_handler(PranaAIException)
async def prana_exception_handler(request: Request, exc: PranaAIException) -> JSONResponse:
    """Handle PranaAI domain exceptions with structured diagnostics.

    Args:
        request (Request): The incoming HTTP request.
        exc (PranaAIException): Domain exception instance.

    Returns:
        JSONResponse: 400 Bad Request with error type, message, and diagnostic details.
    """
    return JSONResponse(
        status_code=400,
        content={
            "error_type": exc.__class__.__name__,
            "message": exc.message,
            "details": exc.details,
        },
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
async def add_security_and_telemetry_headers(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    """Inject OWASP security headers and response-time telemetry into every HTTP response.

    Args:
        request (Request): Incoming FastAPI HTTP request.
        call_next (Callable): Next ASGI middleware or route handler.

    Returns:
        Response: Enriched HTTP response with security headers and duration metrics.
    """
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
async def health_check() -> dict[str, Any]:
    """Provide application health, version, and architectural readiness.

    Returns:
        dict[str, Any]: Health status, version, deployment environment, and timestamp.
    """
    return {
        "status": "HEALTHY",
        "service": "PranaAI Urban Air Quality Assistant",
        "version": config.app_version,
        "environment": config.environment,
        "gemini_active": bool(config.gemini_api_key),
        "deterministic_fallback_ready": True,
        "timestamp": time.time(),
    }


@app.get("/api/aqi/cities", tags=["Air Quality"])
async def list_preset_cities() -> list[dict[str, Any]]:
    """Return directory of preset urban smog hotspot profiles.

    Returns:
        list[dict[str, Any]]: List of supported preset cities and baselines.
    """
    return [
        {
            "city_name": v["city_name"],
            "country": v["country"],
            "base_pm25": v["base_pm25"],
            "inversion_severity": v["inversion_severity"],
            "safe_window": v["best_vent_window"],
        }
        for v in PRESET_CITIES.values()
    ]


@app.get("/api/aqi/snapshot", response_model=AQISnapshot, tags=["Air Quality"])
async def get_aqi_snapshot(
    city: Annotated[str, Query(description="City name")] = "Delhi-NCR",
) -> AQISnapshot:
    """Compute real-time AQI, cigarette equivalents, and 24-hr diurnal thermal inversion curve.

    Args:
        city (str): Urban metro name to query. Defaults to "Delhi-NCR".

    Returns:
        AQISnapshot: Snapshot containing AQI, pollutant breakdown, and inversion trajectory.
    """
    return AQIEngine.get_snapshot(city)


@app.post("/api/routine/plan", response_model=DailyRoutinePlan, tags=["Routine Optimization"])
async def plan_daily_routine(
    city: Annotated[str, Query(description="City name")] = "Delhi-NCR",
    persona: Annotated[PersonaType, Query(description="Vulnerability persona")] = PersonaType.FAMILY_WITH_KIDS,
) -> DailyRoutinePlan:
    """Synthesize a personalized, low-emission daily routine based on diurnal smog curves.

    Args:
        city (str): Target city name. Defaults to "Delhi-NCR".
        persona (PersonaType): User vulnerability persona. Defaults to FAMILY_WITH_KIDS.

    Returns:
        DailyRoutinePlan: Optimized chronological routine, emission cuts, and health metrics.
    """
    return RoutineEngine.generate_plan(city, persona)


@app.post("/api/iaq/calculate", response_model=IAQPlanResponse, tags=["Indoor Air Quality"])
async def calculate_iaq_plan(req: IAQRoomRequest) -> IAQPlanResponse:
    """Calculate CADR requirements, Corsi-Rosenthal DIY filter specs, and botanical bio-filters.

    Args:
        req (IAQRoomRequest): Room dimensions, occupancy, and ambient smog risk.

    Returns:
        IAQPlanResponse: Purification blueprint, plant choices, and ventilation protocols.
    """
    return IAQEngine.calculate_room_plan(req)


@app.post("/api/impact/evaluate", response_model=ImpactResponse, tags=["Eco-Telemetry"])
async def evaluate_impact(req: ImpactRequest) -> ImpactResponse:
    """Compute direct quantified personal and community emission reductions.

    Args:
        req (ImpactRequest): Commute habits, distance, and home filtration parameters.

    Returns:
        ImpactResponse: Quantified metrics including PM2.5 avoided, CO2 cut, and alternatives.
    """
    return ImpactEngine.evaluate_impact(req)


@app.post("/api/community/grievance", response_model=CommunityGrievanceResponse, tags=["Community Sentinel"])
async def generate_community_grievance(req: CommunityGrievanceRequest) -> CommunityGrievanceResponse:
    """Generate a formal municipal grievance letter and community WhatsApp broadcast.

    Args:
        req (CommunityGrievanceRequest): Pollution violation category, locality, and impact data.

    Returns:
        CommunityGrievanceResponse: Formal petition, statutory citation, and action checklist.
    """
    return CommunityService.generate_grievance(req)


@app.post("/api/chat", response_model=ChatMessageResponse, tags=["GenAI Assistant"])
async def chat_with_assistant(req: ChatMessageRequest) -> ChatMessageResponse:
    """Consult Prāṇa AI for science-backed air pollution and lifestyle advice.

    Args:
        req (ChatMessageRequest): User question, target city, and persona.

    Returns:
        ChatMessageResponse: AI response grounded in atmospheric science with actionable takeaway.
    """
    return GeminiService.answer_query(req)


# --- Static Files & Root Single Page Application ---

if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/", include_in_schema=False)
async def serve_index() -> Response:
    """Serve the main single page web application interface.

    Returns:
        Response: HTML file response or operational fallback JSON.
    """
    index_file = STATIC_DIR / "index.html"
    if index_file.exists():
        return FileResponse(str(index_file))
    # Fallback to root index.html if present
    root_index = BASE_DIR / "index.html"
    if root_index.exists():
        return FileResponse(str(root_index))
    return JSONResponse(
        content={"message": "PranaAI API operational. Please build UI in static/index.html"},
        status_code=200,
    )

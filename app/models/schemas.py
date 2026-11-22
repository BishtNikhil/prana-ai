"""Pydantic data schemas for PranaAI.

Enforces strict validation, typed API contracts, and clean JSON serialization.
"""

from enum import Enum

from pydantic import BaseModel, Field


class PersonaType(str, Enum):
    """User personas tailored for specific vulnerability profiles."""

    FAMILY_WITH_KIDS = "family_with_kids"
    DAILY_COMMUTER = "daily_commuter"
    HIGH_RISK_ASTHMA = "high_risk_asthma"
    COMMUNITY_LEADER = "community_leader"


class CommuteMode(str, Enum):
    """Daily transit modes for emission calculation and exposure modeling."""

    SOLO_PETROL_CAR = "solo_petrol_car"
    SOLO_DIESEL_SUV = "solo_diesel_suv"
    TWO_WHEELER = "two_wheeler"
    CARPOOL = "carpool"
    ELECTRIC_METRO = "electric_metro"
    EV_BUS = "ev_bus"
    CYCLING_WALKING = "cycling_walking"


class PollutantMetrics(BaseModel):
    """Atmospheric pollutant concentrations and environmental metrics."""

    pm25: float = Field(..., description="PM2.5 concentration in ug/m3")
    pm10: float = Field(..., description="PM10 concentration in ug/m3")
    no2: float = Field(..., description="NO2 concentration in ug/m3")
    co: float = Field(..., description="CO concentration in mg/m3")
    o3: float = Field(..., description="O3 concentration in ug/m3")
    so2: float = Field(..., description="SO2 concentration in ug/m3")
    temp_c: float = Field(..., description="Ambient temperature in Celsius")
    humidity_pct: float = Field(..., description="Relative humidity percentage")


class ThermalInversionHour(BaseModel):
    """Diurnal boundary layer inversion status for an individual hour."""

    hour: int = Field(..., ge=0, le=23, description="Hour of the day 0-23")
    label: str = Field(..., description="e.g. '06:00 AM'")
    ground_temp_c: float
    mixing_height_m: int
    smog_trap_index: int = Field(..., ge=0, le=100, description="0=Clean mixing, 100=Severe ground-level trap")
    ventilation_safe: bool = Field(..., description="True if safe to open windows")


class AQISnapshot(BaseModel):
    """Comprehensive urban air quality status snapshot and inversion report."""

    city_name: str
    country: str
    aqi: int = Field(..., ge=0, le=1000)
    category: str = Field(..., description="e.g. 'Hazardous', 'Severe', 'Very Poor', 'Moderate'")
    dominant_pollutant: str = "PM2.5"
    pollutants: PollutantMetrics
    cigarette_equivalent: float = Field(..., description="Daily cigarette smoking toxicity equivalent")
    thermal_inversion_active: bool
    safe_ventilation_window: str = Field(..., description="e.g. '1:00 PM - 3:00 PM'")
    health_headline: str
    vulnerable_warning: str
    inversion_curve: list[ThermalInversionHour]


class RoutineStep(BaseModel):
    """Individual chronological action step within a protected daily routine."""

    time_window: str = Field(..., description="e.g. '06:00 AM - 08:00 AM'")
    activity_name: str
    action_type: str = Field(..., description="indoor_shield | commute_shift | ventilation | domestic_iaq")
    recommendation: str
    scientific_rationale: str
    pm25_exposure_saved_ug: float
    emission_cut_kg_co2: float
    risk_level: str = Field(..., description="LOW | MODERATE | HIGH | CRITICAL")


class DailyRoutinePlan(BaseModel):
    """Complete 24-hour routine optimized to avoid peak pollution and inversion."""

    city: str
    persona: PersonaType
    current_aqi: int
    safe_ventilation_window: str
    steps: list[RoutineStep]
    total_pm25_saved_ug: float
    cigarettes_toxicity_averted: float
    total_co2_cut_kg: float
    executive_advisory: str


class IAQRoomRequest(BaseModel):
    """Indoor air quality and room dimensions payload."""

    room_name: str = "Living Room"
    length_ft: float = Field(15.0, gt=0)
    width_ft: float = Field(12.0, gt=0)
    ceiling_height_ft: float = Field(10.0, gt=0)
    occupants: int = Field(3, ge=1)
    has_hepa_purifier: bool = False
    kitchen_adjacent: bool = True
    smog_entry_risk: str = "HIGH"


class PlantBioFilter(BaseModel):
    """Phytoremediation botanical filter configuration."""

    name: str
    scientific_name: str
    recommended_count: int
    primary_toxin_filtered: str
    maintenance_level: str
    nighttime_oxygen: bool


class CorsiRosenthalBlueprint(BaseModel):
    """DIY Corsi-Rosenthal clean air box technical specifications."""

    box_fan_size_inches: int = 20
    merv_rating: str = "MERV 13"
    filter_count: int = 4
    estimated_cadr_cfm: int = 250
    estimated_cost_usd: float = 65.0
    commercial_equivalent_cost_usd: float = 380.0
    savings_percentage: float = 82.9
    build_time_minutes: int = 15
    key_steps: list[str]


class IAQPlanResponse(BaseModel):
    """Indoor air purification and ventilation remediation plan."""

    room_name: str
    volume_cuft: float
    target_cadr_cfm: int
    air_changes_per_hour: float
    corsi_rosenthal_plan: CorsiRosenthalBlueprint
    phytoremediation_plants: list[PlantBioFilter]
    hacks_and_precautions: list[str]
    kitchen_emission_protocol: str


class ImpactRequest(BaseModel):
    """User behavioral and transit parameters for emission and exposure calculation."""

    daily_commute_km: float = Field(20.0, ge=0)
    commute_mode: CommuteMode = CommuteMode.SOLO_PETROL_CAR
    household_members: int = Field(4, ge=1)
    winter_heating_source: str = "ELECTRIC"
    cooking_style: str = "HIGH_FRYING"
    adopted_ventilation_protocol: bool = True
    installed_diy_iaq_filter: bool = True


class ImpactResponse(BaseModel):
    """Calculated quantifiable health risk reduction and CO2 mitigation."""

    daily_pm25_inhaled_avoided_ug: float
    annual_pm25_avoided_grams: float
    cigarettes_equivalent_shielded_daily: float
    annual_co2_reduction_kg: float
    car_km_equivalent_saved: float
    pediatric_lung_risk_reduction_pct: float
    explainable_impact_narrative: str
    sustainable_alternatives: list[dict[str, str]]


class CommunityGrievanceRequest(BaseModel):
    """Local environmental violation grievance payload."""

    issue_type: str = Field(..., description="garbage_burning | construction_dust | diesel_generator | road_dust")
    ward_or_colony: str
    city: str
    landmark: str | None = None
    frequency: str = "DAILY_MORNING"
    impacted_residents: int = 500


class CommunityGrievanceResponse(BaseModel):
    """Generated legal petition and collective community mobilization toolkit."""

    formal_grievance_letter: str
    whatsapp_broadcast_message: str
    legal_statutory_basis: str
    priority_tier: str
    action_checklist: list[str]


class ChatMessageRequest(BaseModel):
    """PranaAI Copilot chat interaction payload."""

    message: str
    city: str = "Delhi-NCR"
    persona: PersonaType = PersonaType.FAMILY_WITH_KIDS
    conversation_history: list[dict[str, str]] | None = None


class ChatMessageResponse(BaseModel):
    """PranaAI Copilot response payload with grounding and source attribution."""

    reply: str
    actionable_takeaway: str
    confidence_score: float
    source: str

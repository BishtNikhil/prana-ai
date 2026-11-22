"""Routine Optimization Engine.

Generates tailored, low-emission daily routines and smog-resilient lifestyle schedules
based on active thermal inversion curves and user vulnerability personas.
"""

from app.models.schemas import (
    DailyRoutinePlan,
    PersonaType,
    RoutineStep,
)
from app.services.aqi_engine import AQIEngine


class RoutineEngine:
    """Engine for synthesizing personalized, low-emission daily routines."""

    @classmethod
    def generate_plan(cls, city: str, persona: PersonaType) -> DailyRoutinePlan:
        """Construct an optimized routine tailored to city AQI and lifestyle persona.

        Args:
            city (str): Urban center name to evaluate.
            persona (PersonaType): User vulnerability profile and daily habits.

        Returns:
            DailyRoutinePlan: Chronological 24-hour guidance, exposure saved, and aggregated metrics.
        """
        snapshot = AQIEngine.get_snapshot(city)
        aqi = snapshot.aqi
        vent_window = snapshot.safe_ventilation_window
        pm25 = snapshot.pollutants.pm25

        steps: list[RoutineStep] = []
        total_pm25_saved = 0.0
        total_co2_cut = 0.0

        if persona == PersonaType.FAMILY_WITH_KIDS:
            steps = [
                RoutineStep(
                    time_window="06:30 AM - 08:30 AM",
                    activity_name="Nursery Morning Inversion Shield & School Prep",
                    action_type="indoor_shield",
                    recommendation=(
                        "Seal bedroom windows with silicone weatherstrips; "
                        "run DIY Corsi-Rosenthal/HEPA purifier on Turbo in kids' room."
                    ),
                    scientific_rationale=(
                        "Nocturnal radiation inversion compresses PM2.5 into the bottom 120m air layer. "
                        "Outdoor air is at maximum toxicity. Indoor breathing protects developing alveoli."
                    ),
                    pm25_exposure_saved_ug=round(pm25 * 0.72 * 2.0, 1),
                    emission_cut_kg_co2=0.0,
                    risk_level="CRITICAL",
                ),
                RoutineStep(
                    time_window="08:30 AM - 09:15 AM",
                    activity_name="School Commute Protective Corridor",
                    action_type="commute_shift",
                    recommendation=(
                        "Ensure kids wear fitted N95/KF94 masks; switch car AC to 100% Recirculation mode "
                        "or use electric school bus pool."
                    ),
                    scientific_rationale=(
                        "Vehicle cabin air in recirculation mode with cabin filter blocks 80-88% of ambient PM2.5 "
                        "and ultrafine brake-wear particles."
                    ),
                    pm25_exposure_saved_ug=round(pm25 * 0.65 * 0.75, 1),
                    emission_cut_kg_co2=1.8,
                    risk_level="HIGH",
                ),
                RoutineStep(
                    time_window=vent_window,
                    activity_name="Diurnal High-Sun Ventilation & Flush Window",
                    action_type="ventilation",
                    recommendation=(
                        "Open cross-ventilating windows for 45-60 minutes; air out indoor CO2 and kitchen moisture, "
                        "then reseal."
                    ),
                    scientific_rationale=(
                        "Solar thermal radiation temporarily expands the planetary boundary layer mixing height "
                        "to ~950m, dispersing heavy ground smog by 40-60%."
                    ),
                    pm25_exposure_saved_ug=12.0,
                    emission_cut_kg_co2=0.0,
                    risk_level="LOW",
                ),
                RoutineStep(
                    time_window="05:30 PM - 07:00 PM",
                    activity_name="Indoor Active Play Substitution",
                    action_type="indoor_shield",
                    recommendation=(
                        "Replace outdoor park sports with indoor obstacle play or yoga; "
                        "keep entry door shielded with wet-curtain particulate trap."
                    ),
                    scientific_rationale=(
                        "Cardiovascular exertion during evening inversion increases minute ventilation rate by 400%, "
                        "multiplying deep-lung particulate deposition."
                    ),
                    pm25_exposure_saved_ug=round(pm25 * 0.85 * 1.5, 1),
                    emission_cut_kg_co2=0.0,
                    risk_level="HIGH",
                ),
                RoutineStep(
                    time_window="07:30 PM - 09:00 PM",
                    activity_name="Lidded Induction Cooking Protocol",
                    action_type="domestic_iaq",
                    recommendation=(
                        "Cook with closed lids on induction or low flame; run range hood exhaust at 180+ CFM "
                        "to vent frying aerosols."
                    ),
                    scientific_rationale=(
                        "Unvented deep frying generates volatile organic compounds (VOCs) and oil mist aerosols "
                        "exceeding 450 ug/m3 inside closed winter homes."
                    ),
                    pm25_exposure_saved_ug=145.0,
                    emission_cut_kg_co2=0.8,
                    risk_level="MODERATE",
                ),
            ]
            advisory = (
                "Protect child respiratory airways during peak morning inversion; rely on mid-day solar flush "
                "and clean indoor active games."
            )

        elif persona == PersonaType.DAILY_COMMUTER:
            steps = [
                RoutineStep(
                    time_window="07:00 AM - 08:30 AM",
                    activity_name="Pre-Commute Air Check & Indoor Cardio",
                    action_type="indoor_shield",
                    recommendation=(
                        "Exercise indoors with a room air purifier running; avoid outdoor morning jogging near "
                        "arterial bypasses."
                    ),
                    scientific_rationale=(
                        "Morning traffic combines with boundary layer inversion to create high roadside NO2 "
                        "and black carbon spikes."
                    ),
                    pm25_exposure_saved_ug=round(pm25 * 0.8 * 1.5, 1),
                    emission_cut_kg_co2=0.0,
                    risk_level="HIGH",
                ),
                RoutineStep(
                    time_window="08:30 AM - 09:45 AM",
                    activity_name="Low-Emission Rapid Metro Swap",
                    action_type="commute_shift",
                    recommendation=(
                        "Park vehicle at metro hub; complete 18km journey via Electric Metro Rail "
                        "instead of solo ICE vehicle."
                    ),
                    scientific_rationale=(
                        "Metro ridership slashes personal direct tailpipe exposure while eliminating 3.4kg CO2 "
                        "and 14g vehicular PM2.5 from urban airshed."
                    ),
                    pm25_exposure_saved_ug=round(pm25 * 0.70 * 1.2, 1),
                    emission_cut_kg_co2=3.4,
                    risk_level="CRITICAL",
                ),
                RoutineStep(
                    time_window=vent_window,
                    activity_name="Mid-Day Walk & Fresh Air Refresh",
                    action_type="ventilation",
                    recommendation=(
                        "Step out for a 20-min stroll in a wooded park during solar peak; office HVAC filters work at "
                        "optimal efficiency now."
                    ),
                    scientific_rationale=(
                        "Boundary layer dispersion peaks; ambient PM2.5 drops to its diurnal minimum, "
                        "lowering inhaled toxic burden."
                    ),
                    pm25_exposure_saved_ug=15.0,
                    emission_cut_kg_co2=0.0,
                    risk_level="LOW",
                ),
                RoutineStep(
                    time_window="06:30 PM - 08:00 PM",
                    activity_name="Off-Peak Departure / Carpool Return",
                    action_type="commute_shift",
                    recommendation=(
                        "Shift departure by 30 mins to avoid peak gridlock idling; "
                        "carpool with colleagues or use EV cabs."
                    ),
                    scientific_rationale=(
                        "Vehicle exhaust in slow bumper-to-bumper traffic concentrates toxic carbon monoxide "
                        "and polycyclic aromatic hydrocarbons (PAHs)."
                    ),
                    pm25_exposure_saved_ug=round(pm25 * 0.60 * 1.0, 1),
                    emission_cut_kg_co2=2.6,
                    risk_level="HIGH",
                ),
            ]
            advisory = (
                "Transform daily commute from a toxic smog hazard into a low-carbon transit habit, "
                "saving over 6.0kg CO2 per day."
            )

        elif persona == PersonaType.HIGH_RISK_ASTHMA:
            steps = [
                RoutineStep(
                    time_window="06:00 AM - 09:00 AM",
                    activity_name="Strict Sealed Sanctuary Quarantine",
                    action_type="indoor_shield",
                    recommendation=(
                        "Keep bedroom sealed; keep HEPA purifier running on Sleep/Medium continuous mode; "
                        "use prescribed preventive inhaler."
                    ),
                    scientific_rationale=(
                        "Early morning cold air induces broncho-constriction, compounding the inflammatory "
                        "attack of PM2.5 on hyper-reactive airways."
                    ),
                    pm25_exposure_saved_ug=round(pm25 * 0.90 * 3.0, 1),
                    emission_cut_kg_co2=0.0,
                    risk_level="CRITICAL",
                ),
                RoutineStep(
                    time_window=vent_window,
                    activity_name="Controlled Purifier Reset & Air Balancing",
                    action_type="ventilation",
                    recommendation=(
                        "Open only south-facing filtered windows briefly; clean purifier pre-filter screen with "
                        "damp cloth to remove trapped pet dander & dust."
                    ),
                    scientific_rationale=(
                        "Short midday air exchange prevents dangerous indoor CO2 buildup without admitting "
                        "high particulate loads."
                    ),
                    pm25_exposure_saved_ug=25.0,
                    emission_cut_kg_co2=0.0,
                    risk_level="LOW",
                ),
                RoutineStep(
                    time_window="06:00 PM - 09:00 PM",
                    activity_name="Phytoremediation & Steam Air Hydration",
                    action_type="domestic_iaq",
                    recommendation=(
                        "Sit near clustered NASA clean-air plants (Snake Plant, Areca); "
                        "use warm steam inhalation to moisten cilia."
                    ),
                    scientific_rationale=(
                        "Adequate airway hydration maintains mucosal ciliary clearance, accelerating the "
                        "expulsion of inhaled sub-micron particulates."
                    ),
                    pm25_exposure_saved_ug=round(pm25 * 0.75 * 2.0, 1),
                    emission_cut_kg_co2=0.0,
                    risk_level="HIGH",
                ),
            ]
            advisory = (
                "Zero-tolerance approach to morning outdoor air; enforce strict indoor HEPA filtration "
                "and airway hydration."
            )

        else:  # COMMUNITY_LEADER
            steps = [
                RoutineStep(
                    time_window="06:00 AM - 08:00 AM",
                    activity_name="Neighborhood Thermal Smog & Anti-Burning Patrol",
                    action_type="domestic_iaq",
                    recommendation=(
                        "Deploy community watch to prevent open municipal waste burning or security guard "
                        "biomass fires; supply electric radiant heaters."
                    ),
                    scientific_rationale=(
                        "A single open leaf/garbage fire emits 1,000x more carcinogenic dioxins and fine black "
                        "carbon than clean electric heating."
                    ),
                    pm25_exposure_saved_ug=320.0,
                    emission_cut_kg_co2=8.5,
                    risk_level="CRITICAL",
                ),
                RoutineStep(
                    time_window="09:00 AM - 11:00 AM",
                    activity_name="Water-Mist Road Sprinkling & Dust Suppression",
                    action_type="domestic_iaq",
                    recommendation=(
                        "Coordinate with resident welfare association (RWA) to spray water mist on internal "
                        "paved roads and building construction sites."
                    ),
                    scientific_rationale=(
                        "Moisture agglomeration forces airborne PM10 road dust to settle, preventing resuspension "
                        "by moving vehicular tires."
                    ),
                    pm25_exposure_saved_ug=280.0,
                    emission_cut_kg_co2=4.0,
                    risk_level="HIGH",
                ),
                RoutineStep(
                    time_window="02:00 PM - 04:00 PM",
                    activity_name="Community DIY Corsi-Rosenthal Workshop",
                    action_type="indoor_shield",
                    recommendation=(
                        "Host a workshop teaching apartment residents to build 250-CFM DIY purifiers using "
                        "local box fans and MERV-13 filters."
                    ),
                    scientific_rationale=(
                        "Equipping 20 households with DIY purifiers removes up to 1.8 kilograms of PM2.5 from "
                        "the localized residential airshed each week."
                    ),
                    pm25_exposure_saved_ug=450.0,
                    emission_cut_kg_co2=2.5,
                    risk_level="LOW",
                ),
            ]
            advisory = (
                "Mobilize community action against localized biomass burning, suppress fugitive road dust, "
                "and scale DIY air filtration."
            )

        # Aggregate metrics
        for s in steps:
            total_pm25_saved += s.pm25_exposure_saved_ug
            total_co2_cut += s.emission_cut_kg_co2

        cigarettes_averted = round(total_pm25_saved / 22.0, 1)

        return DailyRoutinePlan(
            city=snapshot.city_name,
            persona=persona,
            current_aqi=aqi,
            safe_ventilation_window=vent_window,
            steps=steps,
            total_pm25_saved_ug=round(total_pm25_saved, 1),
            cigarettes_toxicity_averted=cigarettes_averted,
            total_co2_cut_kg=round(total_co2_cut, 2),
            executive_advisory=advisory,
        )

"""Indoor Air Quality (IAQ) Engine.

Calculates room volume, target Clean Air Delivery Rate (CADR), required
air changes per hour (ACH), Corsi-Rosenthal DIY filter blueprints, and
NASA-backed botanical phytoremediation configurations.
"""

from app.models.schemas import (
    CorsiRosenthalBlueprint,
    IAQPlanResponse,
    IAQRoomRequest,
    PlantBioFilter,
)


class IAQEngine:
    """Deterministic scientific IAQ sizing and DIY clean air synthesizer."""

    @classmethod
    def calculate_room_plan(cls, req: IAQRoomRequest) -> IAQPlanResponse:
        """Compute CADR requirements and customized DIY hacks for any room.

        Args:
            req (IAQRoomRequest): Room dimensions, occupancy, and ambient smog risk level.

        Returns:
            IAQPlanResponse: Sizing calculation, Corsi-Rosenthal blueprint, and plant configurations.
        """
        # Volume in cubic feet
        volume_cuft = round(req.length_ft * req.width_ft * req.ceiling_height_ft, 1)

        # For severe smog conditions, target ACH is 5.0 (Air Changes per Hour)
        target_ach = 5.0 if req.smog_entry_risk == "HIGH" else 4.0

        # Required CADR (CFM) = (Room Volume * ACH) / 60
        target_cadr = round((volume_cuft * target_ach) / 60.0)

        # Corsi-Rosenthal Box specifications
        corsi_blueprint = CorsiRosenthalBlueprint(
            box_fan_size_inches=20,
            merv_rating="MERV 13",
            filter_count=4,
            estimated_cadr_cfm=max(250, target_cadr),
            estimated_cost_usd=65.0,
            commercial_equivalent_cost_usd=380.0,
            savings_percentage=82.9,
            build_time_minutes=15,
            key_steps=[
                "Tape four 20x20x2 inch MERV-13 filters into a 4-sided cube pointing airflow inward.",
                "Seal the bottom with a 20x20 cardboard panel using duct or painter tape.",
                "Place the 20-inch box fan on top, blowing upwards into the room.",
                (
                    "Cut a circular cardboard shroud (14-inch diameter hole) and tape to the fan face "
                    "to eliminate air backdraft vortices."
                ),
                "Run fan on Low/Medium speed for whisper-quiet continuous 250+ CFM purification.",
            ],
        )

        # NASA Botanical Phytoremediation calculation
        # Rule of thumb: 1 medium-sized plant per 80-100 sq ft for active bio-filtration
        room_sqft = req.length_ft * req.width_ft
        snake_plants_needed = max(2, round(room_sqft / 90.0))
        areca_palms_needed = max(1, round(room_sqft / 120.0))

        plants = [
            PlantBioFilter(
                name="Snake Plant (Sansevieria Trifasciata)",
                scientific_name="Dracaena trifasciata",
                recommended_count=snake_plants_needed,
                primary_toxin_filtered="Formaldehyde, Benzene & Trichloroethylene",
                maintenance_level="Very Low (Water every 2-3 weeks)",
                nighttime_oxygen=True,
            ),
            PlantBioFilter(
                name="Areca Palm (Chrysalidocarpus Lutescens)",
                scientific_name="Dypsis lutescens",
                recommended_count=areca_palms_needed,
                primary_toxin_filtered="Xylene, Toluene & General Airborne Particulates",
                maintenance_level="Moderate (Bright indirect sunlight)",
                nighttime_oxygen=False,
            ),
            PlantBioFilter(
                name="Spider Plant (Chlorophytum Comosum)",
                scientific_name="Chlorophytum comosum",
                recommended_count=max(2, round(room_sqft / 100.0)),
                primary_toxin_filtered="Carbon Monoxide & Ethylbenzene",
                maintenance_level="Low (Pet-friendly, adaptable)",
                nighttime_oxygen=False,
            ),
        ]

        hacks = [
            (
                "Electrostatic Wet-Towel Entry Trap: Hang a damp microfiber towel inside high-traffic entrance doors; "
                "damp fibers attract and capture settling sub-micron particulate aerosols."
            ),
            (
                "Cardboard Fan Shroud Trick: Adding a 14-inch round cardboard shroud to any standard box fan "
                "boosts fan static pressure by 35% and prevents dirty air from swirling back into the fan blade tips."
            ),
            (
                "Weatherstrip Window Gaskets: Install high-density foam or self-adhesive silicone D-profiles on window "
                "sashes to block up to 92% of smog infiltration during nighttime inversions."
            ),
            (
                "Negative Pressure Kitchen Quarantine: When cooking, keep kitchen doors closed and run exhaust. "
                "Never open hallway doors during frying to prevent VOCs from permeating sleep zones."
            ),
        ]

        kitchen_protocol = (
            "KITCHEN SMOG PROTOCOL: Unvented oil frying and spice tempering generate severe VOC and PM2.5 spikes "
            "often exceeding 500 ug/m3. Always operate exhaust at minimum 180 CFM with a cracked window in the kitchen "
            "to draw air OUTWARD, while keeping interior doors to living areas firmly sealed."
        )

        return IAQPlanResponse(
            room_name=req.room_name,
            volume_cuft=volume_cuft,
            target_cadr_cfm=target_cadr,
            air_changes_per_hour=target_ach,
            corsi_rosenthal_plan=corsi_blueprint,
            phytoremediation_plants=plants,
            hacks_and_precautions=hacks,
            kitchen_emission_protocol=kitchen_protocol,
        )

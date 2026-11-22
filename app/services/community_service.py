"""Community & Smog Sentinel Service.

Synthesizes formal municipal grievance letters, statutory legal citations,
and community WhatsApp broadcasts to counter localized air pollution hotspots.
"""

from typing import ClassVar

from app.models.schemas import (
    CommunityGrievanceRequest,
    CommunityGrievanceResponse,
)


class CommunityService:
    """Generates community mobilization letters and legal notifications."""

    ISSUE_MAPPING: ClassVar[dict[str, dict[str, str]]] = {
        "garbage_burning": {
            "title": "Unlawful Open Municipal Waste / Leaf Burning",
            "statute": (
                "The Air (Prevention and Control of Pollution) Act, 1981 (Section 19(5)) and "
                "National Green Tribunal (NGT) Order O.A. No. 21/2014."
            ),
            "penalty": "Statutory environmental compensation fine of up to INR 25,000 / USD 300 per violation.",
            "priority": "P0 - CRITICAL EMERGENCY",
        },
        "construction_dust": {
            "title": "Unmitigated Fugitive Construction & Demolition Dust",
            "statute": (
                "Construction and Demolition (C&D) Waste Management Rules, 2016 and CAQM Statutory "
                "Dust Control Guidelines."
            ),
            "penalty": "Mandatory site closure notice and forfeiture of environmental security bond.",
            "priority": "P1 - HIGH URGENCY",
        },
        "diesel_generator": {
            "title": "Illegal Operation of Non-Retrofit DG Sets during GRAP Restrictions",
            "statute": "Graded Response Action Plan (GRAP Stage-IV) Statutory Enforcement Orders.",
            "penalty": "Immediate disconnection of industrial supply and equipment sealing.",
            "priority": "P1 - HIGH URGENCY",
        },
        "road_dust": {
            "title": "High-Volume Unpaved Roadway Particulate Resuspension",
            "statute": "Municipal Solid Waste and Road Maintenance Standard Guidelines (Section 31A).",
            "penalty": "Mandatory mechanized sweeping and continuous water-mist sprinkling mandate.",
            "priority": "P2 - MEDIUM ELEVATED",
        },
    }

    @classmethod
    def generate_grievance(cls, req: CommunityGrievanceRequest) -> CommunityGrievanceResponse:
        """Synthesize formal municipal petition and community broadcast.

        Args:
            req (CommunityGrievanceRequest): Offense type, locality, affected residents count, and landmark.

        Returns:
            CommunityGrievanceResponse: Legal petition, WhatsApp mobilization text, statutory basis, and checklist.
        """
        info = cls.ISSUE_MAPPING.get(req.issue_type, cls.ISSUE_MAPPING["garbage_burning"])
        landmark_str = f" in the vicinity of {req.landmark}" if req.landmark else ""

        letter = (
            "To,\n"
            "The Commissioner / Executive Environmental Officer,\n"
            "Municipal Corporation & Pollution Control Board,\n"
            f"Jurisdiction: {req.city}\n\n"
            "Date: Immediate Notice\n"
            f"Subject: URGENT STATUTORY NOTICE — Cessation of {info['title']}{landmark_str}, {req.ward_or_colony}\n\n"
            "Respected Sir/Madam,\n\n"
            f"We, the undersigned residents and representatives of {req.ward_or_colony}, {req.city} "
            f"(representing approximately {req.impacted_residents} affected families), formally notify your office "
            "of severe, ongoing violations causing localized particulate smog spikes.\n\n"
            f"NATURE OF OFFENSE: {info['title']}.\n"
            f"LOCATION: {req.ward_or_colony}{landmark_str}, {req.city}.\n"
            f"FREQUENCY: {req.frequency.replace('_', ' ').title()}.\n\n"
            "STATUTORY BREACH:\n"
            f"This activity directly contravenes {info['statute']}. "
            "Under current winter boundary layer thermal inversion, localized toxic plumes cannot disperse, "
            "forcing children, elderly cardiac patients, and asthmatic residents to inhale carcinogenic "
            "PM2.5 and dioxins.\n\n"
            "REQUESTED ACTION:\n"
            "1. Immediate deployment of mobile flying enforcement squad to impound/extinguish the source.\n"
            f"2. Imposition of statutory penalties ({info['penalty']}).\n"
            "3. Provision of clean alternative heating or green waste composting infrastructure to prevent "
            "repeat incidents.\n\n"
            "Failure to act within 24 hours will compel escalation to the National Green Tribunal grievance bench and "
            "the State Environmental Ombudsman.\n\n"
            "Respectfully submitted,\n"
            "Concerned Citizens Coalition & RWA Representatives\n"
            f"{req.ward_or_colony}, {req.city}"
        )

        whatsapp = (
            f"🚨 *COMMUNITY SMOG ALERT — {req.ward_or_colony.upper()}* 🚨\n\n"
            f"⚠️ *Active Hazard*: {info['title']}{landmark_str}\n"
            "📊 *Threat*: Dense localized PM2.5 plume trapped by morning thermal inversion.\n\n"
            "🛡️ *Immediate Resident Actions*:\n"
            "• Keep all street-facing windows firmly sealed.\n"
            "• Avoid outdoor jogging / morning walks in this quadrant.\n"
            "• Run home purifiers on High/Turbo.\n"
            "• Do NOT burn garden leaves or garbage! Use our RWA green composting pit.\n\n"
            f"📞 A formal statutory complaint has been filed under {info['statute'][:45]}...\n"
            "Together for Clean Air & Safe Lungs! 🌿"
        )

        checklist = [
            f"Capture timestamped geotagged photograph/video of the {req.issue_type.replace('_', ' ')}.",
            "Dispatch the formal grievance letter to the zonal municipal office email and WhatsApp helpline.",
            "Circulate the emergency advisory in the apartment/colony WhatsApp groups to protect residents.",
            "Distribute electric fan heaters to night security staff to eliminate open scrap-wood bonfires.",
        ]

        return CommunityGrievanceResponse(
            formal_grievance_letter=letter,
            whatsapp_broadcast_message=whatsapp,
            legal_statutory_basis=info["statute"],
            priority_tier=info["priority"],
            action_checklist=checklist,
        )

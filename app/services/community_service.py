"""
Community & Smog Sentinel Service.

Synthesizes formal municipal grievance letters, statutory legal citations,
and community WhatsApp broadcasts to counter localized air pollution hotspots.
"""

from app.models.schemas import (
    CommunityGrievanceRequest,
    CommunityGrievanceResponse
)


class CommunityService:
    """Generates community mobilization letters and legal notifications."""

    ISSUE_MAPPING = {
        "garbage_burning": {
            "title": "Unlawful Open Municipal Waste / Leaf Burning",
            "statute": "The Air (Prevention and Control of Pollution) Act, 1981 (Section 19(5)) and National Green Tribunal (NGT) Order O.A. No. 21/2014.",
            "penalty": "Statutory environmental compensation fine of up to INR 25,000 / USD 300 per violation.",
            "priority": "P0 - CRITICAL EMERGENCY"
        },
        "construction_dust": {
            "title": "Unmitigated Fugitive Construction & Demolition Dust",
            "statute": "Construction and Demolition (C&D) Waste Management Rules, 2016 and CAQM Statutory Dust Control Guidelines.",
            "penalty": "Mandatory site closure notice and forfeiture of environmental security bond.",
            "priority": "P1 - HIGH URGENCY"
        },
        "diesel_generator": {
            "title": "Illegal Operation of Non-Retrofit DG Sets during GRAP Restrictions",
            "statute": "Graded Response Action Plan (GRAP Stage-IV) Statutory Enforcement Orders.",
            "penalty": "Immediate disconnection of industrial supply and equipment sealing.",
            "priority": "P1 - HIGH URGENCY"
        },
        "road_dust": {
            "title": "High-Volume Unpaved Roadway Particulate Resuspension",
            "statute": "Municipal Solid Waste and Road Maintenance Standard Guidelines (Section 31A).",
            "penalty": "Mandatory mechanized sweeping and continuous water-mist sprinkling mandate.",
            "priority": "P2 - MEDIUM ELEVATED"
        }
    }

    @classmethod
    def generate_grievance(cls, req: CommunityGrievanceRequest) -> CommunityGrievanceResponse:
        """Synthesizes formal municipal petition and community broadcast."""
        info = cls.ISSUE_MAPPING.get(req.issue_type, cls.ISSUE_MAPPING["garbage_burning"])
        landmark_str = f" in the vicinity of {req.landmark}" if req.landmark else ""

        letter = (
            f"To,\n"
            f"The Commissioner / Executive Environmental Officer,\n"
            f"Municipal Corporation & Pollution Control Board,\n"
            f"Jurisdiction: {req.city}\n\n"
            f"Date: Immediate Notice\n"
            f"Subject: URGENT STATUTORY NOTICE — Cessation of {info['title']}{landmark_str}, {req.ward_or_colony}\n\n"
            f"Respected Sir/Madam,\n\n"
            f"We, the undersigned residents and representatives of {req.ward_or_colony}, {req.city} "
            f"(representing approximately {req.impacted_residents} affected families), formally notify your office "
            f"of severe, ongoing violations causing localized particulate smog spikes.\n\n"
            f"NATURE OF OFFENSE: {info['title']}.\n"
            f"LOCATION: {req.ward_or_colony}{landmark_str}, {req.city}.\n"
            f"FREQUENCY: {req.frequency.replace('_', ' ').title()}.\n\n"
            f"STATUTORY BREACH:\n"
            f"This activity directly contravenes {info['statute']}. "
            f"Under current winter boundary layer thermal inversion, localized toxic plumes cannot disperse, "
            f"forcing children, elderly cardiac patients, and asthmatic residents to inhale carcinogenic PM2.5 and dioxins.\n\n"
            f"REQUESTED ACTION:\n"
            f"1. Immediate deployment of mobile flying enforcement squad to impound/extinguish the source.\n"
            f"2. Imposition of statutory penalties ({info['penalty']}).\n"
            f"3. Provision of clean alternative heating or green waste composting infrastructure to prevent repeat incidents.\n\n"
            f"Failure to act within 24 hours will compel escalation to the National Green Tribunal grievance bench and "
            f"the State Environmental Ombudsman.\n\n"
            f"Respectfully submitted,\n"
            f"Concerned Citizens Coalition & RWA Representatives\n"
            f"{req.ward_or_colony}, {req.city}"
        )

        whatsapp = (
            f"🚨 *COMMUNITY SMOG ALERT — {req.ward_or_colony.upper()}* 🚨\n\n"
            f"⚠️ *Active Hazard*: {info['title']}{landmark_str}\n"
            f"📊 *Threat*: Dense localized PM2.5 plume trapped by morning thermal inversion.\n\n"
            f"🛡️ *Immediate Resident Actions*:\n"
            f"• Keep all street-facing windows firmly sealed.\n"
            f"• Avoid outdoor jogging / morning walks in this quadrant.\n"
            f"• Run home purifiers on High/Turbo.\n"
            f"• Do NOT burn garden leaves or garbage! Use our RWA green composting pit.\n\n"
            f"📞 A formal statutory complaint has been filed under {info['statute'][:45]}...\n"
            f"Together for Clean Air & Safe Lungs! 🌿"
        )

        checklist = [
            f"Capture timestamped geotagged photograph/video of the {req.issue_type.replace('_', ' ')}.",
            "Dispatch the formal grievance letter to the zonal municipal office email and WhatsApp helpline.",
            "Circulate the emergency advisory in the apartment/colony WhatsApp groups to protect residents.",
            "Distribute electric fan heaters to night security staff to eliminate open scrap-wood bonfires."
        ]

        return CommunityGrievanceResponse(
            formal_grievance_letter=letter,
            whatsapp_broadcast_message=whatsapp,
            legal_statutory_basis=info["statute"],
            priority_tier=info["priority"],
            action_checklist=checklist
        )

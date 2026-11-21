"""
Core custom exceptions for PranaAI.

Defines a structured exception hierarchy for urban air quality,
inversion physics, indoor hacks, and generative services.
"""

from typing import Optional, Dict, Any


class PranaAIException(Exception):
    """Base exception for all PranaAI domain errors."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}


class AQIComputationError(PranaAIException):
    """Raised when AQI or pollutant concentration calculation fails."""
    pass


class InvalidLocationError(PranaAIException):
    """Raised when requested city or geo-coordinates cannot be resolved."""
    pass


class RoutineConstraintError(PranaAIException):
    """Raised when routine scheduling constraints cannot be satisfied."""
    pass


class IAQComputationError(PranaAIException):
    """Raised when CADR or indoor ventilation calculations are invalid."""
    pass


class GenAIServiceError(PranaAIException):
    """Raised when external GenAI model fails or rate-limits without fallback."""
    pass

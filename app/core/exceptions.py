"""Core custom exceptions for PranaAI.

Defines a structured exception hierarchy for urban air quality,
inversion physics, indoor hacks, and generative services.
"""

from typing import Any


class PranaAIException(Exception):
    """Base exception for all PranaAI domain errors.

    Attributes:
        message (str): Human-readable error description.
        details (dict[str, Any]): Supplementary contextual diagnostic metadata.
    """

    def __init__(self, message: str, details: dict[str, Any] | None = None) -> None:
        """Initialize PranaAIException.

        Args:
            message (str): Human-readable error explanation.
            details (dict[str, Any] | None): Optional structured diagnostic dictionary.
        """
        super().__init__(message)
        self.message = message
        self.details = details or {}


class AQIComputationError(PranaAIException):
    """Raised when AQI or pollutant concentration calculation fails."""


class InvalidLocationError(PranaAIException):
    """Raised when requested city or geo-coordinates cannot be resolved."""


class RoutineConstraintError(PranaAIException):
    """Raised when routine scheduling constraints cannot be satisfied."""


class IAQComputationError(PranaAIException):
    """Raised when CADR or indoor ventilation calculations are invalid."""


class GenAIServiceError(PranaAIException):
    """Raised when external GenAI model fails or rate-limits without fallback."""

"""Validates that a number is within an upper/lower bound."""

import logging
from dataclasses import dataclass

from ..exceptions.number import HighBoundError, LowBoundError
from ..exceptions.validator import ValidatorError
from ..validator import Validator

logger = logging.getLogger(__name__)


@dataclass
class NumberRange(Validator):
    """Validates that a number is within an upper/lower bound."""

    low: int | float | None
    high: int | float | None
    low_inclusive: bool = True
    high_inclusive: bool = True

    def __post_init__(self):
        if not (self.low and self.high):
            return
        if self.low > self.high:
            logger.warning(
                "The low value (%s) is higher than the high value (%s), setting `low` equal to %s.",
                self.low,
                self.high,
                self.high,
            )
            self.low = self.high

    def _lower_bound(self, number: int | float) -> bool:
        if not self.low:
            return True
        if self.low_inclusive:
            return self.low <= number
        return self.low < number

    def _higher_bound(self, number: int | float) -> bool:
        if not self.high:
            return True
        if self.high_inclusive:
            return self.high >= number
        return self.high > number

    def validate(self, number: int | float) -> None | ExceptionGroup[ValidatorError]:
        exceptions = []
        if not self._lower_bound(number):
            exceptions.append(LowBoundError(bound=self.low, value=number))
        if not self._higher_bound(number):
            exceptions.append(HighBoundError(bound=self.high, value=number))
        return ExceptionGroup("number_range", exceptions) if exceptions else None

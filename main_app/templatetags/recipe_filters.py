from django import template
from fractions import Fraction
import decimal
import logging

logger = logging.getLogger(__name__)

register = template.Library()

@register.filter
def decimal_to_fraction(decimal_value):
    try:
        logger.debug(f"Received input for conversion: {decimal_value}")

        decimal_value = decimal.Decimal(str(decimal_value))
        logger.debug(f"Converted input to Decimal: {decimal_value}")

        fraction = Fraction(decimal_value).limit_denominator(16)
        logger.debug(f"Converted Decimal to Fraction: {fraction}")

        if fraction.numerator > fraction.denominator:
            whole_number = fraction.numerator // fraction.denominator
            remainder = fraction.numerator % fraction.denominator
            logger.debug(
                f"Fraction is improper: {fraction}, Whole number: {whole_number}, Remainder: {remainder}/{fraction.denominator}"
            )

            if remainder == 0:
                return str(whole_number)
            else:
                return f"{whole_number} {remainder}/{fraction.denominator}"

        logger.debug(f"Returning proper fraction: {fraction}")
        return str(fraction)

    except (ValueError, TypeError, decimal.InvalidOperation) as e:
        logger.error(f"Error converting {decimal_value} to fraction: {e}")
        return str(decimal_value)

from django import template
from fractions import Fraction

register = template.Library()

@register.filter
def decimal_to_fraction(decimal_value):
    try:
        fraction = Fraction(decimal_value).limit_denominator(64)

        if fraction.numerator > fraction.denominator:
            whole_number = fraction.numerator // fraction.denominator
            remainder = fraction.numerator % fraction.denominator

            if remainder == 0:
                return str(whole_number)
            else:
                return f"{whole_number} {remainder}/{fraction.denominator}"
        else:
            return str(fraction)
    except (ValueError, TypeError):
        return str(decimal_value)

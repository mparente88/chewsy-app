from django import template
from fractions import Fraction
import decimal
register = template.Library()

@register.filter
def decimal_to_fraction(decimal_value):
    try:

        decimal_value = decimal.Decimal(str(decimal_value))
        
        fraction = Fraction(decimal_value).limit_denominator(16)
        
        if fraction.numerator > fraction.denominator:
            whole_number = fraction.numerator // fraction.denominator
            remainder = fraction.numerator % fraction.denominator
        
            if remainder == 0:
                return str(whole_number)
            else:
                return f"{whole_number} {remainder}/{fraction.denominator}"

        return str(fraction)

    except (ValueError, TypeError, decimal.InvalidOperation) as e:
        return str(decimal_value)

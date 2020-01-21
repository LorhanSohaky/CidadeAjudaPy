from datetime import date

from django.core.validators import BaseValidator
from django.utils.deconstruct import deconstructible
from django.utils.translation import ugettext_lazy as _


def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


@deconstructible
class MinAgeValidator(BaseValidator):
    def compare(self, a, b):
        return calculate_age(a) < b

    message = _("Age must be at least %(limit_value)d.")
    code = 'min_age'

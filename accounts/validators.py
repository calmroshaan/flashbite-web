import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class ComplexPasswordValidator:
    def validate(self, password, user=None):
        if not re.findall('[A-Z]', password):
            raise ValidationError(
                _("The password must contain at least one uppercase letter (A-Z)."),
                code='password_no_upper',
            )
        if not re.findall('[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]', password):
            raise ValidationError(
                _("The password must contain at least one special character (e.g., @, #, $, %)."),
                code='password_no_symbol',
            )

    def get_help_text(self):
        return _("Your password must contain at least one uppercase letter and one special character.")
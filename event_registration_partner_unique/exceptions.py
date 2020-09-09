# Copyright 2016 Antiun Ingeniería S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, exceptions


class UniqueRegistrationPartnerValidationError(exceptions.ValidationError):
    """Base class for this module's validation errors."""

    def __init__(self, *args, **kwargs):
        self._args, self._kwargs = args, kwargs
        value = self._message()
        super(UniqueRegistrationPartnerValidationError, self).__init__(value)

    def _message(self):
        """Format the message."""
        return self.__doc__.format(*self._args, **self._kwargs)


class DuplicatedPartnerError(UniqueRegistrationPartnerValidationError):
    __doc__ = _("Duplicated partners found in event {0}: {1}.")

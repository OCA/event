# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# © 2015 Grupo ESOC Ingeniería de Servicios, S.L.U.

from openerp import _, exceptions


class SeatsPerRegistrationValidationError(exceptions.ValidationError):
    """Base class for this module's validation errors."""
    def __init__(self, *args, **kwargs):
        self._args, self._kwargs = args, kwargs
        value = self._message()
        super(SeatsPerRegistrationValidationError, self).__init__(value)

    def _message(self):
        """Format the message."""
        return self.__doc__.format(*self._args, **self._kwargs)


class NeedAtLeastOneParticipant(SeatsPerRegistrationValidationError):
    __doc__ = _("You need at least one participant per registration.")


class MaxSmallerThanMin(SeatsPerRegistrationValidationError):
    __doc__ = _("The maximum of participants per registration cannot "
                "be smaller than the minimum.")


class MaxPerRegisterBiggerThanMaxPerEvent(SeatsPerRegistrationValidationError):
    __doc__ = _("The maximum of participants per registration "
                "cannot be bigger than the maximum of participants "
                "for this event.")


class PreviousRegistrationsFail(SeatsPerRegistrationValidationError):
    __doc__ = _("There are already registrations that don't fit in "
                "the new limits of participants per registration. "
                "Change them before setting the limits. "
                "The error was: {.value}")


class TooFewParticipants(SeatsPerRegistrationValidationError):
    __doc__ = _("You cannot register less than {} participants.")


class TooManyParticipants(SeatsPerRegistrationValidationError):
    __doc__ = _("You cannot register more than {} participants.")

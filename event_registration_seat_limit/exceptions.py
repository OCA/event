# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# © 2015 Grupo ESOC Ingeniería de Servicios, S.L.U.

from openerp import _, exceptions


class SeatsPerRegistrationError(exceptions.ValidationError):
    def __init__(self, value):
        super(SeatsPerRegistrationError, self).__init__(value)
        self.name = _("Error in the limits of participants per registration.")


class NeedAtLeastOneParticipant(SeatsPerRegistrationError):
    def __init__(self,
                 value=_("You need at least one participant "
                         "per registration.")):
        super(NeedAtLeastOneParticipant, self).__init__(value)


class MaxSmallerThanMin(SeatsPerRegistrationError):
    def __init__(self,
                 value=_("The maximum of participants per registration cannot "
                         "be smaller than the minimum.")):
        super(MaxSmallerThanMin, self).__init__(value)


class MaxPerRegisterBiggerThanMaxPerEvent(SeatsPerRegistrationError):
    def __init__(self,
                 value=_("The maximum of participants per registration "
                         "cannot be bigger than the maximum of participants "
                         "for this event.")):
        super(MaxPerRegisterBiggerThanMaxPerEvent, self).__init__(value)


class PreviousRegistrationsFail(SeatsPerRegistrationError):
    def __init__(self,
                 previous_exception,
                 value=_("There are already registrations that don't fit in "
                         "the new limits of participants per registration. "
                         "Change them before setting the limits. "
                         "The error was: '%s'")):
        self.previous_exception = previous_exception
        super(PreviousRegistrationsFail, self).__init__(
            value % previous_exception.value)


class TooFewParticipants(SeatsPerRegistrationError):
    def __init__(self,
                 min,
                 value=_("You cannot register less than %d participants.")):
        self.min = min
        super(TooFewParticipants, self).__init__(value % min)


class TooManyParticipants(SeatsPerRegistrationError):
    def __init__(self,
                 max,
                 value=_("You cannot register more than %d participants.")):
        self.max = max
        super(TooManyParticipants, self).__init__(value % max)

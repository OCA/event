# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# © 2015 Grupo ESOC Ingeniería de Servicios, S.L.U. - Jairo Llopis

from openerp import _, exceptions


class TrainingTrackValidationError(exceptions.ValidationError):
    def __init__(self, value):
        super(TrainingTrackValidationError, self).__init__(value)
        self.name = _("Error(s) with the training track data.")


class DifferentEventError(TrainingTrackValidationError):
    def __init__(self,
                 registration,
                 track,
                 value=_("Registration %(registration)s and track %(track)s "
                         "belong to different events.")):
        value = value % {
            "registration": registration.name_get()[0][1],
            "track": track.name_get()[0][1],
        }
        self.registration = registration
        self.track = track
        super(DifferentEventError, self).__init__(value)

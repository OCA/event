# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# © 2015 Grupo ESOC Ingeniería de Servicios, S.L.U.

from openerp import _, exceptions


class TrainingValidationError(exceptions.ValidationError):
    def __init__(self, value):
        super(TrainingValidationError, self).__init__(value)
        self.name = _("Error(s) with the training data.")


class WrongDurationType(TrainingValidationError):
    def __init__(self,
                 invalid_hour_type,
                 valid_hour_types,
                 value=_("Hour type '%(hour_type)s' is not among the valid "
                         "ones defined in the training type "
                         "(%(training_type)s).")):
        self.invalid_hour_type = invalid_hour_type
        self.valid_hour_types = valid_hour_types
        value = value % {"hour_type": invalid_hour_type.name,
                         "training_type": ", ".join(valid_hour_types
                                                    .mapped("name"))}
        super(WrongDurationType, self).__init__(value)

# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# © 2015 Grupo ESOC Ingeniería de Servicios, S.L.U. - Jairo Llopis

from openerp import _, exceptions


class TrainingValidationError(exceptions.ValidationError):
    def __init__(self, value):
        super(TrainingValidationError, self).__init__(value)
        self.name = _("Error(s) with the training data.")


class TrainingValidationWarning(exceptions.Warning):
    def __init__(self, value):
        super(TrainingValidationWarning, self).__init__(value)
        self.name = _("Error(s) with the training data.")


class GradeLimitError(TrainingValidationError):
    def __init__(self,
                 registration,
                 value=_("Grade %(grade)f for %(student)s does not fit "
                         "between %(min)f and %(max)f.")):
        value = value % {
            "grade": registration.grade,
            "student": registration.name,
            "min": registration.event_id.training_action_id.grade_min,
            "max": registration.event_id.training_action_id.grade_max,
        }
        self.registration = registration
        super(GradeLimitError, self).__init__(value)


class GradeLimitIncoherentError(TrainingValidationError):
    pass


class NoMaterialsToDeliverError(TrainingValidationError):
    def __init__(self, value=_("No materials are set in the event.")):
        super(NoMaterialsToDeliverError, self).__init__(value)


class ChangeDeliveredMaterialsWarning(TrainingValidationWarning):
    def __init__(self,
                 value=_("Yoy are changing materials that have been delivered "
                         "already.")):
        super(ChangeDeliveredMaterialsWarning, self).__init__(value)


class WrongDurationTypeError(TrainingValidationError):
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
        super(WrongDurationTypeError, self).__init__(value)

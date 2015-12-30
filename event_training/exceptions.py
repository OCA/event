# -*- coding: utf-8 -*-
# © 2015 Grupo ESOC Ingeniería de Servicios, S.L.U. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from __future__ import unicode_literals
from openerp import _, exceptions


class TrainingValidationError(exceptions.ValidationError):
    """Base class for this module's validation errors."""
    def __init__(self, *args, **kwargs):
        self._args, self._kwargs = args, kwargs
        value = self._message()
        super(TrainingValidationError, self).__init__(value)

    def _message(self):
        """Format the message."""
        return self.__doc__.format(*self._args, **self._kwargs)


class GradeLimitOverflowError(TrainingValidationError):
    __doc__ = _("Minimum grade cannot be higher than maximum.")


class GradePassingOverflowError(TrainingValidationError):
    __doc__ = _("Passing grade must be between minimum and maximum grades.")


class StudentGradeOutsideLimitsError(TrainingValidationError):
    __doc__ = _("Grade {grade} for {student} does not fit "
                "between {min} and {max}.")

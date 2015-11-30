# -*- coding: utf-8 -*-
# © 2015 Grupo ESOC Ingeniería de Servicios, S.L.U. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, exceptions


class EventRegistrationProductDeliverValidationError(
        exceptions.ValidationError):
    """Base class for this module's validation errors."""
    def __init__(self, *args, **kwargs):
        self._args, self._kwargs = args, kwargs
        value = self._message()
        super(EventRegistrationProductDeliverValidationError, self).__init__(
            value)

    def _message(self):
        """Format the message."""
        return self.__doc__.format(*self._args, **self._kwargs)


class NoProductsToDeliverError(EventRegistrationProductDeliverValidationError):
    __doc__ = _("Event has no products set to deliver.")

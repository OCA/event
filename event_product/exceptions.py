# -*- coding: utf-8 -*-
# © 2015 Grupo ESOC Ingeniería de Servicios, S.L.U. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, exceptions


class EventProductValidationError(exceptions.ValidationError):
    """Base class for this module's validation errors."""
    def __init__(self, *args, **kwargs):
        self._args, self._kwargs = args, kwargs
        value = self._message()
        super(EventProductValidationError, self).__init__(value)

    def _message(self):
        """Format the message."""
        return self.__doc__.format(*self._args, **self._kwargs)


class EventAndTicketError(EventProductValidationError):
    __doc__ = _("It cannot be a whole event and a ticket at the same time.")


class ProductIsNotEventError(EventProductValidationError):
    __doc__ = _("Product {} is not for events.")


class TypeMismatchError(EventProductValidationError):
    __doc__ = _("Product has type {product_type}, but event has {event_type}.")

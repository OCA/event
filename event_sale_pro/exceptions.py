# -*- coding: utf-8 -*-
# © 2015 Grupo ESOC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import exceptions


class EventSaleProValidationError(exceptions.ValidationError):
    """Base validaton error class."""


class MultipleEventsError(EventSaleProValidationError):
    """The user tried to generate quotations for multiple events at once."""

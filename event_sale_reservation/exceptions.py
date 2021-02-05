# Copyright 2021 Tecnativa - Jairo Llopis
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import exceptions


class TicketAndReservationError(exceptions.ValidationError):
    pass


class ReservationWithoutEventTypeError(exceptions.ValidationError):
    pass

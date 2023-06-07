# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class Company(models.Model):
    _inherit = "res.company"

    cancelled_order_message = fields.Char(
        help="Message displayed, if order is cancel before the payment process.",
        default="Your order has been cancelled, before the payment processed. Please "
        "go back to our event page to register again.",
        translate=True,
    )
    no_more_seats_on_event_message = fields.Char(
        help="Message displayed, if the last seats of the event have been sold before "
        "the current payment process. (Availability per event)",
        default="The last available seats have just been sold. Please go back to our "
        "event page to register to another event.",
        translate=True,
    )
    no_more_ticket_message = fields.Char(
        help="Message displayed, if the last tickets have been sold before the "
        "current payment process. (Availability per ticket)",
        default="The last available tickets have just been sold. Please go back to "
        "our event page to register to another event.",
        translate=True,
    )

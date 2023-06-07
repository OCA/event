from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    cancelled_order_message = fields.Char(
        related="company_id.cancelled_order_message", readonly=False
    )
    no_more_seats_on_event_message = fields.Char(
        related="company_id.no_more_seats_on_event_message", readonly=False
    )
    no_more_ticket_message = fields.Char(
        related="company_id.no_more_ticket_message", readonly=False
    )

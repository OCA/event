# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)

from odoo import api, fields, models


class EventEventTicket(models.Model):
    _inherit = "event.event.ticket"

    show_in_website = fields.Boolean(default=True)


class EventTemplateTicket(models.Model):
    _inherit = "event.type.ticket"

    show_in_website = fields.Boolean(default=True)

    @api.model
    def _get_event_ticket_fields_whitelist(self):
        """Add website specific field to copy from template to ticket"""
        return super(EventTemplateTicket, self)._get_event_ticket_fields_whitelist() + [
            "show_in_website"
        ]

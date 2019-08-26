# Copyright 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class WizardModel(models.TransientModel):
    _name = "crm.lead.event.pick"
    _description = "Crm Lead Event Pick"

    lead_id = fields.Many2one(
        "crm.lead",
        "Lead/Opportunity",
        default=lambda self: self._default_lead_id(),
        help="Lead/Opportunity from where to get contact information.")
    event_id = fields.Many2one(
        "event.event",
        "Event",
        required=True,
        help="Event where the registration will be created.")

    @api.model
    def _default_lead_id(self):
        return self.env.context["active_id"]

    @api.multi
    def action_accept(self):
        self.lead_id.action_generate_event_registration(self.event_id)

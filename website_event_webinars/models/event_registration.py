# Copyright 2019 Chris Mann - github.com/chrisandrewmann
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class EventRegistration(models.Model):
    _inherit = 'event.registration'

    webinar_id = fields.Char(
        string='Webinar ID/URL',
        related='event_id.webinar_id',
        store=False,
        readonly=True
        )

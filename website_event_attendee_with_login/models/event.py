# Copyright 2019 Chris Mann - github.com/chrisandrewmann
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class EventEvent(models.Model):
    _inherit = 'event.event'

    website_attendee_require_login = fields.Boolean(
        string='Require attendee login for tickets',
        help='If set, an attendee must have their own account '
             'to register for an event. All tickets limited to '
             'their logged-in name/email.',
    )

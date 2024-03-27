# Copyright 2024 Tecnativa S.L. - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class EventRegistration(models.Model):
    _inherit = "event.registration"

    cancelled_from_event = fields.Boolean(
        help="Technical field to distinguish those registrations which where cancelled "
        "from the event so we can, for example send them scheduled mails after the "
        "cancellation but not if the were cancelled before that"
    )

    def action_cancel(self):
        res = super().action_cancel()
        if self.env.context.get("cancelled_from_event"):
            self.cancelled_from_event = True
        return res

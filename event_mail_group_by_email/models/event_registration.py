# Copyright 2021 Camptocamp SA - Iván Todorovich
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class EventRegistration(models.Model):
    _inherit = "event.registration"

    def _group_by_email(self):
        """Returns a list of attendee recordsets, grouped by email address"""
        res = []
        email_to_rec_ids = {}
        for rec in self:
            email = rec.email or rec.partner_id.email
            # If there's no email, add directly to result, ungrouped
            if email:
                email_to_rec_ids.setdefault(email, []).append(rec.id)
            else:  # pragma: no cover
                res.append(rec)
        # Add groups to result
        for __, rec_ids in email_to_rec_ids.items():
            res.append(self.browse(rec_ids))
        return res

# -*- coding: utf-8 -*-
# © 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class MultiImage(models.Model):
    _inherit = "base_multi_image.image"

    event_published = fields.Boolean(
        compute="_compute_event_published",
        store=True,
    )

    @api.multi
    @api.depends("owner_model", "owner_id")
    def _compute_event_published(self):
        """Know if this image is from a published event."""
        for s in self:
            if s.owner_model == "event.event":
                s.event_published = (self.env[s.owner_model].sudo()
                                     .browse(s.owner_id).published)
            else:
                s.event_published = False

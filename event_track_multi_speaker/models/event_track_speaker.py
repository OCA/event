# Copyright 2017 David Vidal<david.vidal@tecnativa.com>
# Copyright 2017 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class EventTrackSpeaker(models.Model):
    _name = "event.track.speaker"
    _description = "Track Speaker"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(related="partner_id.name")
    email = fields.Char(related="partner_id.email")
    phone = fields.Char(related="partner_id.phone")
    biography = fields.Html(related="partner_id.website_description")
    function = fields.Char(related="partner_id.function")
    image = fields.Image(related="partner_id.image_256")
    partner_id = fields.Many2one("res.partner", string="Contact")
    track_ids = fields.Many2many(
        comodel_name="event.track",
        string="Tracks",
    )
    status = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("waiting", "Waiting"),
            ("validated", "Validated"),
        ],
        default="draft",
    )
    event_id = fields.Many2one(
        "event.event", compute="_compute_event", string="Event", store=True
    )

    @api.depends("track_ids.event_id")
    def _compute_event(self):
        self.event_id = self.track_ids[0].event_id

    @api.constrains("track_ids")
    def _check_unique_event(self):
        for speaker in self:
            if len(speaker.mapped("track_ids").mapped("event_id")) > 1:
                raise UserError(_("Speakers should belong to only one event."))

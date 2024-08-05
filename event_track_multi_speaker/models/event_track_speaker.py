# Copyright 2017 David Vidal<david.vidal@tecnativa.com>
# Copyright 2017 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


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
        string="Speakers",
    )
    status = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("waiting", "Waiting"),
            ("validated", "Validated"),
        ]
    )

    # @api.depends("track_ids.speaker_ids")
    # def compute_tracks(self):
    #     tracks = self.env["event.track"].search([]).filtered(
    #             lambda : self in
    #         )
    #     for track in self.track_ids:
    #         speakers += track.speaker_ids

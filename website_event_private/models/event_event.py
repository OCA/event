# Copyright 2023- Le Filament (https://le-filament.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import uuid

from odoo import api, fields, models


class Event(models.Model):
    _inherit = "event.event"

    access_token = fields.Char(
        string="Security Token", compute="_compute_access_token", store=True, copy=False
    )
    event_share_link = fields.Char(
        string="Event link",
        compute="_compute_event_share_link",
    )
    event_privacy = fields.Selection(
        [
            ("public", "Public"),
            ("private_displayed", "Private displayed"),
            ("private_hidden", "Private hidden"),
        ],
        string="Event privacy",
        default="public",
        required=True,
        readonly=False,
        store=True,
        compute="_compute_event_privacy",
    )

    # ------------------------------------------------------
    # Computed fields / Search Fields
    # ------------------------------------------------------
    @api.depends("event_type_id")
    def _compute_event_privacy(self):
        for event in self:
            event.event_privacy = event.event_type_id.event_privacy

    @api.depends("event_privacy")
    def _compute_access_token(self):
        for event in self:
            if event.event_privacy != "public" and not event.access_token:
                event.access_token = str(uuid.uuid4())

    def _compute_event_share_link(self):
        for event in self:
            if event.id and event.access_token and event.event_privacy != "public":
                event.event_share_link = (
                    event.get_base_url()
                    + "/event/"
                    + str(event.id)
                    + "?access_token="
                    + event.access_token
                )
            else:
                event.event_share_link = ""

    # ------------------------------------------------------
    # Inherit parent
    # ------------------------------------------------------
    @api.model
    def _search_get_detail(self, website, order, options):
        result = super(Event, self)._search_get_detail(website, order, options)
        if not self.env.user.has_group("website.group_website_restricted_editor"):
            result["base_domain"].append([("event_privacy", "!=", "private_hidden")])

        return result

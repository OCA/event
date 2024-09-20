# Copyright 2024 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0).
from odoo import api, fields, models


class EventEvent(models.Model):
    _inherit = "event.event"

    seats_reserved_unconfirmed = fields.Integer(
        string="Number of Reserved Attendees",
        store=False,
        readonly=True,
        compute="_compute_seats",
    )

    @api.depends("seats_max", "registration_ids.state", "registration_ids.active")
    def _compute_seats(self):
        # Override the original method to add the new state and the compute for the new field
        # initialize fields to 0
        res = super()._compute_seats()
        counts = dict()
        if self.ids:
            groups = self.env["event.registration"].read_group(
                [
                    ("event_id", "in", self.ids),
                    ("state", "=", "reserved"),
                ],
                groupby=["event_id"],
                fields=["event_id"],
            )
            counts = {g["event_id"][0]: g["event_id_count"] for g in groups}

        # compute seats_available and expected
        for event in self:
            event.seats_reserved_unconfirmed = counts.get(event.id, 0)
            if event.seats_max > 0:
                event.seats_available = event.seats_max - (
                    event.seats_reserved
                    + event.seats_used
                    + event.seats_reserved_unconfirmed
                )

            event.seats_expected = (
                event.seats_unconfirmed
                + event.seats_reserved_unconfirmed
                + event.seats_reserved
                + event.seats_used
            )
        return res

# Copyright 2017-19 Tecnativa - David Vidal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0).
from odoo import api, models


class EventSession(models.Model):
    _inherit = "event.session"

    @api.depends("registration_ids.qty")
    def _compute_seats(self):
        for session in self:
            if not session.event_id.registration_multi_qty:
                return super()._compute_seats()
            vals = {
                "seats_unconfirmed": 0,
                "seats_reserved": 0,
                "seats_used": 0,
                "seats_available": 0,
                "seats_available_expected": 0,
                "seats_available_pc": 0,
            }
            registrations = self.env["event.registration"].read_group(
                [
                    ("session_id", "=", session.id),
                    ("state", "in", ["draft", "open", "done"]),
                ],
                ["state", "qty"],
                ["state"],
            )
            for registration in registrations:
                if registration["state"] == "draft":
                    vals["seats_unconfirmed"] += registration["qty"]
                elif registration["state"] == "open":
                    vals["seats_reserved"] += registration["qty"]
                elif registration["state"] == "done":
                    vals["seats_used"] += registration["qty"]
            vals["seats_expected"] = (
                vals["seats_unconfirmed"] + vals["seats_reserved"] + vals["seats_used"]
            )
            if session.seats_max > 0:
                vals["seats_available"] = session.seats_max - (
                    vals["seats_reserved"] + vals["seats_used"]
                )
                vals["seats_available_expected"] = (
                    session.seats_max - vals["seats_expected"]
                )
                vals["seats_available_pc"] = (
                    vals["seats_expected"] * 100 / float(session.seats_max)
                )
            session.update(vals)

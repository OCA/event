# Copyright 2017-19 Tecnativa - David Vidal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0).
from odoo import api, models


class EventSession(models.Model):
    _inherit = "event.session"

    @api.depends("registration_ids.qty")
    def _compute_seats(self):
        multi_qty_sessions = self.filtered("event_id.registration_multi_qty")
        res = super(EventSession, self - multi_qty_sessions)._compute_seats()
        for session in multi_qty_sessions:
            vals = {
                "seats_reserved": 0,
                "seats_used": 0,
                "seats_available": 0,
            }
            registrations = self.env["event.registration"].read_group(
                [
                    ("session_id", "=", session.id),
                    ("state", "in", ["open", "done"]),
                ],
                ["state", "qty"],
                ["state"],
            )
            for registration in registrations:
                if registration["state"] == "open":
                    vals["seats_reserved"] += registration["qty"]
                elif registration["state"] == "done":
                    vals["seats_used"] += registration["qty"]
            vals["seats_taken"] = vals["seats_reserved"] + vals["seats_used"]
            if session.seats_max > 0:
                vals["seats_available"] = session.seats_max - (
                    vals["seats_reserved"] + vals["seats_used"]
                )
            session.update(vals)
        return res

    @api.depends("registration_ids.qty")
    def _compute_seats_unconfirmed(self):
        multi_qty_sessions = self.filtered("event_id.registration_multi_qty")
        res = super(
            EventSession, self - multi_qty_sessions
        )._compute_seats_unconfirmed()
        for session in multi_qty_sessions:
            registrations = self.env["event.registration"].read_group(
                [
                    ("session_id", "=", session.id),
                    ("state", "=", "draft"),
                ],
                ["qty:sum"],
                [],
            )
            session.seats_unconfirmed = registrations[0]["qty"] if registrations else 0
        return res

# Copyright 2026 SportJoe GmbH
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
from odoo import fields, models

TAKEN_STATES = ("open", "done")


class EventRegistration(models.Model):
    _inherit = "event.registration"

    waitlist_entry_id = fields.Many2one(
        "event.waitlist",
        string="Waiting List Entry",
        index="btree_not_null",
        ondelete="set null",
        readonly=True,
        copy=False,
    )

    def _waitlist_freed_events(self, vals):
        """Events in which this write frees seats."""
        frees = (vals.get("state") and vals["state"] not in TAKEN_STATES) or (
            "active" in vals and not vals["active"]
        )
        if not frees:
            return self.env["event.event"]
        return self.filtered(lambda r: r.state in TAKEN_STATES and r.active).event_id

    def write(self, vals):
        events = self._waitlist_freed_events(vals)
        if {"event_id", "event_ticket_id"} & set(vals):
            events |= self.filtered(lambda r: r.state in TAKEN_STATES).event_id
        res = super().write(vals)
        if events:
            events._waitlist_process()
        return res

    def unlink(self):
        events = self.filtered(lambda r: r.state in TAKEN_STATES and r.active).event_id
        res = super().unlink()
        if events.exists():
            events.exists()._waitlist_process()
        return res

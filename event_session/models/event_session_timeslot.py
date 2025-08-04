# Copyright 2021 Moka Tourisme (https://www.mokatourisme.fr).
# @author Iván Todorovich <ivan.todorovich@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import time

from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.misc import format_duration


def time_as_float_time(tm):
    hours, minutes = tm.tm_hour, tm.tm_min
    return hours + (minutes / 60)


class EventSessionTimeslot(models.Model):
    _name = "event.session.timeslot"
    _description = "Event Session Timeslot"
    _order = "time"
    _rec_name = "time"

    _sql_constraints = [
        ("unique_time", "UNIQUE(time)", "The timeslot has to be unique"),
        (
            "valid_time",
            "CHECK(time >= 0 AND time <= 24)",
            "Time has to be between 0:00 and 23:59",
        ),
    ]

    time = fields.Float(required=True)

    @api.depends("time")
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = format_duration(rec.time)

    @api.model
    def name_create(self, name):
        try:
            tm = time.strptime(name.strip(), "%H:%M")
        except ValueError as e:
            raise ValidationError(
                self.env._("The timeslot has to be defined in HH:MM format")
            ) from e
        vals = {"time": time_as_float_time(tm)}
        record = self.create(vals)
        return (record.id, record.display_name)

    def _prepare_session_extra_vals(self):
        """Hook to prepare values to apply on sessions created from this timeslot"""
        self.ensure_one()
        return {}

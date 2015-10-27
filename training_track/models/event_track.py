# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# © 2015 Grupo ESOC Ingeniería de Servicios, S.L.U.

from openerp import api, fields, models


class EventTrack(models.Model):
    """Expand event tracks with training duration types.

    This is used to calculate how many hours of each type have been fulfilled.
    """
    _inherit = "event.track"

    duration_type_id = fields.Many2one(
        "training.duration_type",
        "Training hour type",
        help="Training hour type of this track, if it belongs to a training "
             "group.")

    monitor_attendance = fields.Boolean(
        help="Should this track use attendance monitoring?")

    attendee_ids = fields.Many2many(
        "event.registration",
        string="Attendees",
        domain="[('event_id', '=', event_id)]",
        help="People that attended this track.")

    @api.constrains("attendee_ids", "event_id")
    def _check_attendees_events(self):
        """Enforce same event in registration and track."""
        self.mapped("attendee_ids")._check_attended_tracks_events()

    @api.onchange("duration_type_id")
    def _onchange_monitor_attendance(self):
        """Set attendance monitoring."""
        for s in self:
            s.monitor_attendance = s.duration_type_id.monitor_attendance

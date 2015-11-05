# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# © 2015 Grupo ESOC Ingeniería de Servicios, S.L.U. - Jairo Llopis

from openerp import api, fields, models
from .. import exceptions


class EventRegistration(models.Model):
    _inherit = "event.registration"

    attended_track_ids = fields.Many2many(
        "event.track",
        string="Attended tracks",
        domain="""[('event_id', '=', event_id),
                   ('monitor_attendance', '=', True)]""",
        help="Tracks of this event that this person attended.")

    @api.constrains("attended_track_ids", "event_id")
    def _check_attended_tracks_events(self):
        """Enforce same event in registration and track."""
        for registration in self:
            failure_tracks = registration.attended_track_ids.filtered(
                lambda track: track.event_id != registration.event_id)
            if failure_tracks:
                raise exceptions.DifferentEventError(
                    registration, failure_tracks[0])

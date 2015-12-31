# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# © 2015 Grupo ESOC Ingeniería de Servicios, S.L.U. - Jairo Llopis

from openerp import _, api, exceptions, fields, models


class EventRegistration(models.Model):
    _inherit = "event.registration"

    attended_track_ids = fields.Many2many(
        "event.track",
        string="Attended tracks",
        domain="""[('event_id', '=', event_id),
                   ('monitor_attendance', '=', True)]""",
        help="Tracks of this event that this person attended.")

    @api.multi
    @api.constrains("attended_track_ids", "event_id")
    def _check_attended_tracks_events(self):
        """Enforce same event in registration and track."""
        for s in self:
            failure_tracks = s.attended_track_ids.filtered(
                lambda track: track.event_id != s.event_id)
            if failure_tracks:
                values = {
                    "registration": s.display_name,
                    "track": failure_tracks[0].display_name,
                }
                raise exceptions.ValidationError(
                    _("Registration %(registration)s and track %(track)s "
                      "belong to different events.") % values)


class EventTrack(models.Model):
    _inherit = "event.track"

    expected_duration_type_ids = fields.Many2many(
        readonly=True,
        related="event_id.type.expected_duration_type_ids")
    duration_type_id = fields.Many2one(
        "event.training.duration.type",
        "Training hours type",
        help="Training hours type of this track.")
    monitor_attendance = fields.Boolean(
        readonly=True,
        related="duration_type_id.monitor_attendance",
        help="Should this track use attendance monitoring?")
    registration_ids = fields.Many2many(
        "event.registration",
        string="Attendees",
        domain="[('event_id', '=', event_id)]",
        help="People that attended this track.")

    @api.multi
    @api.constrains("registration_ids", "event_id")
    def _check_attendees_events(self):
        """Enforce same event in registration and track."""
        self.mapped("registration_ids")._check_attended_tracks_events()

    @api.multi
    @api.onchange("expected_duration_type_ids")
    def _onchange_expected_durations_change_durations_domain(self):
        """Change the domain for ``duration_type_id`` as needed.

        This cannot be done in the ``domain`` field attribute because it
        depends on a Many2one field.
        """
        return {
            "domain": {
                "duration_type_id": [
                    ("id", "in", self.expected_duration_type_ids.ids),
                ],
            },
        }


class EventType(models.Model):
    _inherit = "event.type"

    expected_duration_type_ids = fields.Many2many(
        "event.training.duration.type",
        string="Expected duration types",
        help="Hour types expected in this type of course. For example, "
             "a training of type 'mixed' may expect durations of types "
             "'on-site' and 'online'.")

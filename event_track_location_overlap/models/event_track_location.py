# Copyright 2017 Tecnativa - Jairo Llopis
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from datetime import timedelta

from odoo import _, api, exceptions, fields, models


class EventTrackLocation(models.Model):
    _inherit = "event.track.location"

    overlappable = fields.Boolean(help="Can this location have simultaneous tracks?")

    @api.constrains("overlappable")
    def _check_overlappable(self):
        for item in self:
            item._check_overlappable_one()

    def _check_overlappable_one(self):
        """Ensure no overlaps happen with this location."""
        # Skip locations that can be overlapped
        if self.overlappable:
            return
        # Get tracks that could produce an overlap
        remaining_tracks = self.env["event.track"].search(
            [("location_id", "=", self.id), ("stage_id.is_cancel", "=", False)]
        )
        # Compare tracks overlapping among themselves
        while remaining_tracks:
            # Extract some track from the set
            a_track = remaining_tracks[0]
            remaining_tracks -= a_track
            # Get track A's dates
            a_start = a_track.date
            a_end = a_start + timedelta(hours=a_track.duration)
            # Compare with all remaining tracks
            for b_track in remaining_tracks:
                # Get track B's dates
                b_start = b_track.date
                b_end = b_start + timedelta(hours=b_track.duration)
                # Fail if there's an overlap
                if b_start <= a_end and b_end >= a_start:
                    msg = _(
                        "Track %(one)s (from event %(one_event)s) and "
                        "track %(other)s (from event %(other_event)s) would "
                        "overlap in the same location %(location)s"
                    )
                    params = {
                        "location": self.display_name,
                        "one_event": a_track.event_id.display_name,
                        "one": a_track.display_name,
                        "other_event": b_track.event_id.display_name,
                        "other": b_track.display_name,
                    }
                    raise exceptions.ValidationError(msg % params)

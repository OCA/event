# -*- coding: utf-8 -*-
# Copyright 2017 Tecnativa - Jairo Llopis
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from datetime import timedelta
from openerp import _, api, exceptions, fields, models


class EventTrackLocation(models.Model):
    _inherit = "event.track.location"

    overlappable = fields.Boolean(
        help="Can this location have simultaneous tracks?"
    )

    # TODO oca.decorators.foreach() in v12
    @api.one  # pragma pylint: disable=api-one-deprecated
    @api.constrains("overlappable")
    def _check_overlappable(self):
        """Ensure no overlaps happen with this location."""
        # Skip locations that can be overlapped
        if self.overlappable:
            return
        # Get track states that can always overlap
        skip_track_states = self.env.context.get(
            "skip_track_states",
            ["draft", "refused", "cancel"],
        )
        # Get tracks that could produce an overlap
        remaining_tracks = self.env["event.track"].search([
            ("location_id", "=", self.id),
            ("state", "not in", skip_track_states),
        ])
        # Compare tracks overlapping among themselves
        while remaining_tracks:
            # Extract some track from the set
            a_track = remaining_tracks[0]
            remaining_tracks -= a_track
            # Get track A's dates
            a_start = fields.Datetime.from_string(a_track.date)
            a_end = a_start + timedelta(hours=a_track.duration)
            # Compare with all remaining tracks
            for b_track in remaining_tracks:
                # Get track B's dates
                b_start = fields.Datetime.from_string(b_track.date)
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

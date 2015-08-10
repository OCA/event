# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# © 2015 Grupo ESOC Ingeniería de Servicios, S.L.U.

from openerp.tests.common import TransactionCase


class TrainingTrackCase(TransactionCase):
    """Test behavior of training tracks."""

    def test_duration_type_set(self):
        """Set a duration type in a track that has no one."""

        track = self.env.ref("website_event_track.event_track30")
        duration_type = self.env.ref("training.duration_type_online")

        track.duration_type_id = duration_type

        self.assertEqual(track.duration_type_id, duration_type)

    def test_duration_type_unset(self):
        """Remove a duration type from a track that has one."""

        track = self.env.ref("website_event_track.event_track20")

        track.duration_type_id = False

        self.assertFalse(track.duration_type_id)

    def test_duration_type_change(self):
        """Change a duration type to another one."""

        track = self.env.ref("website_event_track.event_track21")
        duration_type = self.env.ref("training.duration_type_on_site")

        track.duration_type_id = duration_type

        self.assertEqual(track.duration_type_id, duration_type)

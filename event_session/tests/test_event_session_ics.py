# Copyright 2022 Moka Tourisme (https://www.mokatourisme.fr).
# @author Iván Todorovich <ivan.todorovich@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import HttpCase, tagged


@tagged("-at_install", "post_install")
class TestEventSessionICS(HttpCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.event_session = cls.env.ref("event_session.event_session_007_1_16_00")
        cls.event = cls.event_session.event_id

    def test_event_session_ics_file(self):
        self.authenticate("admin", "admin")
        res = self.url_open(f"/event/session/{self.event_session.id}/ics")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers["Content-Type"], "application/octet-stream")
        self.assertTrue(res.content.startswith(b"BEGIN:VCALENDAR"))

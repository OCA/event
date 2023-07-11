# Copyright 2022 Moka Tourisme (https://www.mokatourisme.fr).
# @author Iván Todorovich <ivan.todorovich@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields
from odoo.tests import TransactionCase


class CommonEventSessionCase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.stage_new = cls.env.ref("event.event_stage_new")
        cls.stage_done = cls.env.ref("event.event_stage_done")

    def assertSessionDates(self, sessions, expected):
        for session, date in zip(sessions, expected):
            local_date = fields.Datetime.context_timestamp(
                session._set_tz_context(), session.date_begin
            )
            local_date_str = fields.Datetime.to_string(local_date)
            self.assertEqual(local_date_str, date)

    def _wizard_generate_sessions(self, vals):
        wizard = self.env["wizard.event.session"].create(vals)
        sessions_domain = wizard.action_create_sessions()["domain"]
        return self.env["event.session"].search(sessions_domain)

# Copyright 2021 Camptocamp SA - Iván Todorovich
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from dateutil.relativedelta import relativedelta

from odoo import fields
from odoo.tests import common


class TestMailSchedule(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.template_badge = cls.env.ref("event.event_registration_mail_template_badge")
        cls.template_subscription = cls.env.ref("event.event_subscription")
        cls.template_reminder = cls.env.ref("event.event_reminder")
        cls.event = cls.env["event.event"].create(
            {
                "name": "Test Event",
                "auto_confirm": False,
                "date_begin": fields.Datetime.now() + relativedelta(days=1),
                "date_end": fields.Datetime.now() + relativedelta(days=15),
            }
        )
        # Registrations
        cls.reg_1 = cls.env["event.registration"].create(
            {
                "event_id": cls.event.id,
                "name": "Jon Snow",
                "email": "the.black.crow@nigthswatch.org",
            }
        )
        cls.reg_2 = cls.env["event.registration"].create(
            {
                "event_id": cls.event.id,
                "name": "Samwell Tarly",
                "email": "the.black.crow@nigthswatch.org",
            }
        )
        cls.reg_3 = cls.env["event.registration"].create(
            {
                "event_id": cls.event.id,
                "name": "Daenerys Targaryen",
                "email": "queen.of.everything@fire.io",
            }
        )
        cls.registrations = cls.reg_1 | cls.reg_2 | cls.reg_3

    def _get_event_registrations_mails(self, registration):
        return self.env["mail.mail"].search(
            [("model", "=", "event.registration"), ("res_id", "in", registration.ids)]
        )

    def test_00_after_sub_grouped(self):
        # Configure event
        self.event.event_mail_ids = [
            (5, 0),
            (
                0,
                0,
                {
                    "interval_unit": "now",
                    "interval_type": "after_sub",
                    "group_by_email": True,
                    "template_id": self.template_badge.id,
                },
            ),
        ]
        # After registration confirmation, mails should be grouped
        self.registrations.confirm_registration()
        mails = self._get_event_registrations_mails(self.registrations)
        self.assertEqual(len(mails), 2, "Only two emails should've been sent")
        # Reg 1
        reg_1_mails = self._get_event_registrations_mails(self.reg_1)
        self.assertEqual(len(reg_1_mails), 1, "Reg 1 should've received 1 email.")
        self.assertEqual(
            len(reg_1_mails.attachment_ids), 2, "Both badges should be in the email."
        )
        # Reg 2
        reg_2_mails = self._get_event_registrations_mails(self.reg_2)
        self.assertEqual(
            len(reg_2_mails), 0, "Reg 2 shouldn't have received any email."
        )
        # Reg 3
        reg_3_mails = self._get_event_registrations_mails(self.reg_3)
        self.assertEqual(len(reg_3_mails), 1, "Reg 3 should've received 1 email.")
        self.assertEqual(
            len(reg_3_mails.attachment_ids), 1, "Only one badge in the email."
        )

    def test_01_after_sub_ungrouped(self):
        # Configure event
        self.event.event_mail_ids = [
            (5, 0),
            (
                0,
                0,
                {
                    "interval_unit": "now",
                    "interval_type": "after_sub",
                    "group_by_email": False,
                    "template_id": self.template_badge.id,
                },
            ),
        ]
        # Default behaviour is expected, no groupings
        self.registrations.confirm_registration()
        mails = self._get_event_registrations_mails(self.registrations)
        self.assertEqual(len(mails), 3, "3 emails should've been sent")
        # Reg 1
        reg_1_mails = self._get_event_registrations_mails(self.reg_1)
        self.assertEqual(len(reg_1_mails), 1, "Reg 1 should've received 1 email.")
        self.assertEqual(
            len(reg_1_mails.attachment_ids), 1, "One badge should be in the email."
        )
        # Reg 2
        reg_2_mails = self._get_event_registrations_mails(self.reg_2)
        self.assertEqual(len(reg_2_mails), 1, "Reg 2 should've received 1 email.")
        self.assertEqual(
            len(reg_2_mails.attachment_ids), 1, "One badge should be in the email."
        )
        # Reg 3
        reg_3_mails = self._get_event_registrations_mails(self.reg_3)
        self.assertEqual(len(reg_3_mails), 1, "Reg 3 should've received 1 email.")
        self.assertEqual(
            len(reg_3_mails.attachment_ids), 1, "One badge should be in the email."
        )

    def test_03_before_event_grouped(self):
        # Configure event
        self.event.event_mail_ids = [
            (5, 0),
            (
                0,
                0,
                {
                    "interval_nbr": 1,
                    "interval_unit": "days",
                    "interval_type": "before_event",
                    "group_by_email": True,
                    "template_id": self.template_badge.id,
                },
            ),
        ]
        # After registration confirmation, mails should be grouped
        self.registrations.confirm_registration()
        # Execute schedulers manually
        self.event.event_mail_ids.execute()
        # Check
        mails = self._get_event_registrations_mails(self.registrations)
        self.assertEqual(len(mails), 2, "Only 2 emails should've been sent")
        # Reg 1
        reg_1_mails = self._get_event_registrations_mails(self.reg_1)
        self.assertEqual(len(reg_1_mails), 1, "Reg 1 should've received 1 email.")
        self.assertEqual(
            len(reg_1_mails.attachment_ids), 2, "Both badges should be in the email."
        )
        # Reg 2
        reg_2_mails = self._get_event_registrations_mails(self.reg_2)
        self.assertEqual(
            len(reg_2_mails), 0, "Reg 2 shouldn't have received any email."
        )

    def test_04_before_event_ungrouped(self):
        # Configure event
        self.event.event_mail_ids = [
            (5, 0),
            (
                0,
                0,
                {
                    "interval_nbr": 1,
                    "interval_unit": "days",
                    "interval_type": "before_event",
                    "group_by_email": False,
                    "template_id": self.template_badge.id,
                },
            ),
        ]
        # After registration confirmation, mails should be grouped
        self.registrations.confirm_registration()
        # Execute schedulers manually
        self.event.event_mail_ids.execute()
        # Check
        mails = self._get_event_registrations_mails(self.registrations)
        self.assertEqual(len(mails), 3, "3 emails should've been sent")
        # Reg 1
        reg_1_mails = self._get_event_registrations_mails(self.reg_1)
        self.assertEqual(len(reg_1_mails), 1, "Reg 1 should've received 1 email.")
        self.assertEqual(
            len(reg_1_mails.attachment_ids), 1, "Only one badge should be in the email."
        )
        # Reg 2
        reg_2_mails = self._get_event_registrations_mails(self.reg_2)
        self.assertEqual(len(reg_2_mails), 1, "Reg 2 should've received 1 email.")
        self.assertEqual(
            len(reg_2_mails.attachment_ids), 1, "Only one badge should be in the email."
        )

    def test_05_onchange_event_type(self):
        event_type = self.env["event.type"].create(
            {
                "name": "Test Event Type",
                "event_type_mail_ids": [
                    (
                        0,
                        0,
                        {
                            "interval_unit": "now",
                            "interval_type": "after_sub",
                            "group_by_email": True,
                            "template_id": self.template_badge.id,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "interval_nbr": 1,
                            "interval_unit": "days",
                            "interval_type": "before_event",
                            "group_by_email": True,
                            "template_id": self.template_badge.id,
                        },
                    ),
                ],
            }
        )
        self.assertEqual(len(self.event.event_mail_ids), 0)
        self.event.event_type_id = event_type.id
        self.event._onchange_type()
        self.assertEqual(len(self.event.event_mail_ids), 2)
        for mail in self.event.event_mail_ids:
            self.assertTrue(mail.group_by_email)

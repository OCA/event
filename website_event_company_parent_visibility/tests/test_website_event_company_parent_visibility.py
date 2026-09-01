# Copyright 2026 INVITU (<https://www.invitu.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import timedelta

from odoo import Command, fields
from odoo.exceptions import AccessError
from odoo.tests import common, tagged


@tagged("post_install", "-at_install")
class TestWebsiteEventCompanyParentVisibility(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.event_group = cls.env.ref("event.group_event_manager")

        Company = cls.env["res.company"]
        cls.company_hq = Company.create({"name": "HQ"})
        cls.company_sub1 = Company.create(
            {"name": "Sub1", "parent_id": cls.company_hq.id}
        )
        cls.company_sub2 = Company.create(
            {"name": "Sub2", "parent_id": cls.company_hq.id}
        )
        (cls.company_hq + cls.company_sub1 + cls.company_sub2).invalidate_recordset(
            ["parent_path"]
        )

        cls._create_events()
        cls._create_users()

    @classmethod
    def _make_event_vals(cls, name, company=None):
        today = fields.Datetime.now()
        vals = {
            "name": name,
            "date_begin": today + timedelta(days=10),
            "date_end": today + timedelta(days=11),
            "date_tz": "UTC",
        }
        if company is not None:
            vals["company_id"] = company.id if company else False
        return vals

    @classmethod
    def _create_events(cls):
        E = cls.env["event.event"]
        cls.event_hq = E.with_company(cls.company_hq).create(
            cls._make_event_vals("Event HQ", cls.company_hq)
        )
        cls.event_sub1 = E.with_company(cls.company_sub1).create(
            cls._make_event_vals("Event Sub1", cls.company_sub1)
        )
        cls.event_sub2 = E.with_company(cls.company_sub2).create(
            cls._make_event_vals("Event Sub2", cls.company_sub2)
        )
        cls.event_global = E.create(cls._make_event_vals("Event global", company=False))

    @classmethod
    def _make_user(cls, login, company):
        return cls.env["res.users"].create(
            {
                "name": login,
                "login": login,
                "groups_id": [Command.set(cls.event_group.ids)],
                "company_id": company.id,
                "company_ids": [Command.set(company.ids)],
            }
        )

    @classmethod
    def _create_users(cls):
        cls.user_hq = cls._make_user("event_user_hq", cls.company_hq)
        cls.user_sub1 = cls._make_user("event_user_sub1", cls.company_sub1)
        cls.user_sub2 = cls._make_user("event_user_sub2", cls.company_sub2)

    def test_share_default_true(self):
        self.assertTrue(self.company_sub1.share_events_with_parents)
        self.assertTrue(self.company_sub2.share_events_with_parents)

    def test_hq_user_sees_descendants_when_opted_in(self):
        visible = (
            self.env["event.event"]
            .with_user(self.user_hq)
            .search(
                [("id", "in", (self.event_hq + self.event_sub1 + self.event_sub2).ids)]
            )
        )
        self.assertEqual(visible, self.event_hq + self.event_sub1 + self.event_sub2)

    def test_hq_user_does_not_see_opted_out_descendant(self):
        self.company_sub1.share_events_with_parents = False
        visible = (
            self.env["event.event"]
            .with_user(self.user_hq)
            .search(
                [("id", "in", (self.event_hq + self.event_sub1 + self.event_sub2).ids)]
            )
        )
        self.assertEqual(visible, self.event_hq + self.event_sub2)
        with self.assertRaises(AccessError):
            self.event_sub1.with_user(self.user_hq).name = "Bad"

    def test_sub1_user_always_sees_own_events_regardless_of_flag(self):
        self.company_sub1.share_events_with_parents = False
        visible = (
            self.env["event.event"]
            .with_user(self.user_sub1)
            .search([("id", "=", self.event_sub1.id)])
        )
        self.assertEqual(visible, self.event_sub1)

    def test_sub1_user_does_not_see_hq_or_sibling(self):
        visible = (
            self.env["event.event"]
            .with_user(self.user_sub1)
            .search(
                [("id", "in", (self.event_hq + self.event_sub1 + self.event_sub2).ids)]
            )
        )
        self.assertEqual(visible, self.event_sub1)
        with self.assertRaises(AccessError):
            self.event_hq.with_user(self.user_sub1).name = "Bad"
        with self.assertRaises(AccessError):
            self.event_sub2.with_user(self.user_sub1).name = "Bad"

    def test_global_event_visible_to_all(self):
        for user in (self.user_hq, self.user_sub1, self.user_sub2):
            visible = (
                self.env["event.event"]
                .with_user(user)
                .search([("id", "=", self.event_global.id)])
            )
            self.assertEqual(visible, self.event_global)

    def _website_visible_event_ids(self, website):
        clause = [
            "|",
            ("company_id", "=", False),
            "|",
            ("company_id", "=", website.company_id.id),
            "&",
            ("company_id", "child_of", website.company_id.ids),
            ("company_id.share_events_with_parents", "=", True),
        ]
        ids = self.env["event.event"].search(clause).ids
        relevant = self.event_hq + self.event_sub1 + self.event_sub2 + self.event_global
        return [eid for eid in ids if eid in relevant.ids]

    def test_website_hq_shows_descendants_when_opted_in(self):
        site_hq = self.env["website"].create(
            {"name": "Site HQ", "company_id": self.company_hq.id}
        )
        self.assertEqual(
            set(self._website_visible_event_ids(site_hq)),
            {
                self.event_hq.id,
                self.event_sub1.id,
                self.event_sub2.id,
                self.event_global.id,
            },
        )

    def test_website_hq_hides_opted_out_descendant(self):
        self.company_sub1.share_events_with_parents = False
        site_hq = self.env["website"].create(
            {"name": "Site HQ", "company_id": self.company_hq.id}
        )
        self.assertEqual(
            set(self._website_visible_event_ids(site_hq)),
            {self.event_hq.id, self.event_sub2.id, self.event_global.id},
        )

    def test_website_sub1_keeps_seeing_own_events_when_opted_out(self):
        self.company_sub1.share_events_with_parents = False
        site_sub1 = self.env["website"].create(
            {"name": "Site Sub1", "company_id": self.company_sub1.id}
        )
        visible = set(self._website_visible_event_ids(site_sub1))
        self.assertIn(self.event_sub1.id, visible)
        self.assertIn(self.event_global.id, visible)
        self.assertNotIn(self.event_hq.id, visible)
        self.assertNotIn(self.event_sub2.id, visible)

    def test_website_sub1_does_not_show_sibling(self):
        site_sub1 = self.env["website"].create(
            {"name": "Site Sub1", "company_id": self.company_sub1.id}
        )
        self.assertNotIn(
            self.event_sub2.id, set(self._website_visible_event_ids(site_sub1))
        )

    def test_search_get_detail_injects_clause(self):
        site_hq = self.env["website"].create(
            {"name": "Site HQ detail", "company_id": self.company_hq.id}
        )
        detail = self.env["event.event"]._search_get_detail(
            website=site_hq,
            order="date_begin",
            options={"displayDescription": False, "displayDetail": False},
        )
        expected_clause = [
            "|",
            ("company_id", "=", False),
            "|",
            ("company_id", "=", self.company_hq.id),
            "&",
            ("company_id", "child_of", self.company_hq.ids),
            ("company_id.share_events_with_parents", "=", True),
        ]
        self.assertTrue(any(expected_clause == sub for sub in detail["base_domain"]))

    def test_res_config_settings_related_field(self):
        Settings = self.env["res.config.settings"]
        Settings.with_company(self.company_hq).create(
            {"share_events_with_parents": False}
        ).execute()
        self.assertFalse(self.company_hq.share_events_with_parents)
        Settings.with_company(self.company_hq).create(
            {"share_events_with_parents": True}
        ).execute()
        self.assertTrue(self.company_hq.share_events_with_parents)

    def test_registration_rule_follows_hierarchy_and_opt_in(self):
        reg = self.env["event.registration"].create(
            {
                "event_id": self.event_sub1.id,
                "name": "Test attendee",
                "company_id": self.company_sub1.id,
            }
        )
        visible = (
            self.env["event.registration"]
            .with_user(self.user_hq)
            .search([("id", "=", reg.id)])
        )
        self.assertEqual(visible, reg)
        self.company_sub1.share_events_with_parents = False
        visible = (
            self.env["event.registration"]
            .with_user(self.user_hq)
            .search([("id", "=", reg.id)])
        )
        self.assertFalse(visible)
        self.company_sub1.share_events_with_parents = True
        visible = (
            self.env["event.registration"]
            .with_user(self.user_sub2)
            .search([("id", "=", reg.id)])
        )
        self.assertFalse(visible)

    def test_rule_domain_contains_share_check(self):
        for xml_id in (
            "event.event_event_company_rule",
            "event.event_registration_company_rule",
            "event.ir_rule_event_event_ticket_company",
        ):
            rule = self.env.ref(xml_id)
            self.assertIn("share_events_with_parents", rule.domain_force or "")
            self.assertIn("child_of", rule.domain_force or "")

import datetime
from unittest.mock import patch

from odoo.tests import common, tagged

from odoo.addons.event.models.event_event import EventEvent

from ..models.event_event import Event


@tagged("post_install", "-at_install", "website_event_copy")
class WebsiteEventCopyTestCase(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.event_a_name = "test_website_evt_copy_a"
        cls.event_b_name = "test_website_evt_copy_b"

        cls.event_a = cls.env["event.event"].create(
            {
                "name": cls.event_a_name,
                "website_menu": True,
                "date_begin": datetime.datetime(2023, 1, 1),
                "date_end": datetime.datetime(2024, 1, 1),
            }
        )
        cls.event_b = cls.env["event.event"].create(
            {
                "name": cls.event_b_name,
                "website_menu": False,
                "date_begin": datetime.datetime(2023, 1, 1),
                "date_end": datetime.datetime(2024, 1, 1),
            }
        )

        cls.website_views = cls.env["ir.ui.view"].search(
            [("name", "like", cls.event_a_name)]
        )

        v = cls.env["ir.ui.view"].search(
            [
                ("name", "like", cls.event_a_name),
                ("key", "like", "introduction"),
            ]
        )
        cls.event_a_struct_view = cls.env["ir.ui.view"].create(
            {
                "name": f"generated_structure_view_{cls.event_a_name}",
                "key": f"{v.key}_oe_test_things",
                "inherit_id": v.id,
                "arch_db": "<data>"
                "<xpath expr=\"//*[hasclass('oe_structure')][@id='oe_structure_"
                'website_event_intro_2\']" position="inside">'
                "<p class='lead o_default_snippet_text'>This is a simple test view"
                "</p>"
                "</xpath>"
                "</data>",
            }
        )

        cls.event_website_view_strings = [
            "Introduction test_website_evt_copy_a",
            "Location test_website_evt_copy_a",
        ]

        cls.event_website_view_keys = [
            {
                "menu_key": f"introduction-test-website-evt-copy-a-{cls.event_a.id}",
                "view_key": f"test-website-evt-copy-a-{cls.event_a.id}",
            },
            {
                "menu_key": f"location-test-website-evt-copy-a-{cls.event_a.id}",
                "view_key": f"test-website-evt-copy-a-{cls.event_a.id}",
            },
        ]

    def test_views_created(self):
        for i, website_view in enumerate(self.website_views):
            self.assertEqual(
                website_view.display_name, self.event_website_view_strings[i]
            )

    def test_get_website_menu_key(self):
        for i, website_view in enumerate(self.website_views):
            self.assertEqual(
                website_view.get_website_event_menu_key(),
                self.event_website_view_keys[i]["menu_key"],
            )

    def test_get_website_view_key(self):
        for i, website_view in enumerate(self.website_views):
            self.assertEqual(
                website_view.get_website_event_view_key(),
                self.event_website_view_keys[i]["view_key"],
            )

    def test_website_event_duplication_with_website(self):
        copied_event_a = self.event_a.duplicate_event_and_website(
            {"new_name": self.event_a.name}
        )

        self.assertEqual(copied_event_a.name, self.event_a.name)
        self.assertEqual(copied_event_a.website_menu, self.event_a.website_menu)
        self.assertEqual(copied_event_a.date_begin, self.event_a.date_begin)
        self.assertEqual(copied_event_a.date_end, self.event_a.date_end)

        copied_views = self.env["ir.ui.view"].search(
            [("key", "like", copied_event_a.name), ("key", "like", copied_event_a.id)]
        )

        self.assertEqual(len(copied_views), 4)

    def test_website_event_duplication_with_website_b(self):
        with patch.object(EventEvent, "copy") as mocked_copy:
            self.event_b.duplicate_event_and_website({"new_name": self.event_b.name})
            mocked_copy.assert_called_with()

    def test_action_dup_event_and_web(self):
        with patch.object(Event, "action_dup_event_and_web") as mocked_action:
            mocked_action.return_value = {
                "view_type": "form",
                "view_mode": "form",
                "res_model": "event.event",
                "type": "ir.actions.act_window",
                "res_id": 8080,
            }
            dict_result = self.event_a.action_dup_event_and_web()
            self.assertEqual(
                dict_result,
                {
                    "view_type": "form",
                    "view_mode": "form",
                    "res_model": "event.event",
                    "type": "ir.actions.act_window",
                    "res_id": 8080,
                },
            )

    def test_delete_event_with_views(self):
        # It test event_event._flush_website_event_menus_and_views() because unlinking
        # triggers the on_delete decorator
        self.event_a.unlink()
        website_views = self.env["ir.ui.view"].search(
            [("name", "like", self.event_a_name)]
        )
        self.assertFalse(website_views)

    def test_replace_key_id(self):
        good_key = "AnyModel.AnyMenu-AnyEvent-50_AnyDetails"

        key = "AnyModel.AnyMenu-AnyEvent-49_AnyDetails"
        new_key = self.event_a.replace_key_id(key, 50)
        self.assertEqual(new_key, good_key)

        # This use case can happen when an event has been copied before the installation
        # of website_event_copy module. This is due to the way odoo creates event copy
        key2 = "AnyModel.AnyMenu-AnyEvent-1-49_AnyDetails"
        new_key2 = self.event_a.replace_key_id(key2, 50)
        self.assertEqual(new_key2, good_key)

# Copyright 2026 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.tests import TransactionCase


class TestEventEventRibbon(TransactionCase):
    def setUp(self):
        super().setUp()
        self.ribbon = self.env["event.event.ribbon"].create(
            {
                "name": "Test Ribbon",
            }
        )

    def test_get_style(self):
        """We test that the _get_style method returns the correct inline CSS style."""

        # By default, the ribbon should have a black background and white text
        expected_style = "background-color: #000000; color: #FFFFFF;"
        self.assertEqual(self.ribbon._get_style(), expected_style)

    def test_get_css_classes(self):
        """We test that the _get_css_classes method returns the correct CSS classes
        based on position."""

        # By default, the ribbon should be positioned on the left
        expected_classes = "o_ribbon o_not_editable z-index-1  o_ribbon_left"
        self.assertEqual(self.ribbon._get_css_classes(), expected_classes)

        # Change position to right and test again
        self.ribbon.position = "right"
        expected_classes = "o_ribbon o_not_editable z-index-1  o_ribbon_right"
        self.assertEqual(self.ribbon._get_css_classes(), expected_classes)

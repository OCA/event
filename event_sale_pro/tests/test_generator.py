# -*- coding: utf-8 -*-
# © 2015 Grupo ESOC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from .base import BaseCase


class QuotationGeneratorCase(BaseCase):
    """Test quotation generator behavior."""
    def setUp(self):
        super(QuotationGeneratorCase, self).setUp()

        # Create quotation generator wizard
        self.generator = super(QuotationGeneratorCase, self).create_generator()

        # Attach registrations to the wizard
        self.generator.registration_ids |= self.create_registrations()

        # Create unrelated partners
        self.partner_unrelated_0 = self.env["res.partner"].create({
            "name": u"Ünrelated company partner 0",
            "is_company": True,
        })
        self.partner_unrelated_1 = self.env["res.partner"].create({
            "name": u"Ünrelated person partner 1",
            "is_company": False,
            "parent_id": self.partner_unrelated_0.id,
        })
        self.partner_unrelated_2 = self.env["res.partner"].create({
            "name": u"Ünrelated person partner 2",
            "is_company": False,
            "parent_id": self.partner_unrelated_0.id,
        })

    def tearDown(self):
        regs = self.generator.registration_ids

        # Tests for each registration
        for reg in regs:
            self.assertIsNot(reg.origin, False)
            self.assertIsNot(reg.origin_id, False)
            self.assertIsNot(reg.origin_id.order_id, False)
            self.assertEqual(reg.origin, reg.origin_id.name)

            # Test invoiced partner
            client = reg.invoiced_partner_id or reg.partner_id
            parent = (client.commercial_partner_id
                      if self.generator.group_by_commercial_entity
                      else client)

            self.assertEqual(reg.invoiced_partner(), client)
            self.assertEqual(reg.origin_id.order_id.partner_id, parent)

        # Tests comparing both registrations
        if self.generator.group_by_commercial_entity:
            self.assertEqual(regs[0].origin_id.order_id,
                             regs[1].origin_id.order_id)
        else:
            self.assertNotEqual(regs[0].origin_id.order_id,
                                regs[1].origin_id.order_id)

        self.assertEqual(len(regs.mapped("origin_id")), 2)
        self.assertNotEqual(regs[0].origin_id, regs[1].origin_id)

        return super(QuotationGeneratorCase, self).tearDown()

    def unrelated_company(self):
        """Make the registrations be invoiced to an unrelated company."""
        self.generator.registration_ids[0].invoiced_partner_id = (
            self.partner_unrelated_0)
        self.generator.registration_ids[1].invoiced_partner_id = (
            self.partner_unrelated_0)

    def unrelated_persons(self):
        """Make the registrations be invoiced to unrelated persons.

        Both persons belong to the same company.
        """
        self.generator.registration_ids[0].invoiced_partner_id = (
            self.partner_unrelated_1)
        self.generator.registration_ids[1].invoiced_partner_id = (
            self.partner_unrelated_2)

    def test_generate_grouped_same_partner(self):
        """Quotations grouped by commercial entity.

        This is the default behavior of the quotation generator.
        """
        self.generator.action_generate()

    def test_generate_individual_same_partner(self):
        """Quotations individually."""
        self.generator.group_by_commercial_entity = False
        self.generator.action_generate()

    def test_generate_grouped_different_company(self):
        """Quotations grouped by commercial entity for a different company."""
        self.unrelated_company()
        self.generator.action_generate()

    def test_generate_individual_different_company(self):
        """Quotations individually for a different company."""
        self.group_by_commercial_entity = False
        self.unrelated_company()
        self.generator.action_generate()

    def test_generate_grouped_different_persons(self):
        """Quotations grouped by commercial entity for a different persons."""
        self.unrelated_persons()
        self.generator.action_generate()

    def test_generate_individual_different_persons(self):
        """Quotations individually for a different persons."""
        self.generator.group_by_commercial_entity = False
        self.unrelated_persons()
        self.generator.action_generate()

    def test_no_registrations_duplicated(self):
        """No registrations must be duplicated when confirming quotation."""
        regs = len(self.generator.event_id.registration_ids)
        orders = self.generator.action_generate()
        for order in orders:
            order.action_button_confirm()
            self.assertEqual(order.state, "manual")
        self.assertEqual(len(self.generator.event_id.registration_ids), regs)

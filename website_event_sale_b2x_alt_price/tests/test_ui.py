# Copyright 2022 Tecnativa - Carlos Roca
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
from datetime import datetime, timedelta

from odoo.tests.common import Form, HttpCase


class UICase(HttpCase):
    def setUp(self):
        super().setUp()
        website = self.env["website"].get_current_website()
        pricelist = self.env["product.pricelist"].create(
            {
                "name": "website_sale_event_b2x_alt_price public",
                "currency_id": website.user_id.company_id.currency_id.id,
                "selectable": True,
            }
        )
        website.user_id.property_product_pricelist = pricelist
        admin = self.env.ref("base.user_admin")
        admin.property_product_pricelist = pricelist
        self.tax_group_22 = self.env["account.tax.group"].create(
            {"name": "Tax group 22%"}
        )
        tax_22_form = Form(self.env["account.tax"])
        tax_22_form.amount_type = "percent"
        tax_22_form.amount = 22
        tax_22_form.description = "22%"
        tax_22_form.name = "Tax sale 22%"
        tax_22_form.tax_group_id = self.tax_group_22
        tax_22_form.type_tax_use = "sale"
        self.tax_22_sale = tax_22_form.save()
        product_form = Form(self.env["product.product"])
        product_form.name = "Test Product Event Without Taxes"
        product_form.lst_price = 100
        product_form.event_ok = True
        product_form.type = "service"
        self.product_without_taxes = product_form.save()
        self.product_without_taxes.taxes_id = False
        product_form = Form(self.env["product.product"])
        product_form.name = "Test Product Event With Taxes"
        product_form.lst_price = 100
        product_form.event_ok = True
        product_form.type = "service"
        self.product_with_taxes = product_form.save()
        self.product_with_taxes.taxes_id = self.tax_22_sale
        event_form = Form(self.env["event.event"])
        event_form.name = "Test Event One Ticket"
        event_form.date_begin = datetime.today()
        event_form.date_end = datetime.today() + timedelta(days=1)
        event_form.seats_availability = "unlimited"
        with event_form.event_ticket_ids.new() as ticket:
            ticket.name = "Test Ticket"
            ticket.product_id = self.product_with_taxes
            ticket.price = 100
        self.event_one_ticket = event_form.save()
        self.event_one_ticket.is_published = True
        self.event_one_ticket.website_sequence = 1
        event_form = Form(self.env["event.event"])
        event_form.name = "Test Event More Tickets"
        event_form.date_begin = datetime.today()
        event_form.date_end = datetime.today() + timedelta(days=1)
        event_form.seats_availability = "unlimited"
        with event_form.event_ticket_ids.new() as ticket:
            ticket.name = "Test Ticket 1"
            ticket.product_id = self.product_with_taxes
            ticket.price = 100
        with event_form.event_ticket_ids.new() as ticket:
            ticket.name = "Test Ticket 2"
            ticket.product_id = self.product_without_taxes
            ticket.price = 100
        self.event_more_tickets = event_form.save()
        self.event_more_tickets.is_published = True
        self.event_more_tickets.website_sequence = 2

    def _switch_tax_mode(self, mode):
        assert mode in {"tax_excluded", "tax_included"}
        config = Form(self.env["res.config.settings"])
        config.show_line_subtotals_tax_selection = mode
        config.group_product_pricelist = True
        config.product_pricelist_setting = "advanced"
        config.group_discount_per_so_line = True
        config = config.save()
        config.execute()

    def test_ui_website_b2b(self):
        """Test frontend b2b tour."""
        UICase._switch_tax_mode(self, "tax_excluded")
        self.start_tour(
            "/event", "website_event_sale_b2x_alt_price_b2b", login="admin",
        )

    def test_ui_website_b2c(self):
        """Test frontend b2c tour."""
        self._switch_tax_mode("tax_included")
        self.start_tour(
            "/event", "website_event_sale_b2x_alt_price_b2c", login="admin",
        )

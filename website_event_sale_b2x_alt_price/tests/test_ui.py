# Copyright 2022 Tecnativa - Carlos Roca
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
from datetime import datetime, timedelta

from odoo.orm.commands import Command
from odoo.tests import Form, HttpCase, tagged


@tagged("post_install", "-at_install")
class UICase(HttpCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.website = cls.env["website"].get_current_website()
        cls.admin = cls.env.ref("base.user_admin")
        cls.admin.write(
            {
                "street": "215 Vine St",
                "city": "Scranton",
                "zip": "18503",
                "country_id": cls.env.ref("base.us").id,
                "state_id": cls.env.ref("base.state_us_39").id,
                "phone": "+1 570-555-1234",
                "email": "admin@yourcompany.example.com",
            }
        )
        cls.tax_group_22 = cls.env["account.tax.group"].create(
            {"name": "Tax group 22%"}
        )
        cls.tax_22_sale = cls.env["account.tax"].create(
            {
                "amount_type": "percent",
                "amount": 22,
                "description": "22%",
                "name": "Tax sale 22%",
                "tax_group_id": cls.tax_group_22.id,
                "type_tax_use": "sale",
            }
        )
        cls.product_without_taxes = cls.env["product.product"].create(
            {
                "name": "Test Product Event Without Taxes",
                "list_price": 100,
                "type": "service",
                "taxes_id": False,
            }
        )
        cls.product_with_taxes = cls.env["product.product"].create(
            {
                "name": "Test Product Event With Taxes",
                "list_price": 100,
                "type": "service",
                "taxes_id": [Command.set(cls.tax_22_sale.ids)],
            }
        )
        cls.pricelist = cls.env["product.pricelist"].create(
            {
                "name": "website_sale_event_b2x_alt_price public",
                "currency_id": cls.website.company_id.currency_id.id,
                "selectable": True,
            }
        )
        cls.pricelist_with_discount = cls.env["product.pricelist"].create(
            {
                "name": "website_sale_event_b2x_alt_price with discount",
                "currency_id": cls.website.company_id.currency_id.id,
                "selectable": True,
                "item_ids": [
                    Command.create(
                        {
                            "applied_on": "1_product",
                            "compute_price": "percentage",
                            "percent_price": 10.0,
                            "product_tmpl_id": (
                                cls.product_with_taxes.product_tmpl_id.id
                            ),
                        },
                    )
                ],
            }
        )

    def _create_events(self):
        event_form = Form(self.env["event.event"])
        event_form.name = "Test Event One Ticket"
        event_form.date_begin = datetime.today()
        event_form.date_end = datetime.today() + timedelta(days=1)
        event_form.seats_limited = False
        with event_form.event_ticket_ids.new() as ticket:
            ticket.name = "Test Ticket"
            ticket.product_id = self.product_with_taxes
            ticket.price = 100
        event_one_ticket = event_form.save()
        event_one_ticket.is_published = True
        event_form = Form(self.env["event.event"])
        event_form.name = "Test Event More Tickets"
        event_form.date_begin = datetime.today()
        event_form.date_end = datetime.today() + timedelta(days=1)
        event_form.seats_limited = False
        with event_form.event_ticket_ids.new() as ticket:
            ticket.name = "Test Ticket 1"
            ticket.product_id = self.product_with_taxes
            ticket.price = 100
        with event_form.event_ticket_ids.new() as ticket:
            ticket.name = "Test Ticket 2"
            ticket.product_id = self.product_without_taxes
            ticket.price = 100
        event_more_tickets = event_form.save()
        event_more_tickets.is_published = True

    def _switch_tax_mode(self, mode):
        assert mode in {"tax_excluded", "tax_included"}
        config = self.env["res.config.settings"].create(
            {
                "show_line_subtotals_tax_selection": mode,
                "group_product_pricelist": True,
                "group_discount_per_so_line": True,
            }
        )
        config.execute()

    def _set_pricelist(self, pricelist):
        self.website.user_id.property_product_pricelist = pricelist
        self.admin.property_product_pricelist = pricelist

    def test_ui_website_b2b(self):
        """Test frontend b2b tour."""
        self._set_pricelist(self.pricelist)
        self._create_events()
        self._switch_tax_mode("tax_excluded")
        self.start_tour(
            "/event",
            "website_event_sale_b2x_alt_price_b2b",
            login="admin",
        )

    def test_ui_website_b2c(self):
        """Test frontend b2c tour."""
        self._set_pricelist(self.pricelist)
        self._create_events()
        self._switch_tax_mode("tax_included")
        self.start_tour(
            "/event",
            "website_event_sale_b2x_alt_price_b2c",
            login="admin",
        )

    def test_ui_website_b2b_with_discount(self):
        """Test frontend b2b with discount tour."""
        self._set_pricelist(self.pricelist_with_discount)
        self._create_events()
        self._switch_tax_mode("tax_excluded")
        self.start_tour(
            "/event",
            "website_event_sale_b2x_alt_price_b2b_with_discount",
            login="admin",
        )

    def test_ui_website_b2c_with_discount(self):
        """Test frontend b2c with discount tour."""
        self._set_pricelist(self.pricelist_with_discount)
        self._create_events()
        self._switch_tax_mode("tax_included")
        self.start_tour(
            "/event",
            "website_event_sale_b2x_alt_price_b2c_with_discount",
            login="admin",
        )

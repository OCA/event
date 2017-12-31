# -*- coding: utf-8 -*-
# Copyright 2017,2018 IT-Projects LLC - Ivan Yelizariev
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
from odoo import api
from odoo.tests.common import HttpCase


class TestUI(HttpCase):
    def setUp(self):
        super(TestUI, self).setUp()
        self.phantom_env = api.Environment(self.registry.test_cr, self.uid, {})
        # remove tickets to have only unconfirmed paid tickets in tree view
        self.phantom_env['event.registration'].search([]).unlink()
        event = self.phantom_env.ref('event.event_0')
        ticket_type = self.phantom_env.ref('event_sale.event_0_ticket_2')
        for i in range(2):
            self.phantom_env['event.registration']\
                .with_context(registration_force_draft=True)\
                .create({
                    'event_id': event.id,
                    'event_ticket_id': ticket_type.id,
                })

    def test_can_confirm(self):
        self.phantom_js(
            '/web',

            "odoo.__DEBUG__.services['web_tour.tour']"
            ".run('event_sale_confirmation.can_confirm')",

            "odoo.__DEBUG__.services['web_tour.tour']"
            ".tours['event_sale_confirmation.can_confirm'].ready",

            login='admin'
        )

    def test_cannot_confirm(self):
        self.phantom_js(
            '/web',

            "odoo.__DEBUG__.services['web_tour.tour']"
            ".run('event_sale_confirmation.cannot_confirm')",

            "odoo.__DEBUG__.services['web_tour.tour']"
            ".tours['event_sale_confirmation.cannot_confirm'].ready",

            login='demo'
        )

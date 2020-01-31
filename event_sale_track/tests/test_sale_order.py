# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo.tests.common import SavepointCase


class TestSaleOrder(SavepointCase):
    """Test the registration features after ticket move.

    These tests are here to ensure, that the default Event functionality
    is still working after the move of the ticket to the tracks.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.event = cls.env['event.event'].create({
            'name': 'Testevent',
            'date_begin': '2018-03-01 10:00:00',
            'date_end': '2018-03-01 11:00:00',
        })
        cls.track = cls.env['event.track'].create({
            'event_id': cls.event.id,
            'name': 'Testtrack'
        })
        cls.normal_ticket = cls.env['event.event.ticket'].create({
            'name': 'Normal Ticket',
            'track_id': cls.track.id
        })
        cls.premium_ticket = cls.env['event.event.ticket'].create({
            'name': 'Premium Ticket',
            'track_id': cls.track.id,
            'seats_max': 1
        })
        cls.partner = cls.env['res.partner'].with_context(
            track_disable=True).create({
                'name': 'Testpartner'
            })
        cls.another_partner = cls.env['res.partner'].with_context(
            track_disable=True).create({
                'name': 'Another Partner'
            })
        cls.sale_order = cls.env['sale.order'].create({
            'partner_id': cls.partner.id,
            'name': 'Testorder'
        })
        cls.prod = cls.env.ref('event_sale.product_product_event')

    def test_sale_order_create(self):
        self.env['sale.order.line'].create({
            'event_ticket_id': self.normal_ticket.id,
            'event_id': self.event.id,
            'order_id': self.sale_order.id,
            'name': 'testline',
            'product_id': self.prod.id
        })
        self.sale_order.action_confirm()
        reg = self.env['event.registration'].search(
            [('event_ticket_id', '=', self.normal_ticket.id)]
        )
        self.assertEqual(len(reg), 1)
        self.assertEqual(reg.origin, 'Testorder')

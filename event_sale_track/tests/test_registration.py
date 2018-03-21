# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo.tests.common import SavepointCase
from odoo.exceptions import ValidationError


class TestRegistration(SavepointCase):
    """Test the registration features after ticket move."""

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
        cls.partner = cls.env['res.partner'].create({
            'name': 'Testpartner'
        })
        cls.another_partner = cls.env['res.partner'].create({
            'name': 'Another Partner'
        })

    def test_registration(self):
        reg = self.env['event.registration'].create({
            'partner_id': self.partner.id,
            'event_ticket_id': self.normal_ticket.id,
            'event_id': self.event.id
        })
        self.assertEqual(self.normal_ticket.registration_ids, reg)
        self.assertEqual(self.normal_ticket.seats_unconfirmed, 1)
        reg.confirm_registration()
        self.assertEqual(self.normal_ticket.seats_reserved, 1)
        self.event.button_confirm()
        reg.button_reg_close()
        self.assertEqual(self.normal_ticket.seats_used, 1)

    def test_limit_reached(self):
        reg = self.env['event.registration'].create({
            'partner_id': self.partner.id,
            'event_ticket_id': self.premium_ticket.id,
            'event_id': self.event.id
        })
        reg.confirm_registration()
        reg2 = self.env['event.registration'].create({
            'partner_id': self.another_partner.id,
            'event_ticket_id': self.premium_ticket.id,
            'event_id': self.event.id
        })
        with self.assertRaises(ValidationError):
            reg2.confirm_registration()

    def test_limit_reduced(self):
        self.premium_ticket.seats_max = 2
        reg = self.env['event.registration'].create({
            'partner_id': self.partner.id,
            'event_ticket_id': self.premium_ticket.id,
            'event_id': self.event.id
        })
        reg.confirm_registration()
        reg2 = self.env['event.registration'].create({
            'partner_id': self.another_partner.id,
            'event_ticket_id': self.premium_ticket.id,
            'event_id': self.event.id
        })
        reg2.confirm_registration()
        with self.assertRaises(ValidationError):
            self.premium_ticket.seats_max = 1

    def test_autoconfirm(self):
        self.event.auto_confirm = True
        self.event.button_confirm()
        reg = self.env['event.registration'].create({
            'partner_id': self.partner.id,
            'event_ticket_id': self.normal_ticket.id,
            'event_id': self.event.id
        })
        self.assertEqual(reg.state, 'open')

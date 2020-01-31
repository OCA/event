# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo.tests.common import SavepointCase


class TestTicketBase(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.event = cls.env['event.event'].create({
            'name': 'Testevent',
            'date_begin': '2018-03-01 10:00:00',
            'date_end': '2018-03-01 11:00:00',
            'state': 'confirm',
        })
        cls.track1 = cls.env['event.track'].create({
            'event_id': cls.event.id,
            'name': 'Testtrack'
        })
        cls.ticket1 = cls.env['event.event.ticket'].create({
            'name': 'Normal Ticket',
            'track_id': cls.track1.id,
            'seats_max': 3,
        })
        cls.track2 = cls.env['event.track'].create({
            'event_id': cls.event.id,
            'name': 'Testtrack'
        })
        cls.ticket2 = cls.env['event.event.ticket'].create({
            'name': 'Normal Ticket',
            'track_id': cls.track2.id,
            'seats_max': 2,
        })
        cls.partner = cls.env.ref('base.partner_demo')

    def _create_attendee(self, **kw):
        vals = {
            'partner_id': self.partner.id,
            'event_ticket_id': self.ticket1.id,
            'event_id': self.event.id,
        }
        vals.update(kw)
        return self.env['event.registration'].create(vals)


class TestTicket(TestTicketBase):

    def test_create_and_related(self):
        self.assertEqual(self.track1.ticket_ids, self.ticket1)
        self.assertEqual(self.track2.ticket_ids, self.ticket2)
        self.assertEqual(self.event.event_ticket_ids, (
            self.track1.ticket_ids + self.track2.ticket_ids)
        )

    def test_attendee_relation(self):
        att1 = self._create_attendee()
        self.assertIn(self.ticket1, att1.ticket_ids)
        self.assertIn(att1, self.ticket1.registration_ids)
        att2 = self._create_attendee(
            event_ticket_id=self.ticket2.id,
            partner_id=self.env.ref('base.res_partner_1').id
        )
        self.assertIn(self.ticket2, att2.ticket_ids)
        self.assertIn(att2, self.ticket2.registration_ids)
        # check they are not mixed up
        self.assertNotIn(self.ticket2, att1.ticket_ids)
        self.assertNotIn(att1, self.ticket2.registration_ids)
        self.assertNotIn(self.ticket1, att2.ticket_ids)
        self.assertNotIn(att2, self.ticket1.registration_ids)
        # check computed tracks
        self.assertEqual(att1.track_ids, self.track1)
        self.assertEqual(att2.track_ids, self.track2)

    def test_ticket_seats(self):
        att1 = self._create_attendee()
        # registation not confirmed
        self.assertEqual(self.ticket1.seats_available, 3)
        self.assertEqual(self.ticket1.seats_reserved, 0)
        self.assertEqual(self.ticket1.seats_used, 0)
        # create another participant
        att2 = self._create_attendee(
            partner_id=self.env.ref('base.res_partner_1').id
        )
        # same status
        self.assertEqual(self.ticket1.seats_available, 3)
        self.assertEqual(self.ticket1.seats_reserved, 0)
        self.assertEqual(self.ticket1.seats_used, 0)
        # confirm guys
        att1.confirm_registration()
        self.assertEqual(self.ticket1.seats_available, 2)
        self.assertEqual(self.ticket1.seats_reserved, 1)
        self.assertEqual(self.ticket1.seats_used, 0)
        att2.confirm_registration()
        self.assertEqual(self.ticket1.seats_available, 1)
        self.assertEqual(self.ticket1.seats_reserved, 2)
        self.assertEqual(self.ticket1.seats_used, 0)
        # make them attend
        att1.button_reg_close()
        att2.button_reg_close()
        self.assertEqual(self.ticket1.seats_available, 1)
        self.assertEqual(self.ticket1.seats_reserved, 0)
        self.assertEqual(self.ticket1.seats_used, 2)

    def test_ticket_seats_isolated_by_ticket(self):
        # create attendees for both tickets
        att1_t1 = self._create_attendee()
        att2_t1 = self._create_attendee(
            partner_id=self.env.ref('base.res_partner_1').id
        )
        # create some attendees for another ticket
        att1_t2 = self._create_attendee(
            event_ticket_id=self.ticket2.id,
            partner_id=self.env.ref('base.res_partner_2').id
        )
        # we can even pass multiple tickets instead of a single one
        # we'll ignore this ticket in counters
        # as we just want to test that they are not affected by a 3rd ticket
        track3 = self.env['event.track'].create({
            'event_id': self.event.id,
            'name': 'Testtrack 3'
        })
        ticket3 = self.env['event.event.ticket'].create({
            'name': 'Normal Ticket',
            'track_id': track3.id,
            'seats_max': 10,
        })
        att2_t2 = self._create_attendee(
            event_ticket_id=None,
            ticket_ids=[(6, 0, [self.ticket2.id, ticket3.id])],
            partner_id=self.env.ref('base.res_partner_3').id
        )
        # check initial state
        self.assertEqual(self.ticket1.seats_max, 3)
        self.assertEqual(self.ticket1.seats_available, 3)
        self.assertEqual(self.ticket1.seats_reserved, 0)
        self.assertEqual(self.ticket1.seats_used, 0)
        self.assertEqual(self.ticket2.seats_max, 2)
        self.assertEqual(self.ticket2.seats_available, 2)
        self.assertEqual(self.ticket2.seats_reserved, 0)
        self.assertEqual(self.ticket2.seats_used, 0)
        # confirm one
        att1_t1.confirm_registration()
        self.assertEqual(self.ticket1.seats_available, 2)
        self.assertEqual(self.ticket1.seats_reserved, 1)
        self.assertEqual(self.ticket1.seats_used, 0)
        # mark one as done, confirm another on the same ticket1
        att1_t1.button_reg_close()
        att2_t1.confirm_registration()
        self.assertEqual(self.ticket1.seats_available, 1)
        self.assertEqual(self.ticket1.seats_reserved, 1)
        self.assertEqual(self.ticket1.seats_used, 1)
        # confirm both on ticket2
        att1_t2.confirm_registration()
        att2_t2.confirm_registration()
        self.assertEqual(self.ticket2.seats_available, 0)
        self.assertEqual(self.ticket2.seats_reserved, 2)
        self.assertEqual(self.ticket2.seats_used, 0)
        # delete one
        att1_t2.unlink()
        att2_t2.button_reg_close()
        # confirm the other
        self.assertEqual(self.ticket2.seats_available, 1)
        self.assertEqual(self.ticket2.seats_reserved, 0)
        self.assertEqual(self.ticket2.seats_used, 1)

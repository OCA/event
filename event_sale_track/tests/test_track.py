# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from .test_ticket import TestTicketBase


class TestTrack(TestTicketBase):

    def test_track_seats(self):
        # create another ticket for track2
        ticket3 = self.env['event.event.ticket'].create({
            'name': 'Special offer ticket',
            'track_id': self.track2.id,
            'seats_max': 4,
        })
        # create some attendees for ticket1
        att1_t1 = self._create_attendee()
        att2_t1 = self._create_attendee(
            partner_id=self.env.ref('base.res_partner_1').id
        )
        # create some attendees for ticket2
        att1_t2 = self._create_attendee(
            event_ticket_id=self.ticket2.id,
            partner_id=self.env.ref('base.res_partner_2').id
        )
        att2_t2 = self._create_attendee(
            event_ticket_id=self.ticket2.id,
            partner_id=self.env.ref('base.res_partner_3').id
        )
        # create some attendees for ticket3
        att1_t3 = self._create_attendee(
            event_ticket_id=ticket3.id,
            partner_id=self.env.ref('base.res_partner_4').id
        )
        att2_t3 = self._create_attendee(
            event_ticket_id=ticket3.id,
            partner_id=self.env.ref('base.res_partner_10').id
        )
        # check initial state
        self.assertEqual(self.track1.seats_max, 3)
        self.assertEqual(self.track1.seats_available, 3)
        self.assertEqual(self.track1.seats_reserved, 0)
        self.assertEqual(self.track1.seats_used, 0)

        # for track to we'll have 2 (from ticket2) + 4 (from ticket3)
        self.assertEqual(self.track2.seats_max, 6)
        self.assertEqual(self.track2.seats_available, 6)
        self.assertEqual(self.track2.seats_reserved, 0)
        self.assertEqual(self.track2.seats_used, 0)

        # confirm on ticket1
        att1_t1.confirm_registration()
        att2_t1.confirm_registration()
        self.assertEqual(self.track1.seats_available, 1)
        self.assertEqual(self.track1.seats_reserved, 2)
        self.assertEqual(self.track1.seats_used, 0)

        # confirm on ticket2
        att1_t2.confirm_registration()
        att2_t2.confirm_registration()
        self.assertEqual(self.track2.seats_available, 4)
        self.assertEqual(self.track2.seats_reserved, 2)
        self.assertEqual(self.track2.seats_used, 0)

        # confirm on ticket3
        att1_t3.confirm_registration()
        att2_t3.confirm_registration()
        att2_t3.button_reg_close()
        self.assertEqual(self.track2.seats_available, 2)
        self.assertEqual(self.track2.seats_reserved, 3)
        self.assertEqual(self.track2.seats_used, 1)

        # track1 still frozen
        self.assertEqual(self.track1.seats_available, 1)
        self.assertEqual(self.track1.seats_reserved, 2)
        self.assertEqual(self.track1.seats_used, 0)

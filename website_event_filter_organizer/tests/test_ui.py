# Copyright 2019 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from dateutil.relativedelta import relativedelta
from odoo import fields
from odoo.tests.common import HttpCase


class UICase(HttpCase):
    def setUp(self):
        super().setUp()
        now = fields.Datetime.now()
        event_date_begin = now + relativedelta(days=1)
        event_date_end = now + relativedelta(days=3)
        self.event_1 = self.env['event.event'].create({
            'name': 'Event One',
            'user_id': self.env.ref('base.user_admin').id,
            'date_begin': event_date_begin,
            'date_end': event_date_end,
            'organizer_id': self.env.ref('base.res_partner_1').id,
            'event_type_id': self.env.ref('event.event_type_1').id,
            'website_published': True,
            'description': 'Test',
        })
        self.event_2 = self.env['event.event'].create({
            'name': 'Event Two',
            'date_begin': event_date_begin,
            'date_end': event_date_end,
            'organizer_id': self.env.ref('base.res_partner_2').id,
            'website_published': True,
        })

    def test_ui_website(self):
        """Test frontend tour."""
        tour = "website_event_filter_organizer"
        self.browser_js(
            url_path="/event",
            code="odoo.__DEBUG__.services['web_tour.tour']"
                 ".run('%s')" % tour,
            ready="odoo.__DEBUG__.services['web_tour.tour']"
                  ".tours.%s.ready" % tour,
        )

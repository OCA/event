# -*- coding: utf-8 -*-
# Copyright 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp.tests.common import HttpCase
from openerp import fields
from datetime import datetime, timedelta


class UICase(HttpCase):
    def test_ui_website(self):
        """Test frontend tour."""
        templates = {
            "website_event": {
                "event_left_column",
                "event_category",
                "event_location",
            },
            "website_event_filter_selector": {
                "city_left_column",
                "filter_city",
                "filter_country",
                "filter_date",
                "filter_type",
                "user_custom",
            },
        }
        with self.cursor() as cr:
            env = self.env(cr)
            # Create an event for today for assuring test correctness
            event_1 = env['event.event'].create({
                'name': 'Test event',
                'date_begin': fields.Datetime.now(),
                'date_end': fields.Datetime.now(),
                'website_published': True,
                'state': 'confirm',
            })
            # Create an old online event
            event_1.copy({
                'date_begin': datetime.today() - timedelta(days=60),
                'date_end': datetime.today() - timedelta(days=50),
                'address_id': False,
                'website_published': True,
            })
            # Enable all templates required for this test to work
            for model, xids in templates.iteritems():
                for xid in xids:
                    env.ref("%s.%s" % (model, xid)).active = True

        self.phantom_js(
            url_path="/event",
            code="odoo.__DEBUG__.services['web.Tour']"
                 ".run('website_event_filter_selector', 'test')",
            ready="odoo.__DEBUG__.services['web.Tour']"
                  ".tours.website_event_filter_selector")

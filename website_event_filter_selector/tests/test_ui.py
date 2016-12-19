# -*- coding: utf-8 -*-
# Copyright 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp.tests.common import HttpCase
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
            # Enable all templates required for this test to work
            for model, xids in templates.iteritems():
                for xid in xids:
                    env.ref("%s.%s" % (model, xid)).active = True
            # We need to have an old and an online event
            functional_webinar = env.ref("event.event_1")
            functional_webinar.address_id = False
            functional_webinar.date_begin = (
                datetime.today() - timedelta(days=60))
            functional_webinar.date_end = (
                datetime.today() - timedelta(days=50))
            # We need to make sure USA event starts today
            business_apps_conference = env.ref("event.event_2")
            business_apps_conference.date_begin = datetime.today()

        self.phantom_js(
            url_path="/event",
            code="odoo.__DEBUG__.services['web.Tour']"
                 ".run('website_event_filter_selector', 'test')",
            ready="odoo.__DEBUG__.services['web.Tour']"
                  ".tours.website_event_filter_selector")

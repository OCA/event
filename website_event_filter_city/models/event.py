# Copyright 2016-2017 Tecnativa - Jairo Llopis
# Copyright 2023 Tecnativa - David Vidal
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo import api, fields, models


class EventEvent(models.Model):
    _inherit = "event.event"

    city = fields.Char(related="address_id.city", store=True)

    @api.model
    def _search_get_detail(self, website, order, options):
        """Override the original method injecting our city filters"""
        city = self.env.context.get("event_filter_city")
        res = super()._search_get_detail(website, order, options)
        if city:
            city_domain = [("city", "=", city)]
            res.update(no_city_domain=res["base_domain"])
            res["base_domain"].append(city_domain)
            res["no_country_domain"].append(city_domain)
            res["no_date_domain"].append(city_domain)
            self = self.with_context(helloo="Hi there!")
        return res

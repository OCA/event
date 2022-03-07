# Copyright 2016-2017 Tecnativa - Jairo Llopis
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo import api, fields, models
from odoo.osv import expression


class EventEvent(models.Model):
    _inherit = "event.event"

    city = fields.Char(related="address_id.city", store=True)

    def _patch_event_filter_city_domain(self, domain, city):
        return expression.AND([domain, [("city", "=", city)]])

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        event_filter_city = self.env.context.get("event_filter_city")
        if event_filter_city:
            args = self._patch_event_filter_city_domain(args, event_filter_city)
        return super().search(
            args, offset=offset, limit=limit, order=order, count=count
        )

    @api.model
    def read_group(
        self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True
    ):
        event_filter_city = self.env.context.get("event_filter_city")
        if event_filter_city:
            domain = self._patch_event_filter_city_domain(domain, event_filter_city)
        return super().read_group(
            domain,
            fields,
            groupby,
            offset=offset,
            limit=limit,
            orderby=orderby,
            lazy=lazy,
        )

# Copyright 2016-2017 Tecnativa - Jairo Llopis
# Copyright 2023 Tecnativa - David Vidal
# Copyright 2026 Tecnativa - Adasat Torres
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.fields import Domain
from odoo.http import request, route

from odoo.addons.website_event.controllers.main import WebsiteEventController


class WebsiteEvent(WebsiteEventController):
    @route()
    def events(self, page=1, slug_tags=None, **searches):
        searches.setdefault("city", self.env._("All Cities"))
        # Inject our city in `_search_with_fuzzy` which ends up in `event.event`
        # `_search_get_detail` override.
        if searches["city"] != self.env._("All Cities"):
            request.website = request.website.with_context(
                event_filter_city=searches["city"]
            )
        response = super().events(page=page, slug_tags=slug_tags, **searches)
        # We can avoid ugly mokeypatching using the domains that we get in return from
        # the qcontext values, that are already injected with our city filters. This
        # way we can easily make city filter compatible with the other filters.
        qcontext = response.qcontext
        options = self._get_events_search_options(slug_tags, **qcontext["searches"])
        event_details = request.website._search_get_details("events", None, options)[0]
        domain_search = (
            Domain("name", "ilike", qcontext["searches"].get("search"))
            if qcontext["searches"].get("search")
            else Domain.TRUE
        )
        no_city_domain = Domain.AND(
            event_details.get("no_city_domain", event_details["base_domain"])
        )
        cities = request.env["event.event"]._read_group(
            no_city_domain & domain_search,
            aggregates=["__count"],
            groupby=["city"],
        )
        cities = [{"city": city[0], "city_count": city[1]} for city in cities]
        cities.insert(
            0,
            {
                "city_count": sum(x["city_count"] for x in cities),
                "city": self.env._("All Cities"),
            },
        )
        qcontext.update(
            {
                "cities": cities,
                "current_city": searches["city"],
            }
        )
        return response

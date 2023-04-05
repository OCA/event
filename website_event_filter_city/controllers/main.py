# Copyright 2016-2017 Tecnativa - Jairo Llopis
# Copyright 2023 Tecnativa - David Vidal
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _
from odoo.http import request, route

from odoo.addons.website_event.controllers.main import WebsiteEventController


class WebsiteEvent(WebsiteEventController):
    @route()
    def events(self, page=1, **searches):
        searches.setdefault("city", _("All Cities"))
        # Inject our city in `_search_with_fuzzy` which ends up in `event.event`
        # `_search_get_detail` override.
        if searches["city"] != _("All Cities"):
            request.website = request.website.with_context(
                event_filter_city=searches["city"]
            )
        response = super().events(page, **searches)
        # We can avoid ugly mokeypatching using the domains that we get in return from
        # the qcontext values, that are already injected with our city filters. This
        # way we can easily make city filter compatible with the other filters.
        qcontext = response.qcontext
        # We can rely in this domain by default
        domain = next(
            (
                domain
                for _, name, domain, _ in qcontext["dates"]
                if name == qcontext["current_date"]
            ),
            qcontext["dates"][0][2],
        )
        # This domain includes all the other filters
        if qcontext["current_country"]:
            domain = next(
                country_domain["__domain"]
                for country_domain in qcontext["countries"][1:]
                if country_domain["country_id"]
                and country_domain["country_id"][0] == qcontext["current_country"].id
            )
        # Otherwise, we can make some domain surgery to reuse the domain country for
        # our own purposes.
        elif len(qcontext["countries"]) > 1:
            domain = qcontext["countries"][1]["__domain"]
            countries_domain = [
                "|",
                ("country_id", "=", False),
                ("country_id", "!=", False),
            ]
            country_tuple_index = next(
                i for i, x in enumerate(domain) if len(x) > 1 and x[0] == "country_id"
            )
            domain.pop(country_tuple_index)
            domain[country_tuple_index : len(countries_domain)] = countries_domain
        # Finally we can use the domain we obtained to filter the cities in the controls
        cities = request.env["event.event"].read_group(
            domain, ["city"], groupby="city", orderby="city"
        )
        cities.insert(
            0,
            {
                "city_count": sum(x["city_count"] for x in cities),
                "city": _("All Cities"),
            },
        )
        qcontext["cities"] = cities
        qcontext["current_city"] = searches["city"]
        return response

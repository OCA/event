# Copyright 2016-2017 Tecnativa - Jairo Llopis
# Copyright 2023 Tecnativa - David Vidal
# Copyright 2026 Tecnativa - Adasat Torres
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.fields import Domain
from odoo.http import request, route

from odoo.addons.website_event.controllers.main import WebsiteEventController


class WebsiteEvent(WebsiteEventController):
    @route()
    def events(self, page=1, **searches):
        searches.setdefault("city", self.env._("All Cities"))
        # Inject our city in `_search_with_fuzzy` which ends up in `event.event`
        # `_search_get_detail` override.
        if searches["city"] != self.env._("All Cities"):
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
        if request.website.is_view_active("website_event.event_location"):
            country_groups = request.env["event.event"]._read_group(
                domain, ["country_id"], ["__count"], order="country_id"
            )
            countries = [
                {
                    "country_id_count": sum(count for __, count in country_groups),
                    "country_id": (0, self.env._("All Countries")),
                }
            ]
            for g_country, count in country_groups:
                countries.append(
                    {
                        "country_id_count": count,
                        "country_id": g_country
                        and (g_country.id, g_country.sudo().display_name),
                    }
                )
            qcontext.update({"countries": countries})
            if qcontext["current_country"]:
                domain = Domain(domain) & Domain(
                    [("country_id", "=", qcontext["current_country"].id)]
                )
        cities = request.env["event.event"]._read_group(
            domain,
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

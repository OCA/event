# Copyright 2016-2017 Jairo Llopis <jairo.llopis@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _
from odoo.http import request, route

from odoo.addons.website_event.controllers.main import WebsiteEventController


class WebsiteEvent(WebsiteEventController):
    @route()
    def events(self, page=1, **searches):
        # We need to set the defaults again for the pager that we need to reconstruct
        searches.setdefault("search", "")
        searches.setdefault("date", "all")
        searches.setdefault("type", "all")
        searches.setdefault("country", "all")
        searches.setdefault("city", _("All Cities"))
        if searches["city"] != _("All Cities"):
            request.context = dict(request.context, event_filter_city=searches["city"])
        # Get current render values
        response = super().events(page, **searches)
        # Drop the context key to avoid side effects
        context = dict(request.context)
        context.pop("event_filter_city", None)
        request.context = context
        # Controller pagers are quite encapsulated so we need to reconstruct it to add
        # our new stuff
        step = 12
        response.qcontext["pager"] = request.website.pager(
            url="/event",
            url_args=searches,
            total=step * response.qcontext["pager"]["page_count"],
            page=page,
            step=step,  # This is hardcoded upstream too
            scope=5,  # This is hardcoded upstream too
        )
        # Reconstruct domain from the response qcontext to obtain city render values
        domain = request.website.website_domain() + [
            ("state", "in", ("draft", "confirm", "done")),
        ]
        # Search term, if any
        if searches["search"]:
            domain.append(("name", "ilike", searches["search"]))
        # Date domain
        for date in response.qcontext["dates"]:
            if response.qcontext["searches"]["date"] == date[0]:
                domain += date[2]
                break
        # Type domain
        if response.qcontext["current_type"]:
            domain.append(("event_type_id", "=", response.qcontext["current_type"].id))
        # Country domain
        if response.qcontext["current_country"]:
            domain += [
                "|",
                ("country_id", "=", response.qcontext["current_country"].id),
                ("country_id", "=", False),
            ]
        elif searches.get("country", "") == "online":
            domain.append(("country_id", "=", False))
        # Handle city search
        Event = request.env["event.event"].with_context(request.context)
        cities = Event.read_group(domain, ["city"], groupby="city", orderby="city")
        cities.insert(
            0,
            {
                "city_count": sum(x["city_count"] for x in cities),
                "city": _("All Cities"),
            },
        )
        response.qcontext["cities"] = cities
        response.qcontext["current_city"] = searches["city"]
        return response

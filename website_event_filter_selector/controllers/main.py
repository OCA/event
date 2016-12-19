# -*- coding: utf-8 -*-
# © 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp import _, http
from openerp.addons.website_event.controllers.main import website_event


class WebsiteEvent(website_event):
    @http.route()
    def events(self, page=1, **searches):
        # Get current render values
        searches.setdefault("city", "all")
        result = super(WebsiteEvent, self).events(page, **searches)
        values = result.qcontext
        searches = values["searches"]

        # Regenerate current domain. Ideally, upstream would make all this in a
        # separate method and make our life easier, but not happening now.
        domain = [("state", "in", ("draft", "confirm", "done"))]

        # Date domain
        for date in values["dates"]:
            if values['searches']['date'] == date[0]:
                domain += date[2]
                break

        # Type domain
        if values["current_type"]:
            domain.append(("event_type_id", "=", values["current_type"].id))

        # Country domain
        if values["current_country"]:
            domain.append(("country_id", "=", values["current_country"].id))
        elif searches["country"] == 'online':
            domain.append(("country_id", "=", False))

        # Handle city search
        event_obj = http.request.env["event.event"].with_context(
            http.request.context
        )
        cities = event_obj.read_group(
            domain,
            ["city"],
            groupby="city",
            orderby="city")
        cities.insert(0, {"city_count": sum(x['city_count'] for x in cities),
                          "city": _("All Cities"),
                          "key": "all"})
        if searches["city"] != "all":
            domain.append(("city", "=", searches["city"]))
        values["cities"] = cities
        values["current_city"] = searches["city"]

        # We need a new pager now
        step = 10  # This is hardcoded upstream too
        values["pager"] = http.request.website.pager(
            url="/event",
            url_args={
                "date": searches.get("date"),
                "type": searches.get("type"),
                "country": searches.get("country"),
                "city": searches.get("city"),
            },
            total=event_obj.search(domain, count=True),
            page=page,
            step=step,  # This is hardcoded upstream too
            scope=5)

        # Return new event results
        order = 'website_published desc, date_begin'
        if searches["date"] == "old":
            order += " desc"
        values["event_ids"] = event_obj.search(
            domain,
            limit=step,
            offset=values["pager"]["offset"],
            order=order)

        # Return changed template
        result.qcontext = values
        return result

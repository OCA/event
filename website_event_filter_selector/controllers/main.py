# Copyright 2016-2017 Jairo Llopis <jairo.llopis@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, http
from odoo.addons.website_event.controllers.main import WebsiteEventController


class WebsiteEvent(WebsiteEventController):
    @http.route()
    def events(self, page=1, **searches):
        # Get current render values
        searches.setdefault("city", "all")
        result = super(WebsiteEvent, self).events(page, **searches)
        values = result.qcontext
        searches = values["searches"]

        # Regenerate current domain. Ideally, upstream would make all this in a
        # separate method and make our life easier, but not happening now.
        domain = http.request.website.website_domain() + [
            ("state", "in", ("draft", "confirm", "done")),
        ]

        def dom_without(without):
            return [leaf for leaf in domain if leaf[0] not in without]

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
        Event = http.request.env["event.event"].with_context(
            http.request.context
        )
        cities = Event.read_group(
            domain,
            ["city"],
            groupby="city",
            orderby="city")
        cities.insert(0, {"city_count": sum(x['city_count'] for x in cities),
                          "city": _("All Cities"),
                          "key": "all"})
        values["cities"] = cities
        values["current_city"] = searches["city"]

        if searches["city"] != "all":
            domain.append(("city", "=", searches["city"]))
            # Patch type count
            values["types"][1:] = Event.read_group(
                dom_without({"event_type_id"}),
                ["id", "event_type_id"],
                groupby=["event_type_id"],
                orderby="event_type_id")
            values["types"][0]["event_type_id_count"] = sum(
                int(type_['event_type_id_count'])
                for type_ in values["types"][1:])
            # Patch country count
            values["countries"][1:] = Event.read_group(
                dom_without({"country_id"}),
                ["id", "country_id"],
                groupby="country_id",
                orderby="country_id")
            values["countries"][0]["country_id_count"] = sum(
                int(type_['country_id_count'])
                for type_ in values["countries"][1:])
            # Patch date count
            for date in values["dates"]:
                if date[0] != 'old':
                    date[3] = Event.search_count(
                        dom_without({"date_end", "date_begin"}) + date[2])

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
            total=Event.search(domain, count=True),
            page=page,
            step=step,  # This is hardcoded upstream too
            scope=5)

        # Return new event results
        order = 'website_published desc, date_begin'
        if searches["date"] == "old":
            order += " desc"
        values["event_ids"] = Event.search(
            domain,
            limit=step,
            offset=values["pager"]["offset"],
            order=order)

        # Return changed template
        result.qcontext = values
        return result

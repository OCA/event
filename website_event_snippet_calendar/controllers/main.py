# Copyright 2018 Tecnativa - Jairo Llopis
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from datetime import date, timedelta
from openerp.fields import Date
from openerp.http import Controller, request, route


class EventCalendar(Controller):
    @route("/website_event_snippet_calendar/days_with_events",
           auth="public", type="json")
    def days_with_events(self, start, end):
        """Let visitors know when are there going to be any events.

        :param start string:
            Search events from that date.

        :param end string:
            Search events until that date.
        """
        events = request.env["event.event"].search([
            "|",
            ("date_begin", "<=", end),
            ("date_end", ">=", start),
        ])
        days = set()
        one_day = timedelta(days=1)
        start = Date.from_string(start)
        end = Date.from_string(end)
        for event in events:
            now = max(Date.from_string(event.date_begin), start)
            event_end = min(Date.from_string(event.date_end), end)
            while now <= event_end:
                days.add(now)
                now += one_day
        return [Date.to_string(day) for day in days]

    @route("/website_event_snippet_calendar/events_for_day",
           auth="public", type="json")
    def events_for_day(self, day=None, limit=None):
        """List events for a given day.

        :param day string:
            Date in a string. If ``None``, we'll search for upcoming events
            from today up to specified limit.

        :param limit int:
            How many results to return.
        """
        ref = day or Date.to_string(date.today())
        domain = [
            ("date_end", ">=", ref),
        ]
        if day:
            domain.append(("date_begin", "<=", ref))
        return request.env["event.event"].search_read(
            domain=domain,
            limit=limit,
            fields=[
                "date_begin_pred_located",
                "name",
                "event_type_id",
                "website_published",
                "website_url",
            ],
        )

    @route("/website_event_snippet_calendar/embed",
           auth="public", type="http", website=True)
    def embed(self, *args, **kwargs):
        return request.render("website_event_snippet_calendar.embed")

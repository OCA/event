# Copyright 2021 Moka Tourisme (https://www.mokatourisme.fr).
# @author Iván Todorovich <ivan.todorovich@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from werkzeug.exceptions import NotFound

from odoo.http import Controller, content_disposition, request, route


class EventSessionController(Controller):
    @route(
        """/event/session/<model("event.session"):event_session>/ics""",
        type="http",
        auth="public",
    )
    def event_session_ics_file(self, event_session, **kwargs):
        """Similar to core :meth:`~event_ics_file` for event.event"""
        files = event_session._get_ics_file()
        if event_session.id not in files:  # pragma: no cover
            return NotFound()
        content = files[event_session.id]
        disposition = content_disposition(f"{event_session.name}.ics")
        return request.make_response(
            content,
            [
                ("Content-Type", "application/octet-stream"),
                ("Content-Length", len(content)),
                ("Content-Disposition", disposition),
            ],
        )

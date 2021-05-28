from odoo import http
from odoo.exceptions import AccessError, MissingError
from odoo.http import content_disposition, request

from odoo.addons.portal.controllers.portal import CustomerPortal


class CustomerPortal(CustomerPortal):
    @http.route(
        [
            "/my/orders/<int:order_id>/event/<int:event_id>/badge",
            "/my/orders/<int:order_id>/event/<int:event_id>/badge/<int:reg_id>",
        ],
        type="http",
        auth="public",
        website=True,
    )
    def portal_order_event_badge(
        self, order_id, event_id, reg_id=None, access_token=None, download=False, **kw
    ):
        """Download event registration badges from sale order portal page."""
        try:
            order_sudo = self._document_check_access(
                "sale.order", order_id, access_token=access_token
            )
        except (AccessError, MissingError):
            return request.redirect("/my")
        # Get sale order downloadable registrations
        registrations = order_sudo.event_registration_ids.filtered(
            lambda r: (
                r.state == "open"
                and r.event_id.id == event_id
                and r.event_id.portal_badge_download
            )
        )
        if not registrations:  # pragma: no cover
            return request.redirect("/my")
        # Check if registration_id belongs to the sale order
        if reg_id is not None:
            if reg_id not in registrations.ids:  # pragma: no cover
                return request.redirect("/my")
            registrations = registrations.browse(reg_id)
        # Render report
        report_sudo = request.env.ref("event.report_event_registration_badge").sudo()
        report = report_sudo.render(registrations.ids)[0]
        reporthttpheaders = [
            ("Content-Type", "application/pdf"),
            ("Content-Length", len(report)),
        ]
        # Download
        if download:
            filename = (
                "Badges.pdf"
                if len(registrations) > 1
                else "Badge - %s.pdf" % registrations.name
            )
            reporthttpheaders.append(
                ("Content-Disposition", content_disposition(filename))
            )
        return request.make_response(report, headers=reporthttpheaders)

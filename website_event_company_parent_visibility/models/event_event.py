# Copyright 2026 INVITU (<https://www.invitu.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class EventEvent(models.Model):
    _inherit = "event.event"

    def _search_get_detail(self, website, order, options):
        detail = super()._search_get_detail(website, order, options)
        if website and website.company_id:
            company = website.company_id
            extra_domain = [
                "|",
                ("company_id", "=", False),
                "|",
                ("company_id", "=", company.id),
                "&",
                ("company_id", "child_of", company.ids),
                ("company_id.share_events_with_parents", "=", True),
            ]
            detail["base_domain"] = detail.get("base_domain", []) + [extra_domain]
            for key in ("no_date_domain", "no_country_domain"):
                if key in detail:
                    detail[key] = detail[key] + [extra_domain]
        return detail

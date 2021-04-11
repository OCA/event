# Copyright 2016 Tecnativa - Sergio Teruel
# Copyright 2016 Tecnativa - Vicent Cubells
# Copyright 2018 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import timedelta

from odoo import api, fields, models


class EventEvent(models.Model):
    _inherit = "event.event"

    @api.model
    def _send_event_template(self, events, template, partner_ids):
        ctx = self.env.context.copy()
        ctx.update({"events": events.sorted(lambda x: x.date_begin)})
        for partner_id in partner_ids:
            lang = self.env["res.partner"].browse(partner_id).lang
            # Set the contexts with the partner's language
            ctx.update({"events": ctx["events"].with_context(lang=lang), "lang": lang})
            template.with_context(ctx).send_mail(partner_id)

    @api.model
    def run_event_email_reminder(
        self,
        days=7,
        draft_events=False,
        near_events=False,
        template_id=None,
        partner_ids=None,
    ):
        """Enqueue mail with a summary of events that begin on days parameter

        :param int days:
            Number of days to reminder when events start (or end, if negative).
        :param bool draft_events: filter by draft events too.
        :param bool near_events: If you want receive the events which start
          between now and limit date.
        :param int template_id: id of a template or None.
        :param list(int) partner_ids: list of IDs of the partners we
          want to notify.
        """
        today = fields.Date.context_today(self)
        limit_date = today + timedelta(days=days)
        if draft_events:
            domain = [("state", "in", ["draft", "confirm"])]
        else:
            domain = [("state", "=", "confirm")]
        if not near_events:
            domain.extend(
                [("date_begin", ">=", limit_date), ("date_begin", "<=", limit_date)]
            )
        elif today > limit_date:
            domain.extend([("date_end", ">=", limit_date), ("date_end", "<=", today)])
        else:
            domain.extend(
                [("date_begin", ">=", today), ("date_begin", "<=", limit_date)]
            )
        events = self.search(domain)
        if events:
            if not template_id:
                template = self.env.ref(
                    "event_email_reminder.event_email_reminder_template"
                )
            else:
                template = self.env["mail.template"].browse(template_id)
            if partner_ids:
                self._send_event_template(events, template, partner_ids)
            else:
                for user in events.mapped("user_id"):
                    events = events.filtered(lambda x: x.user_id == user)
                    self._send_event_template(
                        events, template, user.partner_id.ids,
                    )
        return True

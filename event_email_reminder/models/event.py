# -*- coding: utf-8 -*-
# © 2016 Sergio Teruel <sergio.teruel@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models
from datetime import datetime, timedelta

from openerp.tools import DEFAULT_SERVER_DATE_FORMAT


class EventEvent(models.Model):
    _inherit = 'event.event'

    @api.model
    def run_event_email_reminder(
            self, days=7, near_events=False, template_id=None):
        """
        @param days: number of days to reminder when events star
        @param near_events: If you want receive the events which start
        between now and limit date
        @param template_name: Name of a template or None
        @return:
        """
        today = fields.Date.context_today(self)
        limit_date = datetime.strptime(
            today, DEFAULT_SERVER_DATE_FORMAT) + timedelta(days=days)

        domain = [('state', '=', 'confirm')]
        if not near_events:
            domain.extend([
                ('date_begin', '>=', '%s 00:00:00' % (
                    fields.Date.to_string(limit_date))),
                ('date_begin', '<=', '%s 23:59:59' % (
                    fields.Date.to_string(limit_date)))
            ])
        else:
            domain.extend([
                ('date_begin', '>=', '%s 00:00:00' % today),
                ('date_begin', '<=', '%s 23:59:59' % (
                    fields.Date.to_string(limit_date)))
            ])
        events = self.search(domain)
        if events:
            if not template_id:
                template = self.env.ref(
                    'event_email_reminder.event_email_reminder_template')
            else:
                template = self.env['email.template'].browse(template_id)
            for user in events.mapped('user_id'):
                ctx = self.env.context.copy()
                event_by_user = events.filtered(lambda x: x.user_id == user)
                ctx.update({
                    'events': event_by_user.sorted(lambda x: x.date_begin),
                })
                template.with_context(ctx).send_mail(user.partner_id.id)
        return True

# -*- coding: utf-8 -*-
# Copyright 2017 David Vidal<david.vidal@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime
from odoo import api, fields, models, tools
import logging

_logger = logging.getLogger(__name__)

try:
    from odoo.addons.event.models.event_mail import _INTERVALS
except ImportError:
    _logger.debug('Can not import events module.')


class EventMailScheduler(models.Model):
    _inherit = 'event.mail'

    session_id = fields.Many2one(
        comodel_name='event.session',
        string='Session',
        ondelete='cascade',
    )

    @api.multi
    def _compute_done(self):
        super(EventMailScheduler, self)._compute_done()
        for event_mail in self:
            if (event_mail.session_id and
                    event_mail.interval_type not in
                    ['before_event', 'after_event']):
                event_mail.done = (
                    True if event_mail.event_id.sessions_count > 0 and
                    not event_mail.session_id else
                    len(event_mail.mail_registration_ids) == len(
                        event_mail.session_id.registration_ids) and
                    all(line.mail_sent for line in
                        event_mail.mail_registration_ids)
                )

    @api.multi
    def _compute_scheduled_date(self):
        super(EventMailScheduler, self)._compute_scheduled_date()
        for event_mail in self:
            if event_mail.event_id.state in ['confirm', 'done'] and \
                    event_mail.session_id:
                if event_mail.interval_type == 'before_event':
                    date, sign = event_mail.session_id.date, -1
                else:
                    date, sign = event_mail.session_id.date_end, 1
                event_mail.scheduled_date = datetime.strptime(
                    date, tools.DEFAULT_SERVER_DATETIME_FORMAT) + _INTERVALS[
                    event_mail.interval_unit](sign * event_mail.interval_nbr)


class EventMailRegistration(models.Model):
    _inherit = 'event.mail.registration'

    @api.multi
    @api.depends('registration_id', 'scheduler_id.interval_unit',
                 'scheduler_id.interval_type')
    def _compute_scheduled_date(self):
        super(EventMailRegistration, self)._compute_scheduled_date()
        for event_mail_reg in self:
            if (event_mail_reg.registration_id and
                    event_mail_reg.registration_id.session_id):
                date_open = event_mail_reg.registration_id.session_id.date
                date_open_datetime = date_open and datetime.strptime(
                    date_open, tools.DEFAULT_SERVER_DATETIME_FORMAT
                ) or fields.datetime.now()
                event_mail_reg.scheduled_date = (
                    date_open_datetime +
                    _INTERVALS[event_mail_reg.scheduler_id.interval_unit](
                        event_mail_reg.scheduler_id.interval_nbr))

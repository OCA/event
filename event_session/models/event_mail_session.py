# Copyright 2021 Moka Tourisme (https://www.mokatourisme.fr).
# @author Iván Todorovich <ivan.todorovich@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging
import threading

from odoo import api, fields, models

from odoo.addons.event.models.event_mail import _INTERVALS

_logger = logging.getLogger(__name__)


class EventMailSession(models.Model):
    _name = "event.mail.session"
    _inherits = {"event.mail": "scheduler_id"}
    _description = "Event Session Automated Mailing"

    scheduler_id = fields.Many2one(
        comodel_name="event.mail",
        string="Event Mail Scheduler",
        ondelete="cascade",
        auto_join=True,
        required=True,
    )
    session_id = fields.Many2one(
        comodel_name="event.session",
        string="Session",
        ondelete="cascade",
        required=True,
    )
    mail_registration_ids = fields.One2many(
        comodel_name="event.mail.registration",
        inverse_name="session_scheduler_id",
    )
    scheduled_date = fields.Datetime(
        compute="_compute_scheduled_date",
        store=True,
    )
    mail_done = fields.Boolean("Sent", copy=False, readonly=True)
    mail_count_done = fields.Integer("# Sent", copy=False, readonly=True)

    @api.depends(
        "session_id",
        "session_id.date_begin",
        "session_id.date_end",
        "scheduler_id",
        "interval_type",
        "interval_unit",
        "interval_nbr",
    )
    def _compute_scheduled_date(self):
        """
        Similar to core's :meth:`event.models.event_mail._compute_scheduled_date`,
        only here we take values from the `event.session` instead.
        """
        for scheduler in self:
            if scheduler.interval_type == "after_sub":
                date, sign = scheduler.session_id.create_date, 1
            elif scheduler.interval_type == "before_event":
                date, sign = scheduler.session_id.date_begin, -1
            else:
                date, sign = scheduler.session_id.date_end, 1
            delta = _INTERVALS[scheduler.interval_unit](sign * scheduler.interval_nbr)
            scheduler.scheduled_date = date + delta if date else False

    def _get_new_event_registrations(self):
        registrations = self.session_id.registration_ids.filtered_domain(
            [("state", "not in", ("cancel", "draft"))]
        )
        return registrations - self.mail_registration_ids.registration_id

    def _prepare_mail_registration_vals(self, registration):
        self.ensure_one()
        return {
            "registration_id": registration.id,
            "scheduler_id": self.scheduler_id.id,
            "session_scheduler_id": self.id,
        }

    def _create_missing_mail_registrations(self, registrations):
        vals_list = []
        for scheduler in self:
            vals_list += [
                scheduler._prepare_mail_registration_vals(registration)
                for registration in registrations
            ]
        if vals_list:
            return self.env["event.mail.registration"].create(vals_list)
        return self.env["event.mail.registration"]

    def execute(self):
        """
        Similar to core's :meth:`event.models.event_mail.execute`, only here we
        take values from the `event.session` instead.
        """
        for scheduler in self:
            now = fields.Datetime.now()
            if scheduler.interval_type == "after_sub":
                new_registrations = self._get_new_event_registrations()
                scheduler._create_missing_mail_registrations(new_registrations)
                # execute scheduler on registrations
                scheduler.mail_registration_ids.execute()
                total_sent = len(
                    scheduler.mail_registration_ids.filtered(lambda reg: reg.mail_sent)
                )
                scheduler.update(
                    {
                        "mail_done": total_sent
                        >= (
                            scheduler.session_id.seats_reserved
                            + scheduler.session_id.seats_used
                        ),
                        "mail_count_done": total_sent,
                    }
                )
            else:
                # before or after event -> one shot email
                if scheduler.mail_done or scheduler.notification_type != "mail":
                    continue  # pragma: no cover
                # no template -> ill configured, skip and avoid crash
                if not scheduler.template_ref:  # pragma: no cover
                    continue
                # do not send emails if the mailing was scheduled before the event
                # but the event is over
                if scheduler.scheduled_date <= now and (
                    scheduler.interval_type != "before_event"
                    or scheduler.session_id.date_end > now
                ):
                    scheduler.session_id.mail_attendees(scheduler.template_ref.id)
                    scheduler.update(
                        {
                            "mail_done": True,
                            "mail_count_done": scheduler.session_id.seats_reserved
                            + scheduler.session_id.seats_used,
                        }
                    )
        return True

    @api.model
    def schedule_communications(self, autocommit=False):
        """
        Similar to core's :meth:`event.models.event_mail.schedule_communications`.
        """
        schedulers = self.search(
            [("mail_done", "=", False), ("scheduled_date", "<=", fields.Datetime.now())]
        )

        for scheduler in schedulers:
            try:
                # Prevent a mega prefetch of the registration ids of all the events
                # of all the schedulers
                self.browse(scheduler.id).execute()
            except Exception as e:  # pragma: no cover
                _logger.exception(e)
                self.env["event.mail"]._warn_template_error(scheduler, e)
            else:
                if autocommit and not getattr(
                    threading.currentThread(), "testing", False
                ):  # pragma: no cover
                    self.env.cr.commit()  # pylint: disable=invalid-commit
        return True

# Copyright 2021 Tecnativa - Jairo Llopis
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tests.common import Form

_logger = logging.getLogger(__name__)


class CRMLead(models.Model):
    _inherit = "crm.lead"

    event_type_website_url = fields.Char(compute="_compute_event_type_url")
    auto_invite_warning = fields.Boolean(compute="_compute_auto_invite_warning")

    @api.depends("event_type_id")
    def _compute_event_type_url(self):
        """Know if lead can be invited to event type."""
        for lead in self:
            lead.event_type_website_url = False
            if not lead.event_type_id:
                continue
            domain = lead.event_type_id._published_events_domain()
            events = self.env["event.event"].search(domain, limit=1)
            if events:
                lead.event_type_website_url = "/event?type=%d" % lead.event_type_id.id

    @api.depends("event_type_id", "company_id")
    def _compute_auto_invite_warning(self):
        """Used for warning purposes in the lead/opportunity form view"""
        self.auto_invite_warning = False
        for lead in self.filtered("event_type_website_url"):
            # If there's no website for the lead/opportunity company we'll warn the user
            # that the invitation won't be sent.
            website = lead.company_id and self.env["website"].search(
                [("company_id", "=", lead.company_id.id)]
            )
            if not lead.company_id or not website:
                lead.auto_invite_warning = True

    @api.model
    def _cron_auto_invite_website_event_type(self):
        """Invite automatically leads/opportunities to website event categories. We
        should be aware of multi-company + multi-website scenarios in which we want
        the link sent to the customer launched only when there are events for their
        company leads. Moreover, we want to send the proper base url link for the
        proper filtered events.
        - crm.leads company isn't mandatory (although unusual). We ignore these cases
          as we can't determine properly what to send to the user.
        - event.event website isn't mandatory: This means that the event will be
          available on all the sites belonging to the company.
        - There could multiple websites in one company: if the event has the link to
          one of them, we'll get the proper base url.
        - There could be no website in a company. In this case, it won't make sense
          to send anything to the customer as he won't be able to reach it.
        """
        # Find opportunities
        leads = self.search(
            [
                ("email_from", "!=", False),
                ("event_type_id", "!=", False),
                ("stage_id.auto_invite_website_event_type", "=", True),
            ]
        )
        available_event_types = leads.mapped("event_type_id")
        published_events = self.env["event.event"].search(
            available_event_types._published_events_domain()
        )
        # Leads with falsy company won't get invitations. It's not usual anyway
        for company in leads.company_id:
            company_leads = leads.filtered(lambda l: l.company_id == company)
            company_published_events = published_events.filtered(
                lambda e: e.company_id == company
            )
            if not company_published_events.event_type_id:
                continue
            # Events could have no website (they'd be available for all the websites in
            # the company). For that case we'll get the first available website.
            for website in list(company_published_events.website_id) + [
                self.env["website"]
            ]:
                if not website:
                    default_website = website.search(
                        [("company_id", "=", company.id)], limit=1
                    )
                    # If there's no website for that company it makes no sense to inform
                    # the users
                    if not default_website:
                        continue
                    base_url = default_website.get_base_url()
                else:
                    base_url = website.get_base_url()
                company_leads.with_context(
                    base_url=base_url
                )._invite_to_website_event_type(
                    company_published_events.filtered(
                        lambda x: x.website_id == website
                    ).event_type_id
                )

    def _invite_to_website_event_type(self, published_event_types):
        for lead in self:
            if lead.event_type_id not in published_event_types:
                continue
            try:
                action = lead.with_context(
                    skip_website_event_crm_warning=True
                ).action_invite_to_website_event_type()
                assert action["res_model"] == "mail.compose.message"
                composer = Form(
                    self.env["mail.compose.message"].with_context(
                        active_id=lead.id,
                        active_ids=lead.ids,
                        active_model=lead._name,
                        mail_notify_force_send=False,
                        **action["context"],
                    ),
                    action["view_id"],
                )
                composer.save()._action_send_mail()
            except Exception:
                _logger.exception("Failure trying to invite to website event type.")

    def action_invite_to_website_event_type(self):
        """Open mail to invite customer to subscribe on website."""
        if (
            not self.env.context.get("skip_website_event_crm_warning")
            and self.auto_invite_warning
        ):
            raise UserError(
                _(
                    "It's not possible to determine to propose events if the company "
                    "isn't set or if the company has no websites. So no invitation "
                    "will be sent for this lead"
                )
            )
        if not self.event_type_id or not self.event_type_website_url:
            raise UserError(_("Select one event type with published events."))
        compose_form_id = self.env.ref("mail.email_compose_message_wizard_form").id
        template_id = self.env.ref(
            "website_event_crm_invitation.crm_lead_event_type_tpl"
        ).id
        # When manually sending the invitation we won't have the proper context and
        # get_base_url isn't very smart in this Odoo version
        base_url_object = (
            fields.first(
                self.env["website"].search([("company_id", "=", self.company_id.id)])
            )
            or self
        )
        return {
            "context": {
                "auto_advance_stage": True,
                "default_composition_mode": "comment",
                "default_model": "crm.lead",
                "default_res_id": self.id,
                "default_template_id": template_id,
                "default_use_template": True,
                "force_email": True,
                "base_url": self.env.context.get(
                    "base_url", base_url_object.get_base_url()
                ),
            },
            "name": _("Invite to visit website"),
            "res_model": "mail.compose.message",
            "target": "new",
            "type": "ir.actions.act_window",
            "view_id": compose_form_id,
            "view_mode": "form",
            "view_type": "form",
            "views": [(compose_form_id, "form")],
        }

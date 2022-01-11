# Copyright 2021 Tecnativa - Jairo Llopis
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tests.common import Form

_logger = logging.getLogger(__name__)


class CRMLead(models.Model):
    _inherit = "crm.lead"

    event_type_website_url = fields.Char(
        compute="_compute_event_type_url",
    )

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
                website = False
                if "website_id" in self.env.context:
                    website = self.env["website"].get_current_website(
                        fallback=False
                    )
                if not website:
                    website = self.env["website"].search([
                        ("company_id", "=", lead.company_id.id)
                    ], limit=1)
                if website:
                    lead.event_type_website_url = "%s/event?type=%d" % (
                        website._get_http_domain(), lead.event_type_id.id
                    )

    @api.model
    def _cron_auto_invite_website_event_type(self):
        """Invite automatically leads/opportunities to website event categories."""
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
        published_event_types = published_events.mapped("event_type_id")
        if not published_event_types:
            return
        for lead in leads:
            if lead.event_type_id not in published_event_types:
                continue
            try:
                action = lead.action_invite_to_website_event_type()
                assert action["res_model"] == "mail.compose.message"
                composer = Form(
                    self.env["mail.compose.message"]
                    .with_context(
                        active_id=lead.id,
                        active_ids=lead.ids,
                        active_model=lead._name,
                        mail_notify_force_send=False,
                        **action["context"],
                    ),
                    action['view_id']
                )
                composer.save().send_mail()
            except Exception:
                _logger.exception("Failure trying to invite to website event type.")

    def action_invite_to_website_event_type(self):
        """Open mail to invite customer to subscribe on website."""
        if not self.event_type_id or not self.event_type_website_url:
            raise UserError(_("Select one event type with published events."))
        compose_form_id = self.env.ref("mail.email_compose_message_wizard_form").id
        template_id = self.env.ref("website_event_crm.crm_lead_event_type_tpl").id
        return {
            "context": {
                "auto_advance_stage": True,
                "default_composition_mode": "comment",
                "default_model": "crm.lead",
                "default_res_id": self.id,
                "default_template_id": template_id,
                "default_use_template": True,
                "force_email": True,
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

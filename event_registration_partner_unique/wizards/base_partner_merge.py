# Copyright 2023 Tecnativa - David Vidal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class BasePartnerMergeAutomaticWizard(models.TransientModel):
    _inherit = "base.partner.merge.automatic.wizard"

    merge_duplicated_registrations = fields.Boolean(
        help="If the merged partners were linked to registrations in an event that had "
        "unique attendees flag we'll take only the oldest one",
    )

    def action_merge(self):
        """Allow to get rid of duplicated registrations linked to the merged partners"""
        if not self.merge_duplicated_registrations:
            return super().action_merge()
        # Skip the constraints and do the partner merge first
        res = super(
            BasePartnerMergeAutomaticWizard,
            self.with_context(skip_registration_partner_unique=True),
        ).action_merge()
        # Now let's merge the attendees
        dupes_to_unlink = self.env["event.registration"]
        partner_registrations = self.dst_partner_id.event_registration_ids
        for attendee, dupes in partner_registrations._find_duplicated_attendees():
            # Keep the oldest one -> min id will be
            event_attendees_for_partner = attendee + dupes
            attendee_to_keep = min(event_attendees_for_partner, key=lambda x: x.id)
            dupes_to_unlink += event_attendees_for_partner - attendee_to_keep
        # Call with skipping context to avoid triggering the constraint again
        dupes_to_unlink.with_context(skip_registration_partner_unique=True).unlink()
        return res

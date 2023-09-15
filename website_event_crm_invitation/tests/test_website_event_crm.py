# Copyright 2022 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.fields import first

from odoo.addons.crm_event.tests.test_event_type import CrmEventCase


class WebsiteEventCrmTests(CrmEventCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company_2 = cls.env["res.company"].create({"name": "Test Company 2"})
        cls.website_1 = cls.env["website"].create(
            {"name": "Test WWW 1", "domain": "www.test-www-1.test"}
        )
        cls.website_2 = cls.env["website"].create(
            {"name": "Test WWW 2", "domain": "www.test-www-2.test"}
        )
        cls.a_events.website_id = cls.website_1
        cls.b_events.website_id = cls.website_2
        cls.invite_stage = cls.env["crm.stage"].create(
            {"name": "Test Pending", "auto_invite_website_event_type": True}
        )
        # An opportunity which we'll should be invited to the event
        cls.opportunity_1 = first(cls.opportunities).copy(
            {"email_from": "test@test.com", "stage_id": cls.invite_stage.id}
        )
        # An opportunity from another company wich won't get any invitation
        cls.opportunity_2 = first(cls.opportunities).copy(
            {
                "email_from": "test@test.com",
                "stage_id": cls.invite_stage.id,
                "company_id": cls.company_2.id,
            }
        )
        # An opportunity from antother type
        cls.opportunity_3 = first(cls.opportunities).copy(
            {
                "email_from": "test@test.com",
                "stage_id": cls.invite_stage.id,
                "event_type_id": cls.type_b.id,
            }
        )
        # An opportunity on a stage without auto invite
        cls.opportunity_4 = first(cls.opportunities).copy(
            {"email_from": "test@test.com"}
        )

    def _lead_msg(self, lead):
        return "\n".join(lead.message_ids.mapped("body"))

    def _test_event_type_invitation(self, lead):
        return "/event?type={}".format(lead.event_type_id.id) in self._lead_msg(lead)

    def test_event_crm_invite_cron(self):
        self.a_events.website_published = True
        # No invitation until cron is run
        self.assertFalse(self._test_event_type_invitation(self.opportunity_1))
        self.assertFalse(self._test_event_type_invitation(self.opportunity_2))
        self.assertFalse(self._test_event_type_invitation(self.opportunity_3))
        self.assertFalse(self._test_event_type_invitation(self.opportunity_4))
        self.env["crm.lead"]._cron_auto_invite_website_event_type()
        # Opportunity 1 event category has published events available
        self.assertTrue(self._test_event_type_invitation(self.opportunity_1))
        # We also get the right base url
        self.assertTrue(self.website_1.domain in self._lead_msg(self.opportunity_1))
        # Opportunity 2 is from another company. It should not receive a notification
        self.assertFalse(self._test_event_type_invitation(self.opportunity_2))
        # The type of opportunity 3 doesn't have event available
        self.assertFalse(self._test_event_type_invitation(self.opportunity_3))
        # Opportunity 4 is in a stage with no auto invitation mail
        self.assertFalse(self._test_event_type_invitation(self.opportunity_4))

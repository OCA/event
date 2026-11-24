# Copyright 2026 INVITU (<https://www.invitu.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import base64

from psycopg2 import IntegrityError

from odoo import fields
from odoo.tests.common import TransactionCase
from odoo.tools import mute_logger


class TestWebsiteEventQuestionsAttachment(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.event = cls.env["event.event"].create(
            {
                "name": "Test Event",
                "date_begin": fields.Datetime.now(),
                "date_end": fields.Datetime.now(),
            }
        )
        cls.question = cls.env["event.question"].create(
            {
                "title": "Upload your document",
                "question_type": "attachment",
                "event_id": cls.event.id,
            }
        )
        cls.registration = cls.env["event.registration"].create(
            {
                "event_id": cls.event.id,
                "name": "Test Attendee",
            }
        )
        cls.attachment = cls.env["ir.attachment"].create(
            {
                "name": "test_doc.pdf",
                "datas": base64.b64encode(b"dummy content"),
                "res_model": "event.registration",
                "res_id": cls.registration.id,
            }
        )

    def test_question_type_attachment(self):
        """Question type 'attachment' is available."""
        self.assertEqual(self.question.question_type, "attachment")

    def test_answer_with_attachment(self):
        """Registration answer with attachment is valid."""
        answer = self.env["event.registration.answer"].create(
            {
                "question_id": self.question.id,
                "registration_id": self.registration.id,
                "value_attachment_id": self.attachment.id,
            }
        )
        self.assertEqual(answer.value_attachment_id, self.attachment)

    @mute_logger("odoo.sql_db")
    def test_answer_without_value_raises(self):
        """Registration answer with no value raises constraint error."""
        with self.assertRaises(IntegrityError):
            self.env["event.registration.answer"].create(
                {
                    "question_id": self.question.id,
                    "registration_id": self.registration.id,
                }
            )

    def test_multiple_attachment_questions(self):
        """Multiple attachment questions per registration are supported."""
        question2 = self.env["event.question"].create(
            {
                "title": "Upload your ID",
                "question_type": "attachment",
                "event_id": self.event.id,
            }
        )
        attachment2 = self.env["ir.attachment"].create(
            {
                "name": "id.jpg",
                "datas": base64.b64encode(b"id content"),
                "res_model": "event.registration",
                "res_id": self.registration.id,
            }
        )
        answer1 = self.env["event.registration.answer"].create(
            {
                "question_id": self.question.id,
                "registration_id": self.registration.id,
                "value_attachment_id": self.attachment.id,
            }
        )
        answer2 = self.env["event.registration.answer"].create(
            {
                "question_id": question2.id,
                "registration_id": self.registration.id,
                "value_attachment_id": attachment2.id,
            }
        )
        self.assertEqual(answer1.value_attachment_id, self.attachment)
        self.assertEqual(answer2.value_attachment_id, attachment2)

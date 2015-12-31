# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# © 2015 Grupo ESOC Ingeniería de Servicios, S.L.U. - Jairo Llopis

from openerp.tests.common import TransactionCase


class DurationsCase(TransactionCase):
    """Test some record operations."""
    def setUp(self):
        super(DurationsCase, self).setUp()
        self.course = self.env.ref("event_training.course_tmpl_odoo_mixed")

    def test_copy_duration_ids(self):
        """Copy course with durations."""
        # Copy the course
        new = self.course.copy()

        # Check if durations were copied
        self.assertEqual(len(self.course.duration_ids), 3)
        self.assertEqual(len(new.duration_ids), 3)
        for field in ("duration", "type_id"):
            field = "duration_ids.%s" % field
            self.assertEqual(
                set(self.course.mapped(field)),
                set(new.mapped(field)),
                "Field %s differs." % field)

    def test_unlink(self):
        """Unlink course with durations."""
        self.course.unlink()

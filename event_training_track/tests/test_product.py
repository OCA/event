# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# © 2015 Grupo ESOC Ingeniería de Servicios, S.L.U. - Jairo Llopis

from openerp.tests.common import TransactionCase


class ProductFillDurationsCase(TransactionCase):
    def setUp(self):
        super(ProductFillDurationsCase, self).setUp()

        self.course = self.env.ref("event_training.course_odoo_mixed")
        self.course_type_good = self.env.ref(
            "event_training.training_type_mixed")
        self.course_type_bad = self.env.ref(
            "event_training.training_type_online")
        self.duration_types_good = (
            self.course.event_type_id.expected_duration_type_ids)
        self.duration_types_bad = [d.copy() for d in self.duration_types_good]
        self.create_duration = self.env["event.training.duration"].create

        # Remove any found durations
        self.course.duration_ids.unlink()

    def tearDown(self):
        """All tests end checking that the fulfill was right."""
        self.course.action_fill_duration_ids()
        self.assertEqual(set(self.course.mapped("duration_ids.type_id.name")),
                         set(self.duration_types_good.mapped("name")))

        super(ProductFillDurationsCase, self).tearDown()

    def test_when_empty(self):
        """When course has no duration records at all."""
        pass

    def test_when_full_good(self):
        """Create good duration records for the course."""
        for duration_type in self.duration_types_good:
            self.course.duration_ids |= self.create_duration({
                "type_id": duration_type.id,
                "product_tmpl_id": self.course.product_tmpl_id.id,
            })

    def test_when_half_good(self):
        """Create only one good duration record for the course."""
        self.course.duration_ids |= self.create_duration({
            "type_id": self.duration_types_good[0].id,
            "product_tmpl_id": self.course.product_tmpl_id.id,
        })

    def test_when_full_bad(self):
        """Create bad duration records for the course."""
        for duration_type in self.duration_types_bad:
            self.course.duration_ids |= self.create_duration({
                "type_id": duration_type.id,
                "product_tmpl_id": self.course.product_tmpl_id.id,
            })

    def test_when_half_bad(self):
        """Create only one bad duration record for the course."""
        self.course.duration_ids |= self.create_duration({
            "type_id": self.duration_types_bad[0].id,
            "product_tmpl_id": self.course.product_tmpl_id.id,
        })

    def test_when_half_good_half_bad(self):
        """Create only one good and one bad duration record for the course."""
        self.course.duration_ids |= self.create_duration({
            "type_id": self.duration_types_good[0].id,
            "product_tmpl_id": self.course.product_tmpl_id.id,
        })
        self.course.duration_ids |= self.create_duration({
            "type_id": self.duration_types_bad[0].id,
            "product_tmpl_id": self.course.product_tmpl_id.id,
        })

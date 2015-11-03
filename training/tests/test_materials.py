# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# © 2015 Grupo ESOC Ingeniería de Servicios, S.L.U.

from .base import BaseCase


class MaterialsCase(BaseCase):
    def setUp(self):
        super(MaterialsCase, self).setUp()
        # Add good duration types
        self.action.material_ids |= self.materials

    def test_copy_training_action(self):
        """Copy training action with materials."""
        new = self.action.copy()
        self.assertEqual(new.material_ids, self.action.material_ids)

    def test_fill_materials(self):
        """Changing training action changes materials."""
        self.event.training_action_id = self.action
        self.event._fill_material_ids()
        self.assertEqual(self.event.material_ids, self.action.material_ids)

    def test_event_has_materials_not_fill_materials(self):
        """No materials changed because event already had one."""
        self.event.material_ids = self.material_1
        self.event.training_action_id = self.action
        self.event._fill_material_ids()
        self.assertEqual(self.event.material_ids, self.material_1)

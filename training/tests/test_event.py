# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# © 2015 Grupo ESOC Ingeniería de Servicios, S.L.U. - Jairo Llopis

from .base import BaseCase


class TrainingModeCase(BaseCase):
    def test_training_mode_true(self):
        """Training mode is ``True`` when read from training context."""
        self.assertTrue(
            self.event.with_context(training_mode=True).training_mode)
        self.assertTrue(
            self.event.with_context(training_mode=1).training_mode)
        self.assertTrue(
            self.event.with_context(training_mode="False").training_mode)

    def test_training_mode_false(self):
        """Training mode is ``False`` when read from training context."""
        self.assertFalse(self.event.training_mode)
        self.assertFalse(
            self.event.with_context(training_mode=0).training_mode)
        self.assertFalse(
            self.event.with_context(training_mode="").training_mode)
        self.assertFalse(
            self.event.with_context(training_mode=None).training_mode)
        self.assertFalse(
            self.event.with_context(training_mode=False).training_mode)

    def test_training_mode_contrary(self):
        """Training mode is opposite depending on context."""
        self.assertIs(
            self.event.training_mode,
            not self.event.with_context(training_mode=True).training_mode)
        self.assertIs(
            not self.event.training_mode,
            self.event.with_context(training_mode=True).training_mode)

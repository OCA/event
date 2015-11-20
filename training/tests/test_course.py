# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# © 2015 Grupo ESOC Ingeniería de Servicios, S.L.U. - Jairo Llopis

from .base import BaseCase


class CourseOperationsCase(BaseCase):
    """Test some record operations."""
    def setUp(self):
        super(CourseOperationsCase, self).setUp()
        # Add good duration types
        self.course.duration_ids |= self.create(
            "duration",
            {"type_id": self.duration_types_good[0].id,
             "course_id": self.course.id,
             "duration": 20.5})
        self.course.duration_ids |= self.create(
            "duration",
            {"type_id": self.duration_types_good[1].id,
             "course_id": self.course.id,
             "duration": 0.1})

    def test_copy_duration_ids(self):
        """Copy course with durations."""
        # Copy the course
        new = self.course.copy()

        # Check if durations were copied
        for field in ("duration", "type_id"):
            field = "duration_ids.%s" % field
            self.assertEqual(
                set(self.course.mapped(field)),
                set(new.mapped(field)),
                "Field %s differs." % field)

    def test_unlink(self):
        """Unlink course with durations."""
        self.course.unlink()


class CourseOnChangeBaseCase(object):
    """Common methods for this module."""
    def tearDown(self, *args, **kwargs):
        """All tests end checking that the fulfill was right."""
        with self.env.do_in_onchange():
            # Set the course's type
            self.course.type_id = self.course_type_good

            # This should be run automatically when on UI
            self.course._onchange_type_id_fulfill_expected_duration_types()

        # User presses *Save*
        # See http://stackoverflow.com/a/33255577/1468388
        self.course.write(self.course._convert_to_write(self.course._cache))

        # Check that it was fulfilled right
        self.assertEqual(set(self.course.mapped("duration_ids.type_id.name")),
                         set(self.duration_types_good.mapped("name")))

        super(CourseOnChangeBaseCase, self).tearDown(*args, **kwargs)


class CourseOnChangeTypeFulfillExpectedDurationTypesCase(
        CourseOnChangeBaseCase, BaseCase):
    """Test method _onchange_type_id_fulfill_expected_duration_types().

    That method of courses gets triggered when changing the course
    type, and is supposed to update the duration_ids field.
    """
    create_method = "new"

    def test_when_empty(self):
        """When course has no duration records at all."""
        pass

    def test_when_full_good(self):
        """Create good duration records for the course."""
        for duration_type in self.duration_types_good:
            self.course.duration_ids |= self.create(
                "duration",
                {"type_id": duration_type.id,
                 "course_id": self.course.id})

    def test_when_half_good(self):
        """Create only one good duration record for the course."""
        self.course.duration_ids |= self.create(
            "duration",
            {"type_id": self.duration_types_good[0].id,
             "course_id": self.course.id})

    def test_when_full_bad(self):
        """Create bad duration records for the course."""
        for duration_type in self.duration_types_bad:
            self.course.duration_ids |= self.create(
                "duration",
                {"type_id": duration_type.id,
                 "course_id": self.course.id})

    def test_when_half_bad(self):
        """Create only one bad duration record for the course."""
        self.course.duration_ids |= self.create(
            "duration",
            {"type_id": self.duration_types_bad[0].id,
             "course_id": self.course.id})

    def test_when_half_good_half_bad(self):
        """Create only one good and one bad duration record for the course."""
        self.course.duration_ids |= self.create(
            "duration",
            {"type_id": self.duration_types_good[0].id,
             "course_id": self.course.id})
        self.course.duration_ids |= self.create(
            "duration",
            {"type_id": self.duration_types_bad[0].id,
             "course_id": self.course.id})


class CourseMixOnChangeCase(CourseOnChangeBaseCase, BaseCase):
    """Problems when mixing onchange and real database writes."""
    def test_when_editing_and_replacing_twice(self):
        """Course had duration X, then X autoremoved and X autoadded again.

        This test can fail **because we are in on change** mode.

        The on change trigger deletes an existing duration, and then creates a
        new one with the same unique key, and thus fails to save.
        """
        # Course has one duration written in DB
        self.course.duration_ids |= self.create(
            "duration",
            {"type_id": self.duration_types_good[0].id,
             "course_id": self.course.id,
             "duration": 20})

        self.create_method = "new"
        self.course = self.course.with_context(active_model="training.course",
                                               active_id=self.course.id)
        with self.env.do_in_onchange():
            # The user changes the course type
            self.course.type_id = self.course_type_bad

            # The duration gets deleted
            self.course._onchange_type_id_fulfill_expected_duration_types()

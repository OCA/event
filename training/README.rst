.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :alt: License: AGPL-3

========
Training
========

This module extends the functionality of events to support training sessions
and allow you to manage courses, training groups, training hour types, training
products, etc.

Usage
=====

To use this module, you need to:

* Have *Training / User* or *Training / Manager* permissions.
* Go to the new menu item called *Training*.

The *Training* menu
-------------------

There you can find the following menus, depending on your permissions:

Courses
~~~~~~~

Courses define the structure of a course.

They have a name, such as *Prevention of occupational hazards, Office
software, Odoo user basic training*, etc.

They are classified with course types. Depending on it, they define how many
hours of each type are expected to be teached.

You can define the training products that should be delivered to students to
accomplish the course.

You can specify the grade settings: which is the minimal and maximum grade
possible for this course, and which grade students need to reach to pass the
course.

Also you can define the contents of this course. They will appear in the back
side of the diploma if available. You have a field called *Append template*
that will help you to fulfill the contents in some complex layouts.

Course Types
~~~~~~~~~~~~

Depending on the type of hours that a course is expected to have, the
course has that course type. For instance:

- A training of type *on-site* may expect only *on-site* hours.
- A training of type *online* may expect only *online* hours.
- A training of type *remote* may expect only *remote* hours.
- A training of type *mixed* may expect *on-site*, *online* and *remote* hours.

You can define course types and the expected type of hours in this menu.

Hour Types
~~~~~~~~~~

Hours in each course are separated by type. Types of hours can be *On
site, Online, Remote* and anything you decide.

For instance, a course of *online* type cannot have *on-site* hours.

Groups
~~~~~~

A training group is a course that belongs to a course. Most of the
time you will likely use this menu.

They have all details about it: students, start and end dates, products
delivered, etc.

Technically speaking, groups are just events that are assigned to a training
course. Therefore, you can use also the events view to manage training groups,
but the *Training* menu is a more consistent place to manage training groups,
and when using that view you will be required to set a course.

Registrations (inside Groups form view)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

These are similar to event registrations too, but with some additions:

- Set a grade for the student and see if it is passing the course
  automatically (it compares with the passing grade in the course).
- Quick access to the course.
- Check if products were delivered to the registrant.

There are also these reports here:

- *Diploma / Certificate*. Printed diploma to be delivered if the attendee has
  completed and passed the course. Otherwise a certificate of assistance will
  be delivered
- *Diploma / Certificate Delivery Receipt*, to prove the diploma or
  certificate was delivered to the attendee.
- *Training Products Delivery Receipt*, to prove the products were
  delivered to the attendee.

  You might want to check the box *Products delivered* in the registration
  form when any attendee signs this report.

Partner views
-------------

If you access a partner view from any module, you will be able to print a new
report called *Training Attendance Certificate*. It will display the status of
all registrations made in the name of this partner (and/or its contacts if it
is a company).

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/199/8.0

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/event/issues>`_. In
case of trouble, please check there if your issue has already been reported. If
you spotted it first, help us smashing it by providing a detailed and welcomed
feedback `here
<https://github.com/OCA/event/issues/new?body=module:%20training%0Aversion:%208.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Credits
=======

Contributors
------------

* Jairo Llopis <j.llopis@grupoesoc.es>.

Maintainer
----------

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit http://odoo-community.org.

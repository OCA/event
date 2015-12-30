.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :alt: License: AGPL-3

========
Training
========

This module extends events to support training events and courses.

Courses are products that:

- Are marked as *Is event*.
- Have an event type marked as *Is training*.

Documentation about event products can be found in module ``event_product``.

Usage
=====

To use this module, you need to have at least *Event / Training User*
permissions.

Creating a training event type
------------------------------

#. Go to *Marketing > Configuration > Events > Types of Events > Create*.
#. Set a name.
#. Enable *Is training*.

Defining a course
-----------------

Remember that your courses are products, and they share the same catalog and
features.

#. Go to *Sales > Products > Products > Create*.
#. Set a name, such as *Prevention of occupational hazards, Office
   software, Odoo user basic training*, etc.
#. Enable *Is an event*.
#. Choose the event type you just created in *Event > Type of Event*.
#. Set a *Minimum grade*. Students will not be able to get grade below this.
#. Set a *Maximum grade*. Students will not be able to get grade above this.
#. Set a *Passing grade*. Students will pass if their grade is above this.
#. Set the *Contents* of the course.
    - These contents will appear in the back side of the diploma if available.
    - Use *Contents layout* to fulfill the contents in some complex layouts.

Creating an event that belongs to that course
---------------------------------------------

These are known as training events, or training groups.

#. Go to *Marketing > Events > Events > Create*.
#. Set a name, start and end dates.
#. Choose the same *Type of Event* that you created previously.
#. Choose the *Product* that you created previously.

Setting grades for students
---------------------------

Only students that have attended the course have grade.

#. Edit the event you just created.
#. Press the *# Registrations* button.
#. Press *Create*.
#. Choose a partner for the student, or add name and other data.
#. Press *Confirm*.
#. Press *Attended*.
#. Set a *Grade*.
    - *Passing* will be true if it is at least the passing grade you chose in
      the event type.

Printing reports
----------------

Reports for event registrations:

- *Diploma / Certificate*. Printed diploma to be delivered if the attendee has
  completed and passed the course. Otherwise it becomes a certificate of
  assistance.
- *Diploma / Certificate Delivery Receipt*, to prove the diploma or certificate
  was delivered to the attendee.

Reports for partners:

- *Training Attendance Certificate*. Display the status of all registrations
  made in the name of this partner (and/or its contacts if it is a company).

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/199/8.0

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/event/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smashing it by providing a detailed and welcomed `feedback
<https://github.com/OCA/
event/issues/new?body=module:%20
training_event%0Aversion:%20
8.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Credits
=======

Images
------

* Font Awesome: `Icon <http://fontawesome.io/icon/graduation-cap/>`_.

Contributors
------------

* Jairo Llopis <yajo.sk8@gmail.com>

Maintainer
----------

.. image:: https://odoo-community.org/logo.png
  :alt: Odoo Community Association
  :target: https://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit https://odoo-community.org.

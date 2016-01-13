.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

========================
Training track generator
========================

This combines the functionality of the ``event_training_track`` and
``event_track_generate`` modules and adds the ability to set the training hour
type when batch generating event tracks in training groups.

Installation
============

This module will get installed automatically if ``event_training_track`` when
``event_track_generate`` modules are installed.

Usage
=====

See usage instructions for ``event_track_generate``. This module just adds
these special fields required to use it in combination with ``training``:

- *Training duration type* to assign to tracks.
- *Stop when reaching expected durations*, which will stop track generations
  if you reach what was expected. Remember than regardless of this choice, the
  generator will stop when reaching the end date of your event.

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/199/8.0

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/event/issues>`_. In
case of trouble, please check there if your issue has already been reported. If
you spotted it first, help us smashing it by providing a detailed and welcomed
feedback `here
<https://github.com/OCA/event/issues/new?body=module:%20event_training_track_generate%0Aversion:%208.0.1.0.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Credits
=======

Images
------

* FontAwesome: `Icon <http://fontawesome.io/icon/graduation-cap/>`_.

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

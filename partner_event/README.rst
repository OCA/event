.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :alt: License: AGPL-3

=======================
Link partner and events
=======================

This module links partners with the events they are registered through a
smart button.

It also includes:

* Search partners by their event registrations.
* Search partners by number of events registered.
* Search partners by number of events attended.
* Partner column is visible on registration one2many list inside the event.
* Action in partner tree view 'More' button, to register several partners
  to an event

Configuration
=============

There is a new option in event form view, "Create Partners in registration". If
this option is checked, when you add registrations to this event, partners will
be created automatically with name, email and phone fields.

If partner already exists and user only fills email, name and phone fields will
be filled with partner's data.

Usage
=====

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/199/8.0


Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/event/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and welcomed feedback
`here <https://github.com/OCA/event/issues/new?body=module:%20partner_event%0Aversion:%208.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Known Issues / Roadmap
======================

* Remove some TODOs if https://github.com/odoo/odoo/pull/12997 is merged.

Credits
=======

Contributors
------------

* Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>
* Javier Iniesta <javieria@antiun.com>
* Antonio Espinosa <antonioea@antiun.com>
* Jairo Llopis <jairo.llopis@tecnativa.com>

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

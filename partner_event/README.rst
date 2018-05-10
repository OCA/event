.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.png
    :alt: License: AGPL-3

=======================
Link partner and events
=======================

This module links partners with the events they are registered through a
smart button.

It also includes:

* Search partners by their event attendees.
* Search partners by number of events attendees.
* Search partners by number of events attended.
* Partner column is visible on registration one2many list inside the event.
* Action in partner tree view 'More' button, to register several partners
  to an event
* Restricts partner deletion when event attendees are linked to it.

Configuration
=============

There is a new option in event form view, "Create Partners in registration". If
this option is checked, when you add registrations to this event, partners will
be created automatically with name, email and phone fields.

If partner already exists and user only fills email, name and phone fields will
be filled with partner's data.

The event registration values email, name and phone will be changed if the
related partner values are changed and the event end date hasn't passed yet.

Usage
=====

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/199/11.0

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/event/issues>`_.
In case of trouble, please check there if your issue has already been
reported. If you spotted it first, help us smashing it by providing a detailed
and welcomed feedback.

Known Issues / Roadmap
======================

* In registration contact field has no onchange check so changing the partner
  is not going to change any info on the registration.

Credits
=======

Images
------

* Odoo Community Association: `Icon <https://github.com/OCA/maintainer-tools/blob/master/template/module/static/description/icon.svg>`_.

Contributors
------------

* Pedro M. Baeza <pedro.baeza@tecnativa.com>
* Javier Iniesta <javieria@antiun.com>
* Antonio Espinosa <antonioea@tecnativa.com>
* Jairo Llopis <jairo.llopis@tecnativa.com>
* Vicent Cubells <vicent.cubells@tecnativa.com>
* David Vidal <david.vidal@tecnativa.com>
* Rafael Blasco <rafael.blasco@tecnativa.com>

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

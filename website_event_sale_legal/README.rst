.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=====================
Legal terms per event
=====================

This module was written to extend the functionality of online event ticket
sales to support setting legal terms that attendees will accept when ordering
their registrations.

Legal terms can be set by event and/or by ticket.

Installation
============

To install this module, you need to:

* Install the repository `OCA/e-commerce <https://github.com/OCA/e-commerce>`_.

Usage
=====

Please review usage instructions for module *website_sale_product_legal*.

Also, to use this module, you need to:

* Go to *Marketing > Events > Events*.
* Create or edit one.
* Go to *Event Details*.
* Set event's legal terms there. They will apply to all ticket types.
* Go to *Ticket Types*.
* Create or edit a ticket type.
* Set ticket's legal terms there.
* Publish the event.
* Log out.
* Visit your public event page.
* You will see links to legal terms for ticket types, and legal advices to make
  you accept those implicitly to buy.

To set a legal term for many events at once, you need to:

* Go to *Marketing > Configuration > Events > Legal terms*.
* Create or edit a legal term.
* Choose the events it applies to in the *Events* table.

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
website_event_sale_legal%0Aversion:%20
8.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Credits
=======

Images
------

* Antiun Ingeniería, S.L.: `Icon <https://github.com/Antiun/antiun-odoo-addons/commit/3160fb96636c890f06b39c028cd34dcae3b0896e#diff-921de683b9f637743b52c770525098db>`_.

Contributors
------------

* Rafael Blasco <rafaelbn@antiun.com>
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

To contribute to this module, please visit http://odoo-community.org.

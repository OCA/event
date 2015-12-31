.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==============
Event Products
==============

This module extends the functionality of events and products allowing their
combination and the organization of a catalog of events.

Those events in your catalog can have variants, and any event can be linked to
any product as long as:

* The product's *Is an event* checkbox is enabled.
* The product's event type is empty, or matches the event's.

Examples:

* Wedding.
    * Variants:
        * Up to 50 attendees.
        * Up to 100 attendees.
        * In beach.
        * In countryfield.
* Congress.
    * Variants:
        * Up to 50 attendees.
        * Up to 100 attendees.
* Opening.
    * Variants:
        * 1 day.
        * 2 days.
        * 3 days.

Usage
=====

To create your *event products*, you need to:

#. Go to *Sales > Products > Products > Create*.
#. Give it a name, such as *Wedding*.
#. Enable *Is an event*.
#. Choose event type in *Event > Type of Event* (or leave blank for
   events of any type).
#. Press *Save*.

To create variants for that, you need to:

#. Edit previous product.
#. Go to *Variants* tab.
#. Press *Add an Item*.
#. Add your attribute and values as usual.

To link an event to any of those variants, you need to:

#. Go to *Marketing > Events > Events > Create*.
#. Set name, start and end dates.
#. Choose the same *Type of Event* as when creating the product (unless you
   left it blank, in which case you do not need this).
#. Choose one of your variants in *Product*.

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/199/8.0

Known issues / Roadmap
======================

* Installing this module will install sale too. If you do not intend to sell
  events, but just handle internal ones, this can be annoying since the sale
  module requires complex configuration with accounting and external
  dependencies.

  However, this happens because this module needs the ``event_type_id`` field
  in products, which is added by the *event_sale* module, which installs
  *sale*; so unless Odoo divides that module in smaller parts with smaller
  dependencies, the only workaround is to give permissions to use *sale* to
  nobody.
* Support creating a sales order from the event.
* Support creating an event when confirming an event product sales order.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/event/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smashing it by providing a detailed and welcomed `feedback
<https://github.com/OCA/
event/issues/new?body=module:%20
event_product%0Aversion:%20
8.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Credits
=======

Images
------

* Odoo Community Association: `Icon <https://github.com/OCA/maintainer-tools/blob/master/template/module/static/description/icon.svg>`_.

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

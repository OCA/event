.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==========================
Product Delivery in Events
==========================

Sometimes you want to give some products to your event's attendees. For
example: a pen, a notebook, a book, etc.

This module extends the functionality of events to support setting products to
deliver to event attendees and allow you to know if they have already been
delivered to them.

.. warning::
    Please make no confusion between *event products* and *products to
    deliver in events*:

    * **Event products** are created in the ``event_product`` addon, and
      define an event as a product (wedding, fair, etc.), to have a catalog
      of them.
    * **Products Delivery in Events** are created in this addon, and define
      the products (goodies, leaflets, etc.) that you will deliver to event
      attendees.

      They can be defined in the *event product*, in the event directly, or in
      both.

Usage
=====

To set products to deliver in an event product (see ``event_product`` module),
you need to:

#. Go to *Sales > Products > Product variants > Create*.
#. Set a name.
#. Enable *Is an event*.
#. Open the new tab called *Event*.
#. Set products to deliver there.

To set products to deliver in an event, you need to:

#. Go to *Marketing > Events > Events > Create*.
#. Set a name, start and end dates..
#. Open the *Products to Deliver* tab.
#. Do you want to get those products from the *event product* you just created?
    - Yes.
        #. Set that product in the *Product* field.
        #. Press *Load from linked product*.
    - No.
        #. Set products to deliver directly on the list.

To mark those products as delivered to everyone, you need to:

#. Press the *Mark as delivered to all attendees* button there in the *Products
   to Deliver* tab.

To mark those products as delivered to only one attendee, you need to:

#. Press the button that indicates the registration quantity, at the top of the
   event form.
#. Choose one registration.
#. Check the *Products delivered* box.

To print a delivery receipt for those products, you need to:

#. Press the button that indicates the registration quantity, at the top of the
   event form.
#. Choose all the registrations you want.
#. Press *Print > Products Delivery Receipt*.

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/199/8.0

Known issues / Roadmap
======================

* Please read known issues section of ``event_product``'s README about
  installation of the ``sale`` addon.
* Product deliveries currently do not create the corresponding stock moves.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/event/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smashing it by providing a detailed and welcomed `feedback
<https://github.com/OCA/
event/issues/new?body=module:%20
event_product_logistics%0Aversion:%20
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

.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==============
Event Sale Pro
==============

This module was written to extend the functionality of ``event_sale`` to
support creating quotations from the event itself and allow you to navigate
quickly between the event and its sale process.

Installation
============

If you install this module after using the main ``event_sale`` module for
awhile, at installation the module will try to link any registration with its
corresponding sales orders if available, but it will not be able to link them
to the exact sales order line. It will start doing it from the moment you
install it onwards.

Usage
=====

This module mainly modifies event registrations. To see the changes go to
*Marketing > Events* and choose one, and then click the *Registrations* button.
Now read below.

Permissions
-----------

To use this module, you need to:

* Have permissions for events.
* Have permissions for sales.

New fields
----------

* In registrations form, you have a new field called *Invoiced partner*, that
  will be used as client in the quotation if set. If you do not set it, the
  *Partner* field will be used. It is useful when:

  * A registration belongs to a partner but is paid by another one.
  * No database partner is associated with the event assistant and you do not
    want to create it.

* In the registrations form and list views, you have another new field:
  *Origin*. When the registration is automatically linked to any sale order or
  sale order line, you will be able to click on this field to get there
  instantly.

  If you want to link that registration to any other *Origin*, you can do it
  manually too.

New wizard
----------

From the registrations form and list views, you can now select one or several
registrations, and click *Generate quotations* from the *More* menu.

That will open a wizard that will help you to generate quotations automatically
for the registrations that have none.

You can opt to create a quotation for each commercial entity, which will merge
registrations of persons that belong to the same company into the same
quotation.

Always remember that the *Partner* field in registrations will be ignored if
there is a *Invoiced partner* set.

After running the wizard, you will be able to visit the exact quotation line
that is linked to each registration, and visit the full quotation from there.

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/199/8.0

For further information, please visit:

* https://www.odoo.com/forum/help-1

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/event/issues>`_. In
case of trouble, please check there if your issue has already been reported. If
you spotted it first, help us smashing it by providing a detailed and welcomed
feedback `here
<https://github.com/OCA/event/issues/new?body=module:%20event_sale_pro%0Aversion:%208.0.1.0.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.


Credits
=======

Contributors
------------

* Jairo Llopis <j.llopis@grupoesoc.es>

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

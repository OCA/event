.. image:: https://img.shields.io/badge/license-LGPL--3-blue.svg
   :target: https://www.gnu.org/licenses/lgpl
   :alt: License: LGPL-3

============================
Event Track Location Overlap
============================

This module extends the functionality of event tracks to allow users to set
some track locations as non-overlappable. Thus, an error will happen if
somebody tries to save more than one track at the same time and location.

Configuration
=============

To configure this module, you need to:

#. Go to *Events > Configuration > Locations*.
#. By default, no location is overlappable, but here you can enable
   overlapping for some of them if you want.

Usage
=====

To use this module, you need to:

#. Go to *Events > Events*.
#. Enter some event with tracks.
#. Create some tracks for it.
#. If more than one confirmed track overlaps with other in the same location,
   and the location is not overlappable, you will not be able to save it.

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/199/9.0

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/event/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smash it by providing detailed and welcomed feedback.

Credits
=======

Images
------

* Odoo Community Association: `Icon <https://github.com/OCA/maintainer-tools/blob/master/template/module/static/description/icon.svg>`_.

Contributors
------------

* `Tecnativa <https://www.tecnativa.com>`_:

  * Jairo Llopis <jairo.llopis@tecnativa.com>

Do not contact contributors directly about support or help with technical issues.

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

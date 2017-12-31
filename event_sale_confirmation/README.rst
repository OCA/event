.. image:: https://img.shields.io/badge/license-AGPL--3-blue.png
   :target: https://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3

===========================================
Restricted access to confirm unpaid tickets
===========================================

Module hides ``[Confirm]`` button when ticket is not free and user doesn't have access level ``Events: Manager``.

Usage
=====

To use this module, you need to:

#. Switch to user with access level ``Events: User``
#. Open unpaid non-free ticket (record at ``event.registration`` model)
#. Result: you cannot see ``[Confirm]`` button.

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/199/10.0

Known issues / Roadmap
======================

* There is no protection on orm level yet. Malicious user still can use rpc call to confirm unpaid ticket

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

* Odoo Community Association: `Icon <https://odoo-community.org/logo.png>`_.

Contributors
------------

* `Ivan Yelizariev <https://it-projects.info/team/yelizariev>`__

Do not contact contributors directly about support or help with technical issues.

Funders
-------

The development of this module has been financially supported by:

* `Geoparadise, Inc <https://www.tribalgathering.com/>`__

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

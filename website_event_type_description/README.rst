.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=================================
Event Type Description in Website
=================================

This module extends the functionality of events website to support a custom
description for each event type that will be displayed only when events of that
type are filtered, below the common description for the Events page.

Usage
=====

To edit your event type description from the frontend, you need to:

#. Go to `your events page </event>`_.
#. Make sure you *Filter by Category* is enabled in the *Customize* menu.
#. Choose a event type from the filters.
#. Edit the page.
#. You will see a new editable area at the top (just below the one you already
   had) that only will be shown when the page is filtered for this type of
   event.
#. Fill that area with any blocks you want.
#. Save.

To do it from the backend, you need to:

#. Go to *Marketing > Configuration > Events > Types of Events*.
#. Choose a type.
#. Change its description.

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/199/8.0

Known issues / Roadmap
======================

* The best for SEO would be to have a dedicated controller for event types,
  with a friendly slug.
* In such case, the ``event.type`` model should inherit from
  ``website.seo.metadata`` mixin to have access to all SEO tools.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/event/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smashing it by providing a detailed and welcomed `feedback
<https://github.com/OCA/
event/issues/new?body=module:%20
website_event_type_description%0Aversion:%20
8.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Credits
=======

Images
------

* Odoo Community Association: `Icon <https://github.com/OCA/maintainer-tools/blob/master/template/module/static/description/icon.svg>`_.

Contributors
------------

* Rafael Blasco <rafabn@antiun.com>
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

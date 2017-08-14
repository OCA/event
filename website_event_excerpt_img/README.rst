.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=========================
Excerpt + Image in Events
=========================

This module extends the functionality of website events to support having a
more attractive layout that automatically displays an excerpt of each one, a
"Read more" button, and an image.

It also adds a event priority control in the backend that will display the
event at the top and in a bigger shape in the website.

Installation
============

To install this module, you need to:

#. Install `OCA/server-tools <https://github.com/OCA/server-tools>`_.

Configuration
=============

To configure this module, you need to:

#. Log in.
#. Go to `your website events page </event>`_.
#. Open the *Customize* menu.
#. *Images and Description* should be checked, and you should see events with
   an image and description in the layout.

.. warning::
    Normal (not highlighted) events will show up a bit clunky if you do not
    disable the *Filters* view from the *Customize* menu.

    You can either highlight all events, or disable that view.

    If you still need filters, see module ``website_event_filter_selector``
    found in this same repo.

Usage
=====

To use this module, you need to:

#. Go to the events page in your website. They have image and description now.

You will notice that short description is the excerpt of the first 80
characters of the event's long description. If you want to set a manual
description, you need to:

- From the frontend:
    #. Click in that event.
    #. Use the *Promote > Optimize SEO* tool to set a meta description.
- From the backend:
    #. Go to *Events > Events*.
    #. Choose one.
    #. Go to *Featured content*.
    #. Use the *Website meta description* field for the same purpose.

If you want to change the image, you need to:

#. Edit the event page.
#. There, the first image appearing will be the one chosen. Beware, background
   images count!

If you want to set an event as important:

#. Go to the event's form in backend.
#. Publish it.
#. Go to the *Featured content* tab.
#. Add a star in *Priority* to display the event in a full row on website.
#. Remove the star to display it in half a row.

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/199/10.0

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

* Rafael Blasco <rafael.blasco@tecnativa.com>
* Jairo Llopis <jairo.llopis@tecnativa.com>
* David Vidal <david.vidal@tecnativa.com>

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

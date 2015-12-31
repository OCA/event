.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :alt: License: AGPL-3

===============
Training Tracks
===============

This module combines the power of modules ``event_training`` and
``website_event_track``.

You can define the expected hour types per training event type. Examples:

- Online training expects online hours.
- On-site training expects on-site hours.
- Mixed training expects online and on-site hours.

.. note::

    *Hour types* are often called *Duration types*, because durations can
    theoretically be minutes, although that would be a very quick training...

Any of those hour types can be marked to monitor attendance. In the example,
you should only need it for on-site hours.

You can define the expected duration of each hour type per event product, and
you will be able to check if they are effectively fulfilled.

.. note::

    If you want to read more about event products, see README of
    ``event_product`` module.

Event tracks are assigned a training duration type, informing the user whether
the training group has fulfilled all the expected hours for it, and you can
know which attendees attended each track, if attendance monitoring is needed.

Installation
============

This module will be automatically installed when you have installed the modules
``event_training`` and ``website_event_track``.

Usage
=====

Please read instructions for ``event_training`` and ``event_product`` before
starting with these.

To set the expected duration types for an event type:

#. Go to *Marketing > Configuration > Events > Types of Events > Create*.
#. Enable *Is training*.
#. Choose some *Expected duration types*. The ones marked with *Monitor
   attendance* will be expected to fulfill that amount of hours in the event
   tracks.

To set the expected amount of each of those hours for each event product:

#. Go to *Sales > Products > Products > Create*.
#. Enable *Is an event*.
#. Go to *Event*.
#. Choose the *Type of Event* you created before.
#. Fill the *Expected durations* table.

   .. note::

       It gets autofilled when you select a training event type for the first
       time. Further times you have the *Load from event type* button to do it.

To create an event with that product and type, and create tracks with that
type:

#. Create an event.
#. Set a training *Type* and *Product* for it.
#. Create a track in it.
#. Use the new field in the track to set an hour type if you want.

To compare the expected durations with the actual ones:

#. Go to *Marketing > Events > Events* and choose the event you created.
#. Go to *Tracks > Compare tracks with expected hours*.

   There you will find a comparison between what was expected for this event
   and what is being actually fulfilled. Red lines indicate that you are not
   doing what was expected.

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/199/8.0

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/event/issues>`_. In
case of trouble, please check there if your issue has already been reported. If
you spotted it first, help us smashing it by providing a detailed and welcomed
feedback `here
<https://github.com/OCA/event/issues/new?body=module:%20event_training_track%0Aversion:%208.0.1.1.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Credits
=======

Contributors
------------

* Jairo Llopis <j.llopis@grupoesoc.es>.

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

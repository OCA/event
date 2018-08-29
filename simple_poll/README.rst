.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3

===============================================
Simple Poll
===============================================

This module makes it possible to create simple inquiries (polls) and
distribute them using a custom link. The participants can then select
an option/s and submit their answers. The results of the inquiry are nicely
summarised in the link view.

This work is part of a master thesis written by Nikolina Todorova.
The master thesis contains further information, screenshots and the conceptual
background and can be downloaded here https://www.initos.com/forschung/publikationen/year/2018/

Usage
=====

To create a poll and distribute it, follow the steps:

* Go ot "Polls/Polls" menu
* Press the "Create" button
* Fill "Title", which will be your inquire question
* Choose one of the options
  ** "Simple Text Question" - to fill option with arbitrary text
  ** "Choose Date Question" - to fill options using date format
  ** "Choose Date Time Question" - to fill options using date and time format
* Fill an "End Date" for your event.
  This field will be used for the creation of automatic reminders ("Mail Schedulers" Tab)
* In the "Answer Options" Tab, add as many options as needed using "Add an item"
* In the "Invite Participants" Tab fill the people who will take part.
  Using "Group Name", we can invite a predefined group.
  Using "Name", we can add participants one by one.
  Note that the participant should have defined email address.
* In the "Mail Schedulers" Tab, we have one automatically created reminder,
  which will be send 2 days before the "End Date".
  If needed one can add new reminders or change the existing one.
* One can check the "Yes/No/Maybe Poll" to add a "maybe" option to the poll,
  otherwise the participant will be able to select an option using a checkbox.
* Use "Save" button to save the poll
* You will see a button "Send by Email". Press the button to send an invitation mail to the participants
  defined in the "Invite Participants" Tab.
* The results from the poll can be seen using the link in the "Public link" field.

To create a poll email group follow the steps:
* Go ot "Polls/Poll Email Groups" menu
* Press the "Create" button
* Fill "Group Name"
* Fill "Group Participants"
* Save group

Known issues / Roadmap
======================

* The website dependency can be removed when migrated to v11.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/event/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smash it by providing detailed and welcomed feedback.

Credits
=======

Contributors
------------

* Foram Shah <foram.shah@initos.com>
* Dhara Solanki <dhara.solanki@initos.com>

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

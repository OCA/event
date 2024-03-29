=============
Event project
=============

.. 
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   !! This file is generated by oca-gen-addon-readme !!
   !! changes will be overwritten.                   !!
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   !! source digest: sha256:78a585a6bb50de57d652a3f6000c52df9d110cbeb604ab35ccb08adf3ee55853
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

.. |badge1| image:: https://img.shields.io/badge/maturity-Beta-yellow.png
    :target: https://odoo-community.org/page/development-status
    :alt: Beta
.. |badge2| image:: https://img.shields.io/badge/licence-AGPL--3-blue.png
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3
.. |badge3| image:: https://img.shields.io/badge/github-OCA%2Fevent-lightgray.png?logo=github
    :target: https://github.com/OCA/event/tree/14.0/event_project
    :alt: OCA/event
.. |badge4| image:: https://img.shields.io/badge/weblate-Translate%20me-F47D42.png
    :target: https://translation.odoo-community.org/projects/event-14-0/event-14-0-event_project
    :alt: Translate me on Weblate
.. |badge5| image:: https://img.shields.io/badge/runboat-Try%20me-875A7B.png
    :target: https://runboat.odoo-community.org/builds?repo=OCA/event&target_branch=14.0
    :alt: Try me on Runboat

|badge1| |badge2| |badge3| |badge4| |badge5|

This module allows you to assign a project to an event. This project will
inherit its event's name an its due date will be set as the event's begining
date.

Change the event's begining date or its name so the project's due date and name
will be changed. And all the project pending tasks will be retro-planned
according to the new date.

**Table of contents**

.. contents::
   :local:

Usage
=====

To use this module, you need to:

#. Create a project that will be a template project for events.
#. Go to an event or create a brand new one and assign the previous template
   project.
#. After saving, the event will be related to a copy of the selected template
   project and the new copy project will inherit the name of the event and will
   fit its end date to the begging of the event.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/event/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us to smash it by providing a detailed and welcomed
`feedback <https://github.com/OCA/event/issues/new?body=module:%20event_project%0Aversion:%2014.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Do not contact contributors directly about support or help with technical issues.

Credits
=======

Authors
~~~~~~~

* Tecnativa

Contributors
~~~~~~~~~~~~

* Endika Iglesias <endikaig@antiun.com>
* Javier Iniesta <javieria@antiun.com>
* `Tecnativa <https://www.tecnativa.com>`_:

  * Pedro M. Baeza
  * Rafael Blasco
  * Antonio Espinosa
  * David Vidal
  * Ernesto Tejeda

Maintainers
~~~~~~~~~~~

This module is maintained by the OCA.

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

This module is part of the `OCA/event <https://github.com/OCA/event/tree/14.0/event_project>`_ project on GitHub.

You are welcome to contribute. To learn how please visit https://odoo-community.org/page/Contribute.

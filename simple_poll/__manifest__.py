# -*- coding: utf-8 -*-
# © initOS GmbH 2017
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Simple Poll",
    "summary": "Create polls, collect answers, show results.",
    "description": """
Create simple polls
==================================================

Add new Poll main menu.
From there one can create simple polls from the following types:
- simple text
- date
- datetime
    """,
    "version": "10.0.1.0.0",
    "website": "https://github.com/OCA/event",
    "author": "Nikolina Todorova <nikolina.todorova@initos.com>, "
              "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "mail",
        "website"
    ],
    "data": [
        "views/poll_question.xml",
        "views/poll_webpage.xml",
        "data/mail_template.xml",
        "data/ir_cron.xml",
        "data/website_templates.xml"
    ],
}

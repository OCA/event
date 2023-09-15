This module allows you to configure opportunity stages to enable some automations.

To advance automatically to the next stage when the opportunity is invited to view an event category on the website:

#. Go to *CRM > Sales > My pipeline*.

#. Hover over one stage name and click on its cogs icon.

#. Choose *Edit Stage*.

#. Enable *Invite automatically to website event category* if you want that
   opportunities in that stage, which are related to an event category, get
   periodically checked to see if there's a new event published in your website,
   belonging to that category, and, if so, invited to check it out.

#. Enable *Advance stage automatically when inviting to website event category*
   if you want that, when one of the opportunities in that stage is invited to
   check out events published on your website, it advances automatically to the
   next stage.

Important: If you don't want to invite automatically on loop, make sure to
enable both options if you enable the 1st one, and make sure the next stage is
not enabled to autonotify.

To configure the frequency of automated notifications:

#. Go to *Settings > Technical > Automation > Scheduled Actions >
   Notify all opportunities related to event categories*.

#. Edit *Execute Every*.

Important: That only schedules mails, but they will be sent later when the
*Mail: Email Queue Manager* automated action is triggered. You can configure it
the same way.

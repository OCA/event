You can use cron arguments to modify three options in this position
(days, near_events, template_id):

* *days*: Change days to limit events search, 7 as default.
* *draft_events*: This is for including draft events also.
* *near_events*: Select an option to include events which begin date is between
  today and limit days, False as default.
* *template_id*: You can select and id template to render as third parameter,
  None by default, so email is rendered with the template installed by
  the module.
* partner_ids: By default, the event is notified to the event responsible, but
  you can choose who to notify indicating in this parameter a list of the IDs.

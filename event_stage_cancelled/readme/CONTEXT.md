Up to v14, events had an state field instead of configurable stages. A lost feature
with that change was the concept of a cancelled event and with it the logic associated
to it: when we cancelled an event, its registrations were cancelled along with it.

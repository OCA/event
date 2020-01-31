Move ticket relation to the tracks allowing to
manage event subscriptions by tracks.

The typical use case are:

* you have an event with multiple workshops and you have enough space
  but the size of the workshops needs to be limited to be managable

* you have different prices per each track

Note that default relations are preserved by proxying them over the Track model,
so those apps which are based on the default behaviour will work without issues.

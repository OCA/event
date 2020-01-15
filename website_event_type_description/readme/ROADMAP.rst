* The best for SEO would be to have a dedicated controller for event types,
  with a friendly slug.
* In such case, the ``event.type`` model should inherit from
  ``website.seo.metadata`` mixin to have access to all SEO tools.
* It's not obvious that there is an editable area on event types website.

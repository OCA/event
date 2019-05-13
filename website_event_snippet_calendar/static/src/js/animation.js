/* Copyright 2018 Tecnativa - Jairo Llopis
   Copyright 2018 Tecnativa - Alexandre Díaz
 * License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl). */

odoo.define('website_event_snippet_calendar.animation', function (require) {
    "use strict";

    var animation = require('website.content.snippets.animation');
    var core = require("web.core");
    var time = require("web.time");
    var ajax = require("web.ajax");


    var DATE_FORMAT = time.strftime_to_moment_format("%Y-%m-%d");
    var DATETIME_FORMAT = time.strftime_to_moment_format(
        "%Y-%m-%d %H:%M:%S");
    // HACK https://github.com/tempusdominus/bootstrap-3/issues/73
    var INVERSE_FORMAT = "L";

    var CalendarList = animation.Class.extend({
        selector: ".s_event_calendar_list",
        xmlDependencies: [
            "/website_event_snippet_calendar/static/src/xml/snippets.xml",
        ],

        init: function () {
            this.datepicker_options = {
                inline: true,
                minDate: moment().subtract(100, "years"),
                maxDate: moment().add(100, "years"),
                icons: {
                    previous: "fa fa-chevron-left",
                    next: "fa fa-chevron-right",
                },
                format: DATE_FORMAT,
                useCurrent: false,
                locale: moment.locale(),
            };
            return this._super.apply(this, arguments);
        },

        start: function (editable_mode) {
            this._super.apply(this, arguments);

            if (editable_mode) {
                return;
            }
            this._dates = {
                min: null,
                max: null,
                matches: [],
            };

            this.$calendar = this.$target.find('.s_event_calendar')
                .on("change.datetimepicker", $.proxy(this, "day_selected"))
                .on("update.datetimepicker", $.proxy(this, "calendar_moved"));
            this.$list = this.$target.find(".s_event_list");
            this.default_amount = Number(this.$(".js_amount").html()) || 4;
            this.date_format = this.$list.data("dateFormat") || "LLL";
            // Get initial events to render the list
            this.load_events(null, this.default_amount)
                .done($.proxy(this, "render_list"));
            // Preload dates and render the calendar
            this.preload_dates(moment())
                .done($.proxy(this, "render_calendar"));
        },

        day_selected: function (event) {
            this.load_events(event.date.format(DATE_FORMAT))
                .done($.proxy(this, "render_list"));
        },

        calendar_moved: function (event) {
            if (event.change !== "M") {
                // We only care when months are displayed
                return;
            }
            // Preload dates if needed and show evented days
            this.preload_dates(event.viewDate);
        },

        preload_dates: function (when) {
            var margin = moment.duration(4, "months");
            // Don't preload if we have up to 4 months of margin
            if (
                this._dates.min && this._dates.max &&
                this._dates.min <= when - margin &&
                this._dates.max >= when + margin
            ) {
                return $.Deferred().resolve();
            }
            // Default values
            margin.add(2, "months");
            var start = moment(when - margin),
                end = moment(when + margin);
            // If we already preloaded, preload 6 more months
            if (this._dates.min) {
                start.subtract(6, "months");
            }
            if (this._dates.max) {
                end.add(6, "months");
            }
            // Do the preloading
            return this.load_dates(start, end);
        },

        load_dates: function (start, end) {
            return ajax.rpc(
                "/website_event_snippet_calendar/days_with_events",
                {
                    start: start.format(DATE_FORMAT),
                    end: end.format(DATE_FORMAT),
                }
            ).done($.proxy(this, "_update_dates_cache", start, end));
        },

        _update_dates_cache: function (start, end, dates) {
            if (!this._dates.min || this._dates.min > start) {
                this._dates.min = start;
            }
            if (!this._dates.max || this._dates.max < end) {
                this._dates.max = end;
            }
            this._dates.matches = _.union(this._dates.matches, dates);
        },

        load_events: function (day, limit) {
            return ajax.rpc(
                "/website_event_snippet_calendar/events_for_day",
                {day: day, limit: limit}
            );
        },

        render_calendar: function () {
            var enabledDates = _.map(this._dates.matches, function (ndate) {
                return moment(ndate, DATE_FORMAT);
            });
            this.$calendar.empty().datetimepicker(_.extend({},
                this.datepicker_options, {'enabledDates': enabledDates}));
        },

        render_list: function (events) {
            _.each(events, function (element) {
                var date_begin_located = moment(
                    element.date_begin_pred_located, DATETIME_FORMAT);
                element.date_begin = date_begin_located.format(
                    this.date_format);
            }, this);
            this.$list.html(core.qweb.render(
                "website_event_snippet_calendar.list",
                {events: events}
            ));
        },
    });

    animation.registry.website_event_snippet_calendar = CalendarList;

    return {
        CalendarList: CalendarList,
        DATE_FORMAT: DATE_FORMAT,
        DATETIME_FORMAT: DATETIME_FORMAT,
        INVERSE_FORMAT: INVERSE_FORMAT,
    };

});

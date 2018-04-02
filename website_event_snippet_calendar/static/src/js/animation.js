/* Copyright 2018 Tecnativa - Jairo Llopis
 * License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl). */

odoo.define('website_event_snippet_calendar.animation', function (require) {
    "use strict";

    var animation = require("web_editor.snippets.animation");
    var core = require("web.core");
    var time = require("web.time");
    var ajax = require("web.ajax");

    var DATE_FORMAT = time.strftime_to_moment_format("%Y-%m-%d");
    // HACK https://github.com/tempusdominus/bootstrap-3/issues/73
    var INVERSE_FORMAT = "L";

    var CalendarList = animation.Class.extend({
        selector: ".s_event_calendar_list",

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
            if (editable_mode) {
                return;
            }
            this._dates = {
                min: null,
                max: null,
                matches: [],
            };
            this.$calendar = this.$(".s_event_calendar")
                .on("dp.change", $.proxy(this, "day_selected"))
                .on("dp.classify", $.proxy(this, "highlight_day"))
                .on("dp.update", $.proxy(this, "calendar_moved"));
            this.$list = this.$(".s_event_list");
            this.default_amount = Number(this.$(".js_amount").html()) || 4;
            this.loaded_templates = ajax.loadXML(
                "/website_event_snippet_calendar/static/src/xml/snippets.xml",
                core.qweb
            );
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
            this.preload_dates(event.viewDate)
                .done($.proxy(this, "highlight_month"));
        },

        highlight_day: function (event) {
            var match = this._dates.matches.indexOf(
                event.date.format(DATE_FORMAT)
            );
            if (match === -1) {
                return;
            }
            event.classNames.push("has-events");
        },

        highlight_month: function () {
            var _dates = this._dates.matches;
            this.$calendar.find(".day").filter(function () {
                var day = moment(this.dataset.day, INVERSE_FORMAT);
                return _dates.indexOf(day.format(DATE_FORMAT)) !== -1;
            }).addClass("has-events");
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
            )
            .done($.proxy(this, "_update_dates_cache", start, end));
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
            this.$calendar.empty().datetimepicker(this.datepicker_options);
        },

        render_list: function (events) {
            this.loaded_templates.done($.proxy(this, "_render_list", events));
        },
        _render_list: function (events) {
            _.each(events, function (element) {
                element.date_begin = moment(element.date_begin)
                    .format(this.date_format);
            }, this);
            this.$list.html(core.qweb.render(
                "website_event_snippet_calendar.list",
                {events: events}
            ));
        }
    });

    animation.registry.website_event_snippet_calendar = CalendarList;

    return {
        CalendarList: CalendarList,
        DATE_FORMAT: DATE_FORMAT,
        INVERSE_FORMAT: INVERSE_FORMAT,
    };

});

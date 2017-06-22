/* Copyright 2016-2017 Jairo Llopis <jairo.llopis@tecnativa.com>
 * License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl). */
odoo.define("website_event_filter_selector.tour", function (require) {
    "use strict";
    var base = require("web_editor.base");
    var tour = require('web_tour.tour');
    var filter = require("website_event_filter_selector");

    var id = filter.prototype.selector,
        $filters = $(id);

    // Get an option value by its text
    function opt_val(filter, option_text) {
        return _.str.sprintf(
            "text(%s)",
            $filters.find(
                _.str.sprintf(
                    "select[name='%s']>option:contains('%s')",
                    filter,
                    option_text
                )
            ).val()
        );
    }

    // Get an element in the selection filters form
    function sel(name) {
        return _.str.sprintf("%s select[name='%s']", id, name);
    }

    // Define tour
    var options = {
        url: "/event",
        test: true,
        wait_for: base.ready(),
    };
    var steps = [
        {
            content: "Get old events",
            // Make sure Taiwan exists; it's used in the last step
            extra_trigger: "#left_column li:contains('Taiwan')",
            trigger: sel("date"),
            run: "text(old)",
        },
        {
            content: "Get online events",
            extra_trigger: "#left_column .active:contains('Old Events')",
            trigger: sel("country"),
            run: "text(online)",
        },
        {
            content: "Get every country events",
            extra_trigger: "#left_column .active:contains('Online Events')",
            trigger: sel("country"),
            run: "text(all)",
        },
        {
            content: "Get this month's events",
            extra_trigger: "#left_column .active:contains('All Countries')",
            trigger: sel("date"),
            run: "text(month)",
        },
        {
            content: "Get USA events",
            extra_trigger: "#left_column .active:contains('This month')",
            trigger: sel("country"),
            run: opt_val("country", "United States"),
        },
        {
            content: "Get Fremont events",
            extra_trigger: "#left_column .active:contains('United States')",
            trigger: sel("city"),
            run: opt_val("city", "Fremont"),
        },
        {
            content: "Get all countries' events",
            extra_trigger: "#left_column .active:contains('Fremont')",
            trigger: sel("country"),
            run: "text(all)",
        },
        {
            content: "Get Conference events",
            extra_trigger: "#left_column .active:contains('All Countries')",
            trigger: sel("type"),
            run: opt_val("type", "Conference"),
        },
        {
            content: "Taiwan has no conferences",
            extra_trigger: "#left_column .active:contains('Conference')",
            trigger: "#left_column:not(li:contains('Taiwan'))",
        },
    ];

    tour.register("website_event_filter_selector", options, steps);

    return {
        opt_val: opt_val,
        options: options,
        steps: steps,
        $filters: $filters,
    }
});

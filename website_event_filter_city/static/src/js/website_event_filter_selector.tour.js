/* © 2016 Antiun Ingeniería S.L. - Jairo Llopis
 * License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl). */
odoo.define("website_event_filter_selector.tour", function (require) {
    "use strict";
    var Tour = require('web.Tour');
    var filter = require("website_event_filter_selector");

    var id = filter.prototype.selector,
        $filters = $(id);

    // Get an option value by its text
    function opt_val(filter, option_text) {
        return $filters.find(
            _.str.sprintf(
                "select[name='%s']>option:contains('%s')",
                filter,
                option_text
            )
        ).val();
    }

    // Get an element in the selection filters form
    function sel(name) {
        return _.str.sprintf("%s %s", id, name);
    }

    var tour = {
        id: "website_event_filter_selector",
        name: "Apply some filters",
        path: "/event",
        mode: "test",
        steps: [
            {
                title: "Get old events",
                waitFor: id,
                element: sel("#filter_date"),
                sampleText: "old",
            },
            {
                title: "Get online events",
                waitFor: "#left_column .active:contains('Old Events')",
                element: sel("#filter_country"),
                sampleText: "online",
            },
            {
                title: "Get every country events",
                waitFor: "#left_column .active:contains('Online Events')",
                waitNot: "#left_column li:contains('Fremont')",
                element: sel("#filter_country"),
                sampleText: "all",
            },
            {
                title: "Get this month's events",
                waitFor: "#left_column .active:contains('All Countries')",
                element: sel("#filter_date"),
                sampleText: "month",
            },
            {
                title: "Get USA events",
                waitFor: "#left_column .active:contains('This month')",
                waitNot: sel("#filter_country:contains('Online Events')"),
                element: sel("#filter_country"),
                sampleText: opt_val("country", "United States"),
            },
            {
                title: "Get Fremont events",
                waitFor: "#left_column .active:contains('United States')",
                waitNot: "#left_column li:contains('Wavre')",
                element: sel("#filter_city"),
                sampleText: opt_val("city", "Fremont"),
            },
            {
                title: "Get all countries' events",
                waitFor: "#left_column .active:contains('Fremont')",
                waitNot: "#left_column li:contains('Wavre')",
                element: sel("#filter_country"),
                sampleText: "all",
            },
            {
                title: "Get Conference events",
                waitFor: "#left_column .active:contains('All Countries')",
                element: sel("#filter_type"),
                sampleText: opt_val("type", "Conference"),
            },
            {
                title: "Taiwan has no conferences",
                waitFor: "#left_column .active:contains('Conference')",
                waitNot: "#left_column li:contains('Taiwan')",
            },
        ]
    }

    Tour.register(tour);

    return {
        opt_val: opt_val,
        tour: tour,
        $filters: $filters,
    }
});

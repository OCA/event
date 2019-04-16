/* Copyright 2016-2017 Jairo Llopis <jairo.llopis@tecnativa.com>
 * License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl). */
odoo.define("website_event_filter_selector.tour", function (require) {
    "use strict";
    var base = require("web_editor.base");
    var tour = require('web_tour.tour');
    var filter = require("website_event_filter_selector");

    var id = filter.prototype.selector,
        $filters = $(id);

    // Get an element in the selection filters form
    function sel (name) {
        return _.str.sprintf("%s select[name='%s']", id, name);
    }

    // Get an option value by its text
    function opt_val (option_text) {
        return function (action_helper) {
            var option_id = this.$anchor.children(_.str.sprintf(
                "option:contains('%s')", option_text
            )).val();
            action_helper.text(option_id);
        };
    }

    // Define tour
    var options = {
        url: "/event",
        test: true,
        wait_for: base.ready(),
    };
    var steps = [
        {
            extra_trigger:
                "#middle_column:not(:contains('Barcelona Days 2017'))" +
                ":not(:contains('Online Code Sprint 2018'))" +
                ":not(:contains('Sevilla Code Sprint 2018'))" +
                ":not(:contains('Sevilla Code Awesome Breakfast'))",
            run: "text old",
            trigger: sel("date"),
        },
        {
            extra_trigger:
                "#middle_column:contains('Barcelona Days 2017')" +
                ":contains('Online Code Sprint 2018')" +
                ":contains('Sevilla Code Sprint 2018')" +
                ":contains('Sevilla Awesome Breakfast 2018')",
            trigger: sel("country"),
            run: "text online",
        },
        {
            extra_trigger:
                "#middle_column:not(:contains('Barcelona Days 2017'))" +
                ":contains('Online Code Sprint 2018')" +
                ":not(:contains('Sevilla Code Sprint 2018'))" +
                ":not(:contains('Sevilla Code Awesome Breakfast'))",
            trigger: sel("country"),
            run: opt_val("Spain"),
        },
        {
            extra_trigger:
                "#middle_column:contains('Barcelona Days 2017')" +
                ":not(:contains('Online Code Sprint 2018'))" +
                ":contains('Sevilla Code Sprint 2018')" +
                ":contains('Sevilla Awesome Breakfast 2018')",
            trigger: sel("city"),
            run: opt_val("Sevilla"),
        },
        {
            extra_trigger:
                "#middle_column:not(:contains('Barcelona Days 2017'))" +
                ":not(:contains('Online Code Sprint 2018'))" +
                ":contains('Sevilla Code Sprint 2018')" +
                ":contains('Sevilla Awesome Breakfast 2018')",
            trigger: sel("type"),
            run: opt_val("Code Sprint"),
        },
        {
            extra_trigger:
                "#middle_column:not(:contains('Barcelona Days 2017'))" +
                ":not(:contains('Online Code Sprint 2018'))" +
                ":contains('Sevilla Code Sprint 2018')" +
                ":not(:contains('Sevilla Awesome Breakfast 2018'))",
            trigger: "a:contains('Sevilla Code Sprint 2018')",
        },
    ];

    tour.register("website_event_filter_selector", options, steps);

    return {
        opt_val: opt_val,
        options: options,
        steps: steps,
        $filters: $filters,
    };
});

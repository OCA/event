/* Copyright 2016-2017 Tecnativa - Jairo Llopis
 * Copyright 2021 Tecnativa - Víctor Martínez
 * License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl). */
odoo.define("website_event_filter_city.tour", function(require) {
    "use strict";
    var tour = require("web_tour.tour");

    tour.register(
        "website_event_filter_city",
        {
            test: true,
            url: "/event",
        },
        [
            {
                trigger: "a.dropdown-toggle:contains('Next Events')",
            },
            {
                extra_trigger:
                    "#o_wevent_index_main_col h5 a:not(:contains('Barcelona Days 2017'))" +
                    ":not(:contains('Online Code Sprint 2018'))" +
                    ":not(:contains('Sevilla Code Sprint 2018'))" +
                    ":not(:contains('Sevilla Code Awesome Breakfast'))",
                trigger: "a.dropdown-item:contains('Past Events')",
            },
            {
                extra_trigger: "a.dropdown-toggle:contains('Past Events')",
                trigger: "a.dropdown-toggle:contains('All countries')",
            },
            {
                extra_trigger:
                    "#o_wevent_index_main_col h5 a:not(:contains('Barcelona Days 2017'))" +
                    ":contains('Online Code Sprint 2018')" +
                    ":not(:contains('Sevilla Code Sprint 2018'))" +
                    ":not(:contains('Sevilla Code Awesome Breakfast'))",
                trigger: "a.dropdown-item:contains('Spain')",
            },
            {
                extra_trigger: "a.dropdown-toggle:contains('Spain')",
                trigger: "a.dropdown-toggle:contains('All Cities')",
            },
            {
                extra_trigger:
                    "#o_wevent_index_main_col:contains('Barcelona Days 2017')" +
                    ":contains('Sevilla Code Sprint 2018')" +
                    ":contains('Sevilla Awesome Breakfast 2018')",
                trigger: "a.dropdown-item:contains('Sevilla')",
            },
            {
                extra_trigger: "a.dropdown-toggle:contains('Sevilla')",
                trigger: "a.dropdown-toggle:contains('All Categories')",
            },
            {
                extra_trigger:
                    "#o_wevent_index_main_col:not(:contains('Barcelona Days 2017'))" +
                    ":not(:contains('Online Code Sprint 2018'))" +
                    ":contains('Sevilla Code Sprint 2018')" +
                    ":contains('Sevilla Awesome Breakfast 2018')",
                trigger: "a.dropdown-item:contains('Code Sprint')",
            },
            {
                extra_trigger:
                    "#o_wevent_index_main_col:not(:contains('Barcelona Days 2017'))" +
                    ":not(:contains('Online Code Sprint 2018'))" +
                    ":contains('Sevilla Code Sprint 2018')" +
                    ":not(:contains('Sevilla Awesome Breakfast 2018'))",
                trigger: "a:contains('Sevilla Code Sprint 2018')",
            },
        ]
    );
});

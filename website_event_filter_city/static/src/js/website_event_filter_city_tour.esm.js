/* Copyright 2016-2017 Tecnativa - Jairo Llopis
 * Copyright 2021 Tecnativa - Víctor Martínez
 * Copyright 2023 Tecnativa - David Vidal
 * License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl). */
import {registry} from "@web/core/registry";

registry.category("web_tour.tours").add("website_event_filter_city", {
    url: "/event",
    steps: () => [
        {
            trigger: "a.dropdown-toggle:contains('Upcoming')",
            run: "click",
        },
        {
            trigger: "a.dropdown-item:contains('Past Events')",
            run: "click",
        },
        {
            trigger: "a.dropdown-toggle:contains('Past Events')",
        },
        {
            trigger: "a.dropdown-toggle:contains('All countries')",
        },
        {
            trigger:
                "#o_wevent_index_main_col h5 span:not(:contains('Barcelona Days 2017'))" +
                ":contains('Online Code Sprint 2018')" +
                ":not(:contains('Sevilla Code Sprint 2018'))" +
                ":not(:contains('Sevilla Code Awesome Breakfast'))",
        },
        {
            trigger: "a.dropdown-toggle:contains('All countries')",
            run: "click",
        },
        {
            trigger: "a.dropdown-item:contains('Spain')",
            run: "click",
        },
        {
            trigger: "a.dropdown-toggle:contains('Spain')",
        },
        {
            trigger:
                "#o_wevent_index_main_col:contains('Barcelona Days 2017')" +
                ":contains('Sevilla Code Sprint 2018')" +
                ":contains('Sevilla Awesome Breakfast 2018')",
        },
        {
            trigger: "a.dropdown-toggle:contains('All Cities')",
            run: "click",
        },
        {
            trigger: "a.dropdown-item:contains('Sevilla')",
            run: "click",
        },
        {
            trigger: "a.dropdown-toggle:contains('Sevilla')",
        },
        {
            trigger: "a.dropdown-toggle:contains('Type')",
            run: "click",
        },
        {
            trigger: "span.dropdown-item:contains('Code Sprint')",
            run: "click",
        },
        {
            trigger:
                "#o_wevent_index_main_col:not(:contains('Barcelona Days 2017'))" +
                ":not(:contains('Online Code Sprint 2018'))" +
                ":contains('Sevilla Code Sprint 2018')" +
                ":contains('Sevilla Awesome Breakfast 2018')",
        },
        {
            trigger: "a:contains('Sevilla Code Sprint 2018')",
            run: "click",
        },
        {
            trigger:
                "#o_wevent_index_main_col:not(:contains('Barcelona Days 2017'))" +
                ":not(:contains('Online Code Sprint 2018'))" +
                ":contains('Sevilla Code Sprint 2018')" +
                ":not(:contains('Sevilla Awesome Breakfast 2018'))",
        },
    ],
});

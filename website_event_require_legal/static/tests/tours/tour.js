/* Copyright 2025 Tecnativa - Pilar Vargas
 * License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl). */

odoo.define("website_event_require_legal.tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    var steps = [
        {
            trigger:
                'a:has(span[itemprop="name"]:contains("Test event for require legal"))',
        },
        {
            trigger: '.a-submit:contains("Register")',
        },
        // Cannot proceed until the terms are accepted.
        {
            trigger: 'button:contains("Continue")',
        },
        {
            trigger: "#accepted_event_legal_terms",
        },
        {
            content: "Validate attendees details",
            extra_trigger:
                "input[name='1-name'], input[name='2-name'], input[name='3-name']",
            trigger: 'button:contains("Continue")',
        },
        {
            trigger: ".o_wereg_confirmed_attendees",
        },
    ];

    tour.register(
        "website_event_require_legal",
        {
            url: "/event",
            test: true,
        },
        steps
    );

    return {
        steps: steps,
    };
});

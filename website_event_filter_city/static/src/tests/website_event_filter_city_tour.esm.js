/* Copyright 2016-2017 Tecnativa - Jairo Llopis
 * Copyright 2021 Tecnativa - Víctor Martínez
 * Copyright 2023 Tecnativa - David Vidal
 * Copyright 2026 Tecnativa - Adasat Torres
 * License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl). */
import {registry} from "@web/core/registry";

registry.category("web_tour.tours").add("website_event_filter_city", {
    steps: () => [
        {
            trigger: ".btn[title='Filter by Country']:contains('All countries')",
            run: "click",
        },
        {
            trigger: "a.dropdown-item:contains('Spain')",
            expectUnloadPage: true,
            run: "click",
        },
        {
            trigger: ".btn[title='Filter by City']:contains('All Cities')",
            run: "click",
        },
        {
            trigger: "a.dropdown-item:contains('Santa Cruz de Tenerife')",
            expectUnloadPage: true,
            run: "click",
        },
        {
            trigger: "article:contains('My Event Test')",
        },
    ],
});

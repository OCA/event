/* Copyright 2018 Tecnativa - Jairo Llopis
 * License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl). */

odoo.define("website_event_snippet_calendar.snippets", function (require) {
    "use strict";

    var options = require("web_editor.snippets.options");

    options.registry.website_event_snippet_calendar_list = options.Class.extend({
        increase: function () {
            this.$amount = this.$(".js_amount");
            var current = parseInt(this.$amount.html(), 10) || 4;
            current += 1;
            this.$amount.html(current);
        },
        decrease: function () {
            this.$amount = this.$(".js_amount");
            var current = parseInt(this.$amount.html(), 10) || 4;
            current -= 1;
            this.$amount.html(current || 1);
        },
    });
});

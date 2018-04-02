/* Copyright 2018 Tecnativa - Jairo Llopis
 * License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl). */

odoo.define('website_event_snippet_calendar.snippets', function(require) {
    "use strict";

    var options = require('web_editor.snippets.options');

    var List = options.Class.extend({
        start: function () {
            this._super.apply(this, arguments);
            this.$amount = this.$(".js_amount");
        },

        /**
         * Add or remove a given amount of events by default
         *
         * @param {String} type Event type
         * @param {Number} value How many events to add
         */
        increase: function (type, value) {
            var increment = Number(value);
            if (type === "reset") {
                increment *= -1;
            }
            var current = Number(this.$amount.html()) || 4;
            current += increment;
            this.$amount.html(current);
        },
    });

    options.registry.website_event_snippet_calendar_list = List;

    return {
        List: List,
    };
});

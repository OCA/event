/* © 2016 Antiun Ingeniería S.L. - Jairo Llopis
 * License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl). */
odoo.define("website_event_filter_selector", function (require) {
    "use strict";
    var animation = require('web_editor.snippets.animation');

    return animation.registry.website_event_filter_selector =
    animation.Class.extend({
        selector: "#website_event_filter_selector",

        // Bind events
        start: function () {
            this.$("select").on("change", $.proxy(this.submit, this));
        },

        // Submit form programatically
        submit: function (event) {
            $(event.target).closest("form").submit();
        },
    });
});

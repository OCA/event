// Copyright 2023 Camptocamp SA
// License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)

odoo.define("website_event_sale_constraints.ticket_details", function (require) {
    "use strict";

    const ticketDetailsWidget = require("website_event.ticket_details");

    ticketDetailsWidget.include({
        // --------------------------------------------------------------------------
        // Private
        // --------------------------------------------------------------------------

        /**
         * @private
         */
        _getParentTicketCount: function () {
            var ticketCount = 0;
            this.$(".parent_ticket_select").each(function () {
                ticketCount += parseInt($(this).val());
            });
            return ticketCount;
        },

        /**
         * @private
         */
        _getChildTicketCount: function () {
            var ticketCount = 0;
            this.$(".child_ticket_select").each(function () {
                ticketCount += parseInt($(this).val());
            });
            return ticketCount;
        },

        // --------------------------------------------------------------------------
        // Handlers
        // ----
        /**
         * @override
         */
        _onTicketQuantityChange: function () {
            const parents_count = this._getParentTicketCount();
            const children_count = this._getChildTicketCount();
            this.$("button.btn-primary").attr("disabled", parents_count === 0);
            this.$(".event_sale_constraints_message").attr(
                "hidden",
                parents_count != 0 || children_count === 0
            );
        },
    });
});

// Copyright 2023 Camptocamp SA (https://www.camptocamp.com).
// License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

odoo.define("website_event_sale_joined_constraint.ticket_details", function (require) {
    "use strict";

    const ticketDetailsWidget = require("website_event.ticket_details");

    ticketDetailsWidget.include({
        // --------------------------------------------------------------------------
        // Private
        // --------------------------------------------------------------------------

        /**
         * @private
         * @returns {integer} Number of selected parent tickets
         */
        _getParentTicketCount: function () {
            var ticketCount = 0;
            this.$(".parent_ticket_select").each(function () {
                ticketCount += parseInt($(this).val(), 10);
            });
            return ticketCount;
        },

        /**
         * @private
         * @returns {integer} Number of selected child tickets
         */
        _getChildTicketCount: function () {
            var ticketCount = 0;
            this.$(".child_ticket_select").each(function () {
                ticketCount += parseInt($(this).val(), 10);
            });
            return ticketCount;
        },

        // --------------------------------------------------------------------------
        // Handlers
        // --------------------------------------------------------------------------
        /**
         * @override
         */
        _onTicketQuantityChange: function () {
            this._super.apply(this, arguments);
            const parents_count = this._getParentTicketCount();
            const children_count = this._getChildTicketCount();
            this.$("button.btn-primary").attr("disabled", parents_count === 0);
            this.$(".event_sale_constraint_message").attr(
                "hidden",
                parents_count !== 0 || children_count === 0
            );
        },
    });
});

/*
Copyright 2021 Camptocamp SA - Iván Todorovich
License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
*/

odoo.define("pos_event_sale.db", function(require) {
    "use strict";

    const PosDB = require("point_of_sale.DB");
    const rpc = require("web.rpc");

    PosDB.include({
        get_event_by_id: function(id) {
            return this.event_by_id[id];
        },

        get_event_ticket_by_id: function(id) {
            return this.event_ticket_by_id[id];
        },

        get_events_by_product_id: function(product_id) {
            const tickets = this.get_event_tickets_by_product_id(product_id);
            return _.unique(tickets.map(ticket => ticket.event_id));
        },

        get_event_tickets_by_product_id: function(product_id) {
            return this.event_ticket_by_product_id[product_id] || [];
        },

        /**
         * Updates the event seats_available fields from the backend.
         * Updates both event.event and their related event.ticket records.
         *
         * @param {Array} event_ids
         * @param {Object} options passed to rpc.query. Optional
         * @returns A promise
         */
        update_event_seats_available: function(event_ids, options) {
            // Update event.event seats_available
            const d1 = rpc
                .query(
                    {
                        model: "event.event",
                        method: "search_read",
                        args: [
                            [["id", "in", event_ids]],
                            [
                                "id",
                                "seats_availability",
                                "seats_available",
                                "seats_max",
                            ],
                        ],
                    },
                    options
                )
                .then(events => {
                    for (const event of events) {
                        Object.assign(this.event_by_id[event.id], event);
                    }
                });
            // Update event.event.ticket seats_available
            const d2 = rpc
                .query(
                    {
                        model: "event.event.ticket",
                        method: "search_read",
                        args: [
                            [["event_id", "in", event_ids]],
                            [
                                "id",
                                "seats_availability",
                                "seats_available",
                                "seats_max",
                            ],
                        ],
                    },
                    options
                )
                .then(tickets => {
                    for (const ticket of tickets) {
                        Object.assign(this.event_ticket_by_id[ticket.id], ticket);
                    }
                });
            // Resolve when both finish
            return Promise.all([d1, d2]);
        },
    });

    return PosDB;
});

/** @odoo-module **/
/*
    Copyright 2021 Moka Tourisme (https://www.mokatourisme.fr)
    Copyright 2023 Tecnativa - Carlos Roca
    @author Iván Todorovich <ivan.todorovich@gmail.com>
    License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
*/
import {RelationalModel} from "@web/views/relational_model";
import {patch} from "@web/core/utils/patch";

patch(RelationalModel.prototype, "event_sale_session.RelationalModel", {
    setup(params, {action}) {
        // Trick to keep model as the main EventConfiguratorRelationalModel is not exported
        // https://github.com/odoo/odoo/blob/fa142764b2f583793047f794bbc102e6e0807c31/addons/event_sale/static/src/js/event_configurator_model.js#L17
        // TODO: Try to patch directly the EventConfiguratorRelationalModel
        this._super(...arguments);
        this.oldDoAction = action.doAction;
        const model = this;
        async function EventConfiguratorDoAction(actionRequest, options = {}) {
            const state = model.root.data;
            if (
                state &&
                state.event_use_sessions &&
                actionRequest.type === "ir.actions.act_window_close" &&
                actionRequest.infos.eventConfiguration &&
                !options.skip_definition
            ) {
                actionRequest.infos.eventConfiguration.event_session_id =
                    state.event_session_id;
                options.skip_definition = true;
            }
            return model.oldDoAction(actionRequest, options);
        }
        this.action.doAction = EventConfiguratorDoAction;
    },
});

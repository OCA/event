/** @odoo-module **/
/*
    Copyright 2021 Moka Tourisme (https://www.mokatourisme.fr)
    Copyright 2023 Tecnativa - Carlos Roca
    @author Iván Todorovich <ivan.todorovich@gmail.com>
    License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
*/
import {EventConfiguratorRecord} from "@event_sale/js/event_configurator_model";
import {patch} from "@web/core/utils/patch";

patch(EventConfiguratorRecord.prototype, "event_sale_session.EventConfiguratorRecord", {
    /**
     * @override
     */
    async save() {
        const doAction = this.model.action.doAction;
        this.model.action.doAction = (actionRequest, options = {}) => {
            actionRequest.infos.eventConfiguration.event_session_id =
                this.data.event_session_id;
            return doAction(actionRequest, options);
        };
        const res = await this._super.apply(this, arguments);
        this.model.action.doAction = doAction;
        return res;
    },
});

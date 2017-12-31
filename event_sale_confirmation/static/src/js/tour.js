/* Copyright 2018 IT-Projects LLC - Ivan Yelizariev
   License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl). */
odoo.define('event_sale_confirmation.tour', function(require){

    var core = require('web.core');
    var tour = require("web_tour.tour");
    var base = require("web_editor.base");

    var _t = core._t;
    var options = {
        test: true,
        // use debug to open Attendees menu
        url: '/web?debug',
        wait_for: base.ready()
    };

    var common_steps = [
        {
            content: _t('Go to Events'),
            trigger: '.o_app[data-menu-xmlid="event.event_main_menu"], .oe_menu_toggler[data-menu-xmlid="event.event_main_menu"]',
        },
        {
            content: _t('Go to Attendees'),
            // TODO this works only for odoo CE
            trigger: '.oe_menu_leaf[data-menu-xmlid="event.menu_action_registration"]',
        }
    ];

    tour.register('event_sale_confirmation.can_confirm', options, common_steps.concat([
        {
            content: _t('Confirm in tree view'),
            trigger: '.o_view_manager_content .fa-check'
        },
        {
            content: _t('Wait for confirmation'),
            trigger: '.o_view_manager_content .fa-level-down',
            run: function(){
                //no action needed, we only waited
            },
        },
        {
            content: _t('Open form to confirm'),
            trigger: '.o_view_manager_content tbody tr:has(.fa-check)',
            run: 'click',
        },
        {
            content: _t('Confirm in form view'),
            trigger: '.o_form_view button:contains(Confirm)',
        },
        {
            content: _t('Wait for confirmation'),
            trigger: '.o_form_view .oe_form_field_status li.oe_active .label:contains(Confirmed)',
        },
    ]));

    tour.register('event_sale_confirmation.cannot_confirm', options, common_steps.concat([
        {
            content: _t('Confirm in tree view is not available'),
            trigger: '.o_view_manager_content tr:has([data-field="state"]:contains(Unconfirmed))',
            run: function(){
                if (this.$anchor.has('.fa-check:visible').length){
                    console.log('error', 'Confirmation button is still available in tree view');
                }

            }
        },
        {
            content: _t('Open form'),
            trigger: '.o_view_manager_content tr:has([data-field="state"]:contains(Unconfirmed))',
            run: 'click',
        },
        {
            content: _t('Wait for confirmation'),
            trigger: '.o_form_view .oe_form_field_status li.oe_active .label:contains(Unconfirmed)',
            run: function(){
                if ($('.o_form_view button:visible:contains(Confirm)').length){
                    console.log('error', 'Confirmation button is still available in form view');
                }

            }
        },
    ]));


});

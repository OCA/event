# -*- coding: utf-8 -*-
# © initOS GmbH 2017
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from collections import defaultdict

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class PollQuestion(http.Controller):
    @http.route('/questions/<model("poll.question"):question>', type='http',
                auth='public', website=True)
    def render_questions_page(self, question, uuid):
        if uuid != question.uuid:
            return request.render('website.404')

        answers_list = [(answer.res_partner_id, answer)
                        for answer in question.question_answer_ids]
        answers_dict = defaultdict(list)
        for k, v in answers_list:
            answers_dict[k].append(v)

        answers_sum_dict = {option: defaultdict()
                            for option in question.option_ids}
        answers_sum_list = [(answer.option_id, answer.answer)
                            for answer in question.question_answer_ids]
        for k1, k2 in answers_sum_list:
            answers_sum_dict[k1][k2] = answers_sum_dict[k1].get(k2, 0) + 1

        for k in answers_sum_dict:
            for i in ['1', '2', '3']:
                if i not in answers_sum_dict[k].keys():
                    answers_sum_dict[k][i] = 0
            answers_sum_dict[k] = sorted(answers_sum_dict[k].iteritems(),
                                         key=lambda (k, v): v,
                                         reverse=True)

        return request.render('simple_poll.poll_page', {
            'question': question,
            'answers': answers_dict,
            'answer_sum': answers_sum_dict
        })

    # AJAX submission of a page
    @http.route(['/questions/submit/<model("poll.question"):question>'],
                type='http', methods=['POST'], auth='public', website=True)
    def submit(self, question, uuid, **post):
        if uuid != question.uuid:
            return request.render('website.404')
        request.env['question.answer'].sudo().save_answer(question, post)
        return http.request.render(
            'simple_poll.submit_poll',
            {'question': question}
        )

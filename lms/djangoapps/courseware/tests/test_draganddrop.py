# -*- coding: utf-8 -*-
"""Draganddrop input and response type integration tests using mongo modulestore."""

import json

from . import BaseTestResponseType
from capa.tests.response_xml_factory import DraganddropResponseXmlFactory


class TestDraganddrop(BaseTestResponseType):
    """Integration test for draganddropresponse."""
    answer = """
correct_answer = [
        {'draggables': ['d_1', 'd_2'],
        'targets': ['t_2', 't_3', 't_4' ],
        'rule':'anyof'
        }]
if draganddrop.grade(submission[0], correct_answer):
    correct = ['correct']
else:
    correct = ['incorrect']
            """

    RESPONSETYPE_as_str = DraganddropResponseXmlFactory().build_xml(answer=answer)

    def test_problem_save(self):
        """Checks that save is working."""
        user_input = json.dumps([
            {'p': 'p_l'},
            {'p': 'p_r'}
        ])
        user = self.users[0]
        response = self.clients[user.username].post(
            self.get_url('problem_save'),
            {self.item_module.location.html_id(): user_input},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        users_state = json.loads(response.content)
        self.assertTrue(users_state['success'])

    def test_problem_check_incorrect(self):
        """Checks sure that grader can see incorrent input."""
        user_input = json.dumps([
            {'p': 'p_l'},
            {'p': 'p_r'}
        ])
        user = self.users[0]
        # import ipdb; ipdb.set_trace()

        response = self.clients[user.username].post(
            self.get_url('problem_check'),
            {self.answer_key_prefix + '2_1': user_input},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        users_state = json.loads(response.content)
        self.assertEqual(users_state['success'], 'incorrect')

    def test_problem_check_correct(self):
        """Checks that grader can see correct answer."""
        user_input = json.dumps([
            {'d_1': 't_2'},
            {'d_2': 't_4'}
        ])
        user = self.users[0]
        response = self.clients[user.username].post(
            self.get_url('problem_check'),
            {self.answer_key_prefix + '2_1': user_input},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        users_state = json.loads(response.content)
        self.assertEqual(users_state['success'], 'correct')

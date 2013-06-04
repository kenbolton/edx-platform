# -*- coding: utf-8 -*-
"""Draganddrop input and response type integration tests using mongo modulestore."""

import json

from . import BaseTestResponseType
from capa.tests.response_xml_factory import DraganddropResponseXmlFactory


class TestDraganddrop(BaseTestResponseType):
    """Integration test for draganddropresponse."""
    answer = """
correct_answer = [
        {'draggables': ['1', '2'],
        'targets': ['t2', 't3', 't4' ],
        'rule':'anyof'
        }]
if draganddrop.grade(submission[0], correct_answer):
    correct = ['correct']
else:
    correct = ['incorrect']
            """

    RESPONSETYPE_as_str = DraganddropResponseXmlFactory().build_xml(answer=answer)

    def test_problem_save(self):
        """TODO"""
        user_input = json.dumps([
            {'p': 'p_l'},
            {'p': 'p_r'},
            {'s': 's_l'},
            {'s': 's_r'},
            {'up': {'1': {'p': 'p_l'}}},
            {'up': {'3': {'p': 'p_l'}}},
            {'up': {'1': {'p': 'p_r'}}},
            {'up': {'3': {'p': 'p_r'}}},
            {'up_and_down': {'1': {'s': 's_l'}}},
            {'up_and_down': {'1': {'s': 's_r'}}}
        ])
        user = self.users[0]
        response = self.clients[user.username].post(
            self.get_url('problem_save'),
            {self.item_module.location.html_id(): user_input},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        users_state = json.loads(response.content)
        self.assertTrue(users_state['success'])

    def test_problem_check(self):
        """TODO"""
        user_input = json.dumps([
            {'p': 'p_l'},
            {'p': 'p_r'},
            {'s': 's_l'},
            {'s': 's_r'},
            {'up': {'1': {'p': 'p_l'}}},
            {'up': {'3': {'p': 'p_l'}}},
            {'up': {'1': {'p': 'p_r'}}},
            {'up': {'3': {'p': 'p_r'}}},
            {'up_and_down': {'1': {'s': 's_l'}}},
            {'up_and_down': {'1': {'s': 's_r'}}}
        ])
        user = self.users[0]
        # import ipdb; ipdb.set_trace()
        answer_key_prefix = 'input_i4x-MITx-{}-problem-{}_'.format('999', 'Problem_2')
        response = self.clients[user.username].post(
            self.get_url('problem_check'),
            {answer_key_prefix + '2_1': user_input},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        import ipdb; ipdb.set_trace()
        users_state = json.loads(response.content)

        return users_state

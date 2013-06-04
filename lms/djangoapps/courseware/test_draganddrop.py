# -*- coding: utf-8 -*-
"""Draganddrop input and response type integration tests using mongo modulestore."""

import json

from . import BaseTestResponseType
from capa.tests.response_xml_factory import DraganddropResponseXmlFactory


class TestDraganddrop(BaseTestResponseType):
    """Integration test for draganddropresponse."""
    answer = """
    <![CDATA[correct_answer = [
        {'draggables': ['1', '2'],
        'targets': ['t2', 't3', 't4' ],
        'rule':'anyof'
        }]
        if draganddrop.grade(submission[0], correct_answer):
            correct = ['correct']
        else:
            correct = ['incorrect']
        ]]>
            """

    RESPONSETYPE_as_str = DraganddropResponseXmlFactory().build_xml(answer='answer')

    def test_1(self):
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
            self.get_url('submit'),
            {'user_input': user_input},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        users_state = json.loads(response.content)
        import ipdb; ipdb.set_trace()
        return users_state

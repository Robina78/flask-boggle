from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):
        """ Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """ Make sure information is in the session and HTML is displayed"""

        with self.client:
            response = self.client.get('/')
            # html = response.get_data(as_text=True)
            self.assertIn('board', session)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('nplays'))
            # self.assertEqual(response.status_code, 200)
            self.assertIn(b'High Score:', response.data)
            self.assertIn(b'Score:', response.data)
            self.assertIn(b'Timers Left:', response.data)

    def test_valid_word(self):
        """ Test if word is valid (in dictuonary and on board) by modifying the board in the session """

        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["C", "A", "T", "T", "T"],
                                 ["C", "A", "B", "O", "T"],
                                 ["C", "A", "T", "O", "K"],
                                 ["C", "A", "T", "T", "T"],
                                 ["C", "A", "T", "T", "T"]]

        response = self.client.get('/check-word?word=book')
        self.assertEqual(response.json['result'], 'ok')

    def test_invalid_word(self):
        """ Test for word in dictionary but not on board"""
        self.client.get('/')
        response = self.client.get('/check-word?word=media')
        self.assertEqual(response.json['result'], 'not-on-board')

    def non_english_word(self):
        """ Test if word is on the board but it is not English word"""

        self.client.get('/')
        response = self.client.get('/check-word?word=fsjdakfkldsfjdslkfjdlksf')
        self.assertEqual(response.json['result'], 'not-word')

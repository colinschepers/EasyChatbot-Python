import os
import unittest
from flask import abort, url_for
from flask_testing import TestCase
from app import create_app, db
from app.models import User, Dialog, Question, Answer
from config import app_config


class TestBase(TestCase):
    def create_app(self):
        app = create_app('testing')
        app.config.update(
            SQLALCHEMY_DATABASE_URI = "sqlite:///D:/Repositories/EasyChatbot/databases/testing.db"
        )
        return app

    def setUp(self):
        db.create_all()
        admin = User(username="admin", password="admin", is_admin=True)
        test_user = User(username="test_user", password="test_user")

        db.session.add(admin)
        db.session.add(test_user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class TestModels(TestBase):
    def test_user_model(self):
        self.assertEqual(User.query.count(), 2)

    def test_dialog_model(self):
        dialog = Dialog()
        db.session.add(dialog)
        db.session.commit()
        self.assertEqual(Dialog.query.count(), 1)

    def test_question_model(self):
        question = Question(dialog_id=1, text="question")
        db.session.add(question)
        db.session.commit()
        self.assertEqual(Question.query.count(), 1)

    def test_answer_model(self):
        answer = Answer(dialog_id=1, text="answer")
        db.session.add(answer)
        db.session.commit()
        self.assertEqual(Answer.query.count(), 1)


if __name__ == '__main__':
    unittest.main()
from django.test import TestCase, Client
from django.db import IntegrityError

from .models import User, ClassProfile, Quiz, Question, Answer

class QuizrtTests(TestCase):
    fixtures = ['datadump.json']

    def test_fixture_success(self):
        self.assertTrue(User.objects.all().count() > 0)

    def test_create_user(self):
        user = User.objects.create_user(
            username="validUserName",
            name="valid name",
            email="email@test.com",
            password="meo12345"
        )
        self.assertEqual(user.username, "validUserName")

    def test_create_user_no_email(self):
        with self.assertRaises(TypeError):
            User.objects.create_user(
                username="validUserName",
                name="valid name",
                password="meo12345"
            )

    # Todo: implement email validation?
    # def test_create_user_bad_email(self):
    #     User.objects.create_user(
    #         username="validUserName",
    #         name="valid name",
    #         email="emailtest1234com",
    #         password="meo12345"
    #     )

    def test_create_user_duplicate_email(self):
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                username="validUserName",
                name="valid name",
                email="foohooboo@test.com",
                password="meo12345"
            )

    def test_create_user_duplicate_username(self):
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                username="foohooboo",
                name="valid name",
                email="validtestemail@test.com",
                password="meo12345"
            )

    def test_create_profile(self):
        profile = ClassProfile.objects.create(
            name="test profile",
            description="test profile description",
            is_private=True
        )
        self.assertTrue(profile.is_private)

    def test_create_quiz(self):
        quiz = Quiz.objects.create(
            name = "1quiz",
            description = "1quiz description",
            is_private = True,
            class_profile = ClassProfile.objects.all()[1]
        )
        self.assertTrue(quiz.is_private)

    def test_create_question(self):
        question = Question.objects.create(
            prompt = "1question",
            quiz = Quiz.objects.get(pk=5)
        )
        self.assertTrue(question.prompt == "1question")

    def test_create_answer(self):
        answer = Answer.objects.create(
            description = "1answer",
            is_correct = True,
            question = Question.objects.get(pk=3)
        )
        self.assertTrue(answer.is_correct)
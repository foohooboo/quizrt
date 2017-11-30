import datetime

from django.test import TestCase, Client
from django.db import IntegrityError

from .models import User, ClassProfile, Quiz, Question, Answer
from .models import QuizResult, Response, QuizSession

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
        self.assertEqual(user.name, "valid name")
        self.assertEqual(user.email, "email@test.com")
        self.assertNotEqual(user.password, "meo12345")

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
        self.assertEqual(profile.name, "test profile")
        self.assertEqual(profile.description, "test profile description")

    def test_create_quiz(self):
        quiz = Quiz.objects.create(
            name = "1quiz",
            description = "1quiz description",
            is_private = True,
            class_profile = ClassProfile.objects.get(pk=13)
        )
        self.assertEqual(quiz.name, "1quiz")
        self.assertEqual(quiz.description, "1quiz description")
        self.assertEqual(quiz.class_profile.pk, 13)
        self.assertTrue(quiz.is_private)

    def test_create_question(self):
        question = Question.objects.create(
            prompt = "1question",
            quiz = Quiz.objects.get(pk=5)
        )
        self.assertEqual(question.quiz.pk, 5)
        self.assertEqual(question.prompt, "1question")

    def test_create_answer(self):
        answer = Answer.objects.create(
            description = "1answer",
            is_correct = True,
            question = Question.objects.get(pk=3)
        )
        self.assertEqual(answer.description, "1answer")
        self.assertEqual(answer.question.pk, 3)
        self.assertTrue(answer.is_correct)
        self.assertTrue(answer.is_correct)

    def test_create_quiz_result(self):
        today = datetime.date.today()
        quiz_result = QuizResult.objects.create(date=today)
        self.assertEqual(quiz_result.date, today)

    def test_create_quiz_result_without_date(self):
        quiz_result = QuizResult.objects.create()
        self.assertIsNotNone(quiz_result)
    
    def test_create_response(self):
        response = Response.objects.create(
            user = User.objects.get(pk=4),
            answer = Answer.objects.get(pk=16),
            quiz_result = QuizResult.objects.get(pk=1)
        )
        self.assertTrue(response.user.pk == 4)

    def test_create_quiz_session(self):
        session = QuizSession.objects.create(
            owner = User.objects.get(pk=7),
            quiz = Quiz.objects.get(pk=5),
            quiz_result = QuizResult.objects.get(pk=1)
        )
        self.assertTrue(session.quiz_result == QuizResult.objects.get(pk=1))

    def test_access_response_from_session(self):
        response_set = QuizSession.objects.get(pk=1).quiz_result.response_set.all()
        contains_response = False
        if Response.objects.get(pk=2) in response_set:
            contains_response = True
        self.assertTrue(contains_response)


    
    

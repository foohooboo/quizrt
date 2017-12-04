import datetime

from django.test import TestCase, Client
from django.db import IntegrityError

from .models import (User, ClassProfile, Quiz, Question, Answer,
                    Response, QuizSession)

class QuizrtTests(TestCase):
    fixtures = ['datadump.json']

    def test_fixture_success(self):
        self.assertTrue(User.objects.all().count() > 0)

# --------------- USER TESTS ----------------- #

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

    def test_create_user_no_username(self):
        with self.assertRaises(TypeError):
            User.objects.create_user(
                name="valid name",
                email="validtestemail@test.com",
                password="meo12345"
            )

    def test_create_user_no_name(self):
        with self.assertRaises(TypeError):
            User.objects.create_user(
                username="foohooboo",
                email="validtestemail@test.com",
                password="meo12345"
            )

    def test_create_user_short_password(self):
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                username="foohooboo",
                name="valid name",
                email="validtestemail@test.com",
                password="1"
            )

    def test_create_user_password_is_username(self):
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                username="foohooboo",
                name="valid name",
                email="validtestemail@test.com",
                password="foohooboo"
            )

    def test_create_user_password_is_name(self):
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                username="foohooboo",
                name="valid name",
                email="validtestemail@test.com",
                password="valid name"
            )

    def test_create_user_password_is_email(self):
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                username="foohooboo",
                name="valid name",
                email="validtestemail@test.com",
                password="validtestemail@test.com"
            )

    def test_create_user_duplicate_username(self):
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                username="foohooboo",
                name="valid name",
                email="validtestemail@test.com",
                password="meo12345"
            )

# --------------- PROFILE TESTS ----------------- #
    def test_create_profile(self):
        profile = ClassProfile.objects.create(
            name="test profile",
            description="test profile description",
            is_private=True
        )
        self.assertTrue(profile.is_private)
        self.assertEqual(profile.name, "test profile")
        self.assertEqual(profile.description, "test profile description")

    def test_create_profile_no_name(self):
        with self.assertRaises(TypeError):
            p = ClassProfile.objects.create(
                description = 'yolo'
            )

    def test_create_profile_no_description(self):
        with self.assertRaises(TypeError):
            p = ClassProfile.objects.create(
                name = 'yolo'
            )

    def test_profile_access_users(self):
        p = ClassProfile.objects.get(pk=10)
        u = p.user_set.all()[0]
        self.assertEqual(u.pk, 4)

    def test_profile_access_quizes(self):
        p = ClassProfile.objects.get(pk=13)
        q = p.quiz_set.all()[0]
        self.assertEqual(q.pk, 6)

# --------------- QUIZ TESTS ----------------- #
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

    def test_create_quiz_no_name(self):
        with self.assertRaises(TypeError):
            quiz = Quiz.objects.create(
                class_profile = ClassProfile.objects.get(pk=13),
                description = 'question',
            )

    def test_create_quiz_no_description(self):
        with self.assertRaises(TypeError):
            quiz = Quiz.objects.create(
                class_profile = ClassProfile.objects.get(pk=13),
                name = 'question',
            )

    def test_quiz_access_profile(self):
        q = Quiz.objects.get(pk=6)
        p = q.class_profile
        self.assertEqual(p.pk, 13)

    def test_quiz_access_questions(self):
        q = Quiz.objects.get(pk=5)
        questions = q.question_set.all()
        self.assertEqual(questions[0].pk, 5)
        self.assertEqual(questions[1].pk, 3)

# --------------- QUESTION TESTS ----------------- #
    def test_create_question(self):
        question = Question.objects.create(
            prompt = "1question",
            name = '1.1',
            quiz = Quiz.objects.get(pk=5)
        )
        self.assertEqual(question.quiz.pk, 5)
        self.assertEqual(question.prompt, "1question")
        self.assertEqual(question.name, "1.1")
        self.assertEqual(question.order_number, 0)
        self.assertEqual(question.question_duration, 30)

    def test_create_question_no_prompt(self):
        with self.assertRaises(TypeError):
            question = Question.objects.create(
                quiz = Quiz.objects.get(pk=5),
                name = 'question',
            )
    
    def test_create_question_no_name(self):
        with self.assertRaises(TypeError):
            question = Question.objects.create(
                quiz = Quiz.objects.get(pk=5),
                prompt = 'question',
            )

    def test_question_access_quiz(self):
        q = Question.objects.get(pk=3)
        quiz = q.quiz
        self.assertEqual(quiz.pk, 5)

    def test_question_access_answers(self):
        q = Question.objects.get(pk=3)
        answers = q.answer_set.all()
        self.assertEqual(answers[0].pk, 16)
        self.assertEqual(answers[1].pk, 9)

# --------------- ANSWER TESTS ----------------- #
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

    def test_create_answer_invalid_question(self):
        with self.assertRaises(Question.DoesNotExist):
            answer = Answer.objects.create(
                description = "whatever",
                is_corrent=False,
                question = Question.objects.get(pk=1000)
            )

    def test_create_answer_no_description(self):
        with self.assertRaises(TypeError):
            answer = Answer.objects.create(
                question=Question.objects.get(pk=3)
            )

    def test_answer_access_question(self):
        answer = Answer.objects.get(pk=9)
        self.assertEqual(answer.question.pk, 3)
    
# --------------- RESPONSE TESTS ----------------- #
    def test_create_response(self):
        response = Response.objects.create(
            user = User.objects.get(pk=4),
            answer = Answer.objects.get(pk=16),
            quiz_session = QuizSession.objects.get(pk=1),
            response_delay = 5,
        )
        self.assertTrue(response.user.pk == 4)

    def test_create_response_no_user(self):
        with self.assertRaises(IntegrityError):
            r = Response.objects.create(
                answer = Answer.objects.get(pk=16),
                quiz_session = QuizSession.objects.get(pk=1),
                response_delay = 5,
            )

    def test_create_response_no_answer(self):
        with self.assertRaises(IntegrityError):
            r = Response.objects.create(
                user = User.objects.get(pk=4),
                quiz_session = QuizSession.objects.get(pk=1),
                response_delay = 5,
            )
        
    def test_create_response_no_session(self):
        with self.assertRaises(Exception):
            r = Response.objects.create(
                user = User.objects.get(pk=4),
                answer = Answer.objects.get(pk=16),
                response_delay = 5,
            )

    def test_create_response_negative_delay(self):
        with self.assertRaises(Exception):
            response = Response.objects.create(
            user = User.objects.get(pk=4),
            answer = Answer.objects.get(pk=16),
            quiz_session = QuizSession.objects.get(pk=1),
            response_delay = -1
        )

    def test_create_response_for_closed_session(self):
        with self.assertRaises(Exception):
            r = Response.objects.create(
                user = User.objects.get(pk=4),
                answer = Answer.objects.get(pk=16),
                quiz_session = QuizSession.objects.get(pk=2),
                response_delay = 5,
            )

# --------------- SESSION TESTS ----------------- #
    def test_create_session(self):
        session = QuizSession.objects.create(
            owner = User.objects.get(pk=7),
            quiz = Quiz.objects.get(pk=5),
        )
        self.assertTrue(session.quiz == Quiz.objects.get(pk=5))

    def test_create_session_no_owner(self):
        with self.assertRaises(IntegrityError):
            session = QuizSession.objects.create(
                quiz = Quiz.objects.get(pk=5),
            )

    def test_create_session_no_quiz(self):
        with self.assertRaises(IntegrityError):
            session = QuizSession.objects.create(
                owner = User.objects.get(pk=4),
            )

    def test_access_response_from_session(self):
        response_set = QuizSession.objects.get(pk=1).response_set.all()
        contains_response = False
        if Response.objects.get(pk=2) in response_set:
            contains_response = True
        self.assertTrue(contains_response)


    
    

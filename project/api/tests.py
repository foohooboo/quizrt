from django.test import TestCase, Client

# Create your tests here.
from .models import User, ClassProfile, Quiz, Question, Answer

class QuizrtTests(TestCase):
    fixtures = ['quizrt_tests.json']

    def setUp(self):
        self.client = Client()

    # def test_quiz_create(self):
    #     self.client.login(
    #         username="user1@test.com", password="meo12345"
    #     )
    #     user = User.objects.get(pk=1)

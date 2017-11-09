from django.http import Http404

from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from graphene import relay, ObjectType, Mutation
from graphene.relay import Connection, ConnectionField
import graphene

from project.api.models import Quiz, ClassProfile


class QuizNode(DjangoObjectType):
    class Meta:
        model = Quiz
        filter_fields = ['description', 'id', 'is_public']
        interfaces = (relay.Node, )


class QuizInput(graphene.InputObjectType):
    description = graphene.String(required=True)
    is_public = graphene.Boolean(required=False)
    profile = graphene.String(required=True)


class CreateQuiz(relay.ClientIDMutation):
    class Input:
        quiz_data = QuizInput(required=True)

    quiz = graphene.Field(QuizNode)
    uuid = graphene.String()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        quiz = Quiz.objects.create(
            description=input['quiz_data'].description,
            is_public=input['quiz_data'].is_public,
            class_profile=ClassProfile.objects.get(uuid=input['quiz_data'].profile)
        )
        quiz.save()
        return CreateQuiz(quiz=quiz, uuid=quiz.uuid)


class Query(graphene.AbstractType):
        quizes = DjangoFilterConnectionField(QuizNode)
        quiz = relay.Node.Field(QuizNode)


class Mutation(graphene.AbstractType):
    create_quiz = CreateQuiz.Field()

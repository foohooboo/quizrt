from django.http import Http404

from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from graphene import relay, ObjectType, Mutation
from graphene.relay import Connection, ConnectionField
import graphene

from graphql_relay import from_global_id

from project.api.models import Quiz, ClassProfile


class QuizNode(DjangoObjectType):
    class Meta:
        model = Quiz
        filter_fields = ['description', 'id', 'is_public']
        interfaces = (relay.Node, )


class QuizInput(graphene.InputObjectType):
    description = graphene.String(required=True)
    is_public = graphene.Boolean(required=False)
    profile = graphene.ID(required=True)


class CreateQuiz(relay.ClientIDMutation):
    class Input:
        quiz_data = QuizInput(required=True)

    quiz = graphene.Field(QuizNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        rid = from_global_id(input['quiz_data'].profile)
        quiz = Quiz.objects.create(
            description=input['quiz_data'].description,
            is_public=input['quiz_data'].is_public,
            class_profile=ClassProfile.objects.get(pk=rid[1])
        )
        quiz.save()
        return CreateQuiz(quiz=quiz)


class DeleteQuiz(relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        rid = from_global_id(input['id'])
        try:
            quiz = Quiz.objects.get(pk=rid[1])
            quiz.delete()
            return DeleteQuiz(success=True)
        except Quiz.DoesNotExist:
            raise Exception('404 Not Found')


class UpdateQuiz(relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)
        description = graphene.String(required=False)
        is_public = graphene.Boolean(required=False)


    quiz = graphene.Field(QuizNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        rid = from_global_id(input['id'])
        # TODO: only allow modification of items owned by user
        quiz = Quiz.objects.get(pk=rid[1])
        if input['description']:
            quiz.description = input['description']
        if input['is_public']:
            quiz.is_public = input['is_public']
        quiz.save()
        return UpdateQuiz(quiz=quiz)


class Query(object):
        quizes = DjangoFilterConnectionField(QuizNode)
        quiz = relay.Node.Field(QuizNode)


class Mutation(object):
    create_quiz = CreateQuiz.Field()
    update_quiz = UpdateQuiz.Field()
    delete_quiz = DeleteQuiz.Field()

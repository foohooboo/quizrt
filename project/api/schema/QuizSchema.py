from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from graphene import relay
import graphene

from graphql_relay import from_global_id

from project.api.models import Quiz, ClassProfile


class QuizNode(DjangoObjectType):
    class Meta:
        model = Quiz
        filter_fields = {
            'name': ['exact', 'icontains'],
            'description': ['icontains'],
            'id': ['exact'],
            'is_private': ['exact']
        }

        interfaces = (relay.Node, )


class QuizInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    description = graphene.String(required=True)
    is_private = graphene.Boolean(required=False)
    profile = graphene.ID(required=True)


class CreateQuiz(relay.ClientIDMutation):
    class Input:
        quiz_data = QuizInput(required=True)

    quiz = graphene.Field(QuizNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        # TODO: only allow creation if logged in and has permissions for ClassProfile
        rid = from_global_id(input['quiz_data'].profile)
        kwargs = {
            "description": input['quiz_data'].description,
            "name": input['quiz_data'].name,
            "class_profile": ClassProfile.objects.get(pk=rid[1])
        }
        if input['quiz_data'].get('is_private'):
            kwargs['is_private'] = input['quiz_data'].get('is_private')
        quiz = Quiz.objects.create(**kwargs)
        quiz.save()
        return CreateQuiz(quiz=quiz)


class DeleteQuiz(relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        # TODO: only allow deletion if logged in and has permission on ClassProfile
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
        name = graphene.String(required=False)
        description = graphene.String(required=False)
        is_private = graphene.Boolean(required=False)

    quiz = graphene.Field(QuizNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        rid = from_global_id(input['id'])
        # TODO: only allow modification of items owned by user
        quiz = Quiz.objects.get(pk=rid[1])
        if input.get('name'):
            quiz.name = input['name']
        if input.get('description'):
            quiz.description = input['description']
        if input.get('is_private'):
            quiz.is_private = input['is_private']
        quiz.save()
        return UpdateQuiz(quiz=quiz)


class Query(object):
        quizzes = DjangoFilterConnectionField(QuizNode)
        quiz = relay.Node.Field(QuizNode)


class Mutation(object):
    create_quiz = CreateQuiz.Field()
    update_quiz = UpdateQuiz.Field()
    delete_quiz = DeleteQuiz.Field()

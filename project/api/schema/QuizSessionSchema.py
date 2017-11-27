from django.http import Http404

from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from graphene import relay, ObjectType, Mutation
from graphene.relay import Connection, ConnectionField
from graphql_relay import from_global_id
import graphene

from project.api.models import QuizSession, QuizResult, User, Quiz

class SessionNode(DjangoObjectType):
    class Meta:
        model = QuizSession
        filter_fields = ['owner', 'quiz', 'quiz_result', 'is_locked']
        interfaces = (relay.Node, )


class SessionInput(graphene.InputObjectType):
    owner = graphene.ID(required=True)
    quiz = graphene.ID(required=True)
    quiz_result = graphene.ID(required=True)


class CreateSession(relay.ClientIDMutation):
    class Input:
        session_data = SessionInput(required=True)

    session = graphene.Field(SessionNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        user_ID = from_global_id(input['session_data'].get(user)) 
        quiz_ID = from_global_id(input['session_data'].get(quiz)) 
        result_ID = from_global_id(input['session_data'].get(quiz_result)) 
        kwargs = {
            "owner": User.objects.get(pk=user_ID[1]),
            "quiz": Answer.objects.get(pk=quiz_ID[1]),
            "quiz_result": QuizResult.objects.get(pk=result_ID[1]),
        }
        session = QuizSession.objects.create(**kwargs)
        session.save()
        return CreateSession(session=session)


class DeleteSession(relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        rid = from_global_id(input['id'])
        try:
            session = QuizSession.objects.get(pk=rid[1])
            session.delete()
            return DeleteSession(success=True)
        except QuizSession.DoesNotExist:
            raise Exception('404 Not Found')


class CloseSession(relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)
        # is_locked = graphene.Boolean(required=False)

    session = graphene.Field(SessionNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        rid = from_global_id(input['id'])
        session = QuizSession.objects.get(pk=rid[1])
        # if(input['is_locked']):
        #     session.is_locked = input['is_locked']
        session.is_locked = True
        session.save()
        return UpdateSession(session=session)


class Query(object):
    sessions = DjangoFilterConnectionField(SessionNode)
    session = relay.Node.Field(SessionNode)


class Mutation(object):
    create_session = CreateSession.Field()
    delete_session = DeleteSession.Field()
    close_session = CloseSession.Field()
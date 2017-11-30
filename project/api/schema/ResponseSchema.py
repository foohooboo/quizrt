from django.http import Http404

from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from graphene import relay, ObjectType, Mutation
from graphene.relay import Connection, ConnectionField
from graphql_relay import from_global_id
import graphene

from project.api.models import User, Answer, Response, QuizSession

class ResponseNode(DjangoObjectType):
    class Meta:
        model = Response
        filter_fields = {
            'user': ['exact'],
            'answer': ['exact'],
            'id': ['exact'],
            'quiz_session': ['exact'],
            'question': ['exact']
        }
        interfaces = (relay.Node, )


# class ResponseInput(graphene.InputObjectType):
#     user = graphene.ID(required=True)
#     answer = graphene.ID(required=True)
#     quiz_session = graphene.ID(required=True)
#     response_delay = graphene.Int(required=True)

class CreateResponse(relay.ClientIDMutation):
    class Input:
        # response_data = ResponseInput(required=True)
        user = graphene.ID(required=True)
        answer = graphene.ID(required=True)
        quiz_session = graphene.ID(required=True)
        response_delay = graphene.Int(required=False)

    response = graphene.Field(ResponseNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        user_ID = from_global_id(input.get('user')) 
        answer_ID = from_global_id(input.get('answer')) 
        session_ID = from_global_id(input.get('quiz_session')) 
        kwargs = {
            "user": User.objects.get(pk=user_ID[1]),
            "answer": Answer.objects.get(pk=answer_ID[1]),
            "quiz_session": QuizSession.objects.get(pk=session_ID[1]),
            "response_delay": input.get('response_delay')
        }
        if(QuizSession.objects.get(pk=session_ID[1]).is_locked):
            raise Exception('403 Forbidden')
        else:
            response = Response.objects.create(**kwargs)
            response.save()
            return CreateResponse(response=response)


class DeleteResponse(relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        rid = from_global_id(input.get('id'))
        try:
            response = Response.objects.get(pk=rid[1])
            response.delete()
            return DeleteResponse(success=True)
        except Response.DoesNotExist:
            raise Exception('404 Not Found')


# Deleted the UpdateResponse as well.  Kinda don't think it should be a thing


class Query(object):
    responses = DjangoFilterConnectionField(ResponseNode)
    response = relay.Node.Field(ResponseNode)


class Mutation(object):
    create_response = CreateResponse.Field()
    delete_response = DeleteResponse.Field()
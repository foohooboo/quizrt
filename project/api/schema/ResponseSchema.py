from django.http import Http404

from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from graphene import relay, ObjectType, Mutation
from graphene.relay import Connection, ConnectionField
from graphql_relay import from_global_id
import graphene

from project.api.models import User, Answer, Response, QuizResult

class ResponseNode(DjangoObjectType):
    class Meta:
        model = Response
        filter_fields = {
            'user': ['exact'],
            'answer': ['exact'],
            'id': ['exact'],
            'quiz_result': ['exact']
        }
        interfaces = (relay.Node, )


class ResponseInput(graphene.InputObjectType):
    user = graphene.ID(required=True)
    answer = graphene.ID(required=True)
    quiz_result = graphene.ID(required=True)

class CreateResponse(relay.ClientIDMutation):
    class Input:
        response_data = ResponseInput(required=True)

    response = graphene.Field(ResponseNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        user_ID = from_global_id(input['response_data'].get(user)) 
        answer_ID = from_global_id(input['response_data'].get(answer)) 
        result_ID = from_global_id(input['response_data'].get(quiz_result)) 
        kwargs = {
            "user": User.objects.get(pk=user_ID[1]),
            "answer": Answer.objects.get(pk=answer_ID[1]),
            "quiz_result": QuizResult.objects.get(pk=result_ID[1]),
        }
        response = Response.objects.create(**kwargs)
        response.save()
        return CreateResponse(response=response)


class DeleteResponse(relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        rid = from_global_id(input['id'])
        try:
            response = Response.objects.get(pk=rid[1])
            response.delete()
            return DeleteResponse(success=True)
        except Response.DoesNotExist:
            raise Exception('404 Not Found')

# Belaying this mutation.  Kinda don't think it should be a thing
# class UpdateResponse(relay.ClientIDMutation):
#     class Input:
#         id = graphene.ID(required=True)


class Query(object):
    responses = DjangoFilterConnectionField(ResponseNode)
    response = relay.Node.Field(ResponseNode)


class Mutation(object):
    create_response = CreateResponse.Field()
    delete_response = DeleteResponse.Field()
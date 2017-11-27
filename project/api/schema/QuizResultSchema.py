from django.http import Http404

from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from graphene import relay, ObjectType, Mutation
from graphene.relay import Connection, ConnectionField
from graphql_relay import from_global_id
import graphene

from project.api.models import QuizResult, Response

def add_responses_to_result(result, response_ids):
    rids = list(map(from_global_id, response_ids))
    responses = Response.objects.filter(pk__in=[i[1] for i in rids])
    for r in responses:
        r.quiz_result = result
        r.save()

class ResultNode(DjangoObjectType):
    class Meta:
        model = QuizResult
        filter_fields = {
            'date': ['exact', 'icontains'],
        }
        interfaces = (relay.Node, )

class CreateResult(relay.ClientIDMutation):
    class Input:
        response_list = graphene.List(graphene.ID, required=True)
        date = graphene.types.datetime.DateTime(required=True)

    result = graphene.Field(ResultNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        kwargs = {
            "date": input['date']
        }
        result = QuizResult.objects.create(**kwargs)
        result.save()
        add_responses_to_result(result, input.get('response_list'))
        return CreateResult(result=result)


class Query(object):
    results = DjangoFilterConnectionField(ResultNode)
    result = relay.Node.Field(ResultNode)


class Mutation(object):
    create_result = CreateResult.Field()
from django.http import Http404

from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from graphene import relay, ObjectType, Mutation
from graphene.relay import Connection, ConnectionField
import graphene

from project.api.models import Answer


class AnswerNode(DjangoObjectType):
    class Meta:
        model = Answer
        filter_fields = ['description', 'question', 'is_correct', 'id']
        interfaces = (relay.Node, )


class Query(graphene.AbstractType):
        answers = DjangoFilterConnectionField(AnswerNode)
        answer = relay.Node.Field(AnswerNode)

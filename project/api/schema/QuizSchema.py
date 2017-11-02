from django.http import Http404

from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from graphene import relay, ObjectType, Mutation
from graphene.relay import Connection, ConnectionField
import graphene

from project.api.models import Quiz


class QuizNode(DjangoObjectType):
    class Meta:
        model = Quiz
        filter_fields = ['description', 'id', 'is_public']
        interfaces = (relay.Node, )


class Query(graphene.AbstractType):
        quizes = DjangoFilterConnectionField(QuizNode)
        quiz = relay.Node.Field(QuizNode)

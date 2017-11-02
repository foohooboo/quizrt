from django.http import Http404

from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from graphene import relay, ObjectType, Mutation
from graphene.relay import Connection, ConnectionField
import graphene

from project.api.models import Question


class QuestionNode(DjangoObjectType):
    class Meta:
        model = Question
        filter_fields = ['prompt', 'id', 'quiz']
        interfaces = (relay.Node, )


class Query(graphene.AbstractType):
        questions = DjangoFilterConnectionField(QuestionNode)
        question = relay.Node.Field(QuestionNode)

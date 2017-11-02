from django.http import Http404

from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from graphene import relay, ObjectType, Mutation
from graphene.relay import Connection, ConnectionField
import graphene

from project.api.models import ClassProfile


class ClassProfileNode(DjangoObjectType):
    class Meta:
        model = ClassProfile
        filter_fields = ['description', 'id']
        interfaces = (relay.Node, )


class Query(graphene.AbstractType):
        classes = DjangoFilterConnectionField(ClassProfileNode)
        profileClass = relay.Node.Field(ClassProfileNode)

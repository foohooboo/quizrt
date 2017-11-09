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


class ProfileInput(graphene.InputObjectType):
    description = graphene.String(required=True)
    is_public = graphene.Boolean(required=False)


class CreateProfile(relay.ClientIDMutation):
    class Input:
        profile_data = ProfileInput(required=True)

    profile = graphene.Field(ClassProfileNode)
    uuid = graphene.String()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        profile = ClassProfile.objects.create(
            description=input['profile_data'].description,
            is_public=input['profile_data'].is_public
        )
        profile.save()
        return CreateProfile(profile=profile, uuid=profile.uuid)


class UpdateClassProfile(relay.ClientIDMutation):
    class Input:
        uuid = graphene.String(required=True)
        description = graphene.String(required=False)
        is_public = graphene.Boolean(required=False)


    profile = graphene.Field(ClassProfileNode)
    uuid = graphene.String()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        # TODO: only allow modification of items owned by user
        profile = ClassProfile.objects.get(uuid=input['uuid'])
        if input['description']:
            profile.description = input['description']
        if input['is_public']:
            profile.is_public = input['is_public']
        profile.save()
        return UpdateClassProfile(profile=profile, uuid=profile.uuid)


class Query(graphene.AbstractType):
        classes = DjangoFilterConnectionField(ClassProfileNode)
        profileClass = relay.Node.Field(ClassProfileNode)


class Mutation(graphene.AbstractType):
    create_Profile = CreateProfile.Field()
    update_Profile = UpdateClassProfile.Field()

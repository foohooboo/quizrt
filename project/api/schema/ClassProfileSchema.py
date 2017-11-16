from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from graphene import relay
import graphene

from graphql_relay import from_global_id

from project.api.models import ClassProfile


class ClassProfileNode(DjangoObjectType):
    class Meta:
        model = ClassProfile
        filter_fields = {
            'description': ['icontains'],
            'id': ['exact'],
        }
        interfaces = (relay.Node, )


class ProfileInput(graphene.InputObjectType):
    description = graphene.String(required=True)
    is_public = graphene.Boolean(required=False)


class CreateProfile(relay.ClientIDMutation):
    class Input:
        profile_data = ProfileInput(required=True)

    profile = graphene.Field(ClassProfileNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        kwargs = {
            "description": input['profile_data'].description
        }
        if input['profile_data'].get('is_public'):
            kwargs['is_public'] = input['profile_data'].is_public
        profile = ClassProfile.objects.create(
            **kwargs
        )
        profile.save()
        return CreateProfile(profile=profile)


class DeleteClassProfile(relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        rid = from_global_id(input['id'])
        try:
            profile = ClassProfile.objects.get(pk=rid[1])
            profile.delete()
            return DeleteClassProfile(success=True)
        except ClassProfile.DoesNotExist:
            raise Exception('404 Not Found')


class UpdateClassProfile(relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)
        description = graphene.String(required=False)
        is_public = graphene.Boolean(required=False)


    profile = graphene.Field(ClassProfileNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        rid = from_global_id(input['id'])
        # TODO: only allow modification of items owned by user
        profile = ClassProfile.objects.get(pk=rid[1])
        if input.get('description'):
            profile.description = input['description']
        if input.get('is_public'):
            profile.is_public = input['is_public']
        profile.save()
        return UpdateClassProfile(profile=profile)


class Query(object):
        classes = DjangoFilterConnectionField(ClassProfileNode)
        profileClass = relay.Node.Field(ClassProfileNode)


class Mutation(object):
    create_profile = CreateProfile.Field()
    update_profile = UpdateClassProfile.Field()
    delete_profile = DeleteClassProfile.Field()

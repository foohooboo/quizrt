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
            'name': ['exact', 'icontains'],
            'id': ['exact'],
        }
        interfaces = (relay.Node, )


class ProfileInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    description = graphene.String(required=True)
    is_private = graphene.Boolean(required=False)


class CreateProfile(relay.ClientIDMutation):
    class Input:
        profile_data = ProfileInput(required=True)

    profile = graphene.Field(ClassProfileNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        kwargs = {
            "description": input['profile_data'].description,
            "name": input['profile_data'].name
        }
        if input['profile_data'].get('is_private'):
            kwargs['is_private'] = input['profile_data'].is_private
        profile = ClassProfile.objects.create( **kwargs )
        profile.save()

        current_user = info.context.user

        if current_user.is_authenticated():
            current_user.class_profiles.add(profile)
            current_user.save()

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
        is_private = graphene.Boolean(required=False)


    profile = graphene.Field(ClassProfileNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        rid = from_global_id(input['id'])
        # TODO: only allow modification of items owned by user
        profile = ClassProfile.objects.get(pk=rid[1])
        if input.get('description'):
            profile.description = input['description']
        if input.get('is_private'):
            profile.is_private = input['is_private']
        profile.save()
        return UpdateClassProfile(profile=profile)


class Query(object):
        profiles = DjangoFilterConnectionField(ClassProfileNode)
        profile = relay.Node.Field(ClassProfileNode)


class Mutation(object):
    create_profile = CreateProfile.Field()
    update_profile = UpdateClassProfile.Field()
    delete_profile = DeleteClassProfile.Field()

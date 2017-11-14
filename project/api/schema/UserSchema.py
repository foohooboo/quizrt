from django.http import Http404

from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from graphene import relay, ObjectType, Mutation
from graphene.relay import Connection, ConnectionField
import graphene

from project.api.models import User, ClassProfile
# from .ClassProfileSchema import ClassProfileNode

# class ProfilesConnection(Connection):
#     class Meta:
#         node = ClassProfileNode


class UserNode(DjangoObjectType):
    class Meta:
        model = User
        filter_fields = ['username', 'email', 'id']
        exclude_fields = ('is_superuser', 'password')
        interfaces = (relay.Node, )


class UserInput(graphene.InputObjectType):
    username = graphene.String(required=True)
    name = graphene.String(required=True)
    email = graphene.String(required=True)
    password = graphene.String(required=True)


class CreateUser(relay.ClientIDMutation):
    class Input:
        user_data = UserInput(required=True)

    user = graphene.Field(UserNode)
    uuid = graphene.String()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        user = User.objects.create_user(
            username=input['user_data'].username,
            name=input['user_data'].name,
            email=input['user_data'].email,
            password=input['user_data'].password
        )
        return CreateUser(user=user, uuid=user.uuid)


class DeleteUser(relay.ClientIDMutation):
    class Input:
        uuid = graphene.String()


    ok = graphene.Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        current_user = info.context.user
        if current_user.is_authenticated():
            if current_user.is_superuser or input['uuid'] == current_user.uuid:
                try:
                    User.objects.get(uuid=input['uuid']).delete()
                    return DeleteUser(ok=True)
                except User.DoesNotExist:
                    return DeleteUser(ok=False)


class UpdateUser(relay.ClientIDMutation):
    class Input:
        user_data = UserInput(required=True)

    user = graphene.Field(UserNode)
    uuid = graphene.String()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        current_user = info.context.user
        if current_user.is_authenticated():
            # TODO: Add functionality that allows superusers to edit other users
            if input['user_data'].username:
                current_user.username = input['user_data'].username
            if input['user_data'].name:
                current_user.name = input['user_data'].name
            if input['user_data'].email:
                current_user.email = input['user_data'].email
            # TODO:  Add password change functionality
        else:
            raise Http404
        current_user.save()
        return UpdateUser(user=current_user, uuid=current_user.uuid)


class Query(graphene.AbstractType):
    user = relay.Node.Field(UserNode)
    users = DjangoFilterConnectionField(UserNode)


class Mutation(graphene.AbstractType):
    create_user = CreateUser.Field()
    delete_user = DeleteUser.Field()
    update_user = UpdateUser.Field()

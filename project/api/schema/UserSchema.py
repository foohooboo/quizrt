from django.http import Http404

from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from project.api.models import User, ClassProfile, Quiz, Question, Answer
from graphene import relay, ObjectType, Mutation
from graphene.relay import Connection, ConnectionField
import graphene

class ClassProfileNode(DjangoObjectType):
    class Meta:
        model = ClassProfile
        filter_fields = ['description', 'id']
        interfaces = (relay.Node, )


class ProfilesConnection(Connection):
    class Meta:
        node = ClassProfileNode


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
    id = graphene.Int()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        user = User.objects.create_user(
            username=input['user_data'].username,
            name=input['user_data'].name,
            email=input['user_data'].email,
            password=input['user_data'].password
        )
        return CreateUser(user=user, id=user.id)


class DeleteUser(relay.ClientIDMutation):
    class Input:
        user_data = UserInput(required=True)

    user_deleted = graphene.String()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        input_username = input['user_data'].username
        if not input_username:
            raise Http404
        current_user = info.context.user
        if current_user.is_authenticated():
            if current_user.is_superuser:
                User.objects.filter(username=input_username).delete()
            elif input_username == current_user.username:
                User.objects.filter(username=input_username.username).delete()
            else:
                raise Http404
            return DeleteUser(user_deleted=input_username.username)


class UpdateUser(relay.ClientIDMutation):
    class Input:
        user_data = UserInput(required=True)

    user = graphene.Field(UserNode)
    id = graphene.Int()

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
        return UpdateUser(user=current_user, id=current_user.id)


class Query(object):
    user = relay.Node.Field(UserNode)
    users = DjangoFilterConnectionField(UserNode)

    profileClass = relay.Node.Field(ClassProfileNode)
    classes = DjangoFilterConnectionField(ClassProfileNode)


class Mutation(object):
    create_user = CreateUser.Field()
    delete_user = DeleteUser.Field()
    update_user = UpdateUser.Field()

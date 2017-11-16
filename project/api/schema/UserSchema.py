from django.http import Http404
from django.contrib.auth import authenticate, login, logout

from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from graphene import relay, ObjectType, Mutation
from graphene.relay import Connection, ConnectionField
import graphene

from graphql_relay import from_global_id

from project.api.models import User, ClassProfile
# from .ClassProfileSchema import ClassProfileNode

# class ProfilesConnection(Connection):
#     class Meta:
#         node = ClassProfileNode


class UserNode(DjangoObjectType):
    class Meta:
        model = User
        filter_fields = {
            'name': ['exact', 'icontains'],
            'username': ['exact', 'icontains'],
            'email': ['exact']
        }
        exclude_fields = ('is_superuser', 'password')
        interfaces = (relay.Node, )


class UserInput(graphene.InputObjectType):
    username = graphene.String(required=False)
    name = graphene.String(required=True)
    email = graphene.String(required=True)
    password = graphene.String(required=True)


class CreateUser(relay.ClientIDMutation):
    class Input:
        user_data = UserInput(required=True)

    user = graphene.Field(UserNode)
    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        username = (input['user_data'].username
                    if input['user_data'].username is not None
                    else input['user_data'].email)
        user = User.objects.create_user(
            username=username,
            name=input['user_data'].name,
            email=input['user_data'].email,
            password=input['user_data'].password
        )
        return CreateUser(user=user)


class DeleteUser(relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)


    success = graphene.Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        rid = from_global_id(input['id'])
        current_user = info.context.user
        if current_user.is_authenticated():
            if rid[1] == current_user.id:
                try:
                    User.objects.get(pk=rid[1]).delete()
                    return DeleteUser(success=True)
                except User.DoesNotExist:
                    raise Exception('404 Not Found')
            raise Exception('403 Forbidden')
        raise Exception('401 Unauthorized')


class UpdateUser(relay.ClientIDMutation):
    class Input:
        user_data = UserInput(required=True)

    user = graphene.Field(UserNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        rid = from_global_id(input['id'])
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
            raise Exception('403 Forbidden')
        current_user.save()
        return UpdateUser(user=current_user)


class LoginUser(relay.ClientIDMutation):
    class Input:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    user = graphene.Field(UserNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        email = input['email']
        password = input['password']
        # check login with email
        user = authenticate(info.context, email=email, password=password)
        if user != None:
            login(info.context, user)
            return LoginUser(user=user)
        else:
            raise Exception('401 Unauthorized')


class LogoutUser(relay.ClientIDMutation):
    
    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        logout(info.context)
        return LogoutUser()


class Query(object):
    user = relay.Node.Field(UserNode)
    users = DjangoFilterConnectionField(UserNode)


class Mutation(object):
    login_user = LoginUser.Field()
    logout_user = LogoutUser.Field()
    create_user = CreateUser.Field()
    delete_user = DeleteUser.Field()
    update_user = UpdateUser.Field()

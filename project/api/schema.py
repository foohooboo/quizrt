from graphene_django import DjangoObjectType
from .models import BaseUser
import graphene


class User(DjangoObjectType):
    class Meta:
        model = BaseUser

class UserInput(graphene.InputObjectType):
    username = graphene.String(required=True)
    first_name = graphene.String(required=True)
    last_name = graphene.String(required=True)
    email = graphene.String(required=True)
    password = graphene.String(required=True)


class CreateUser(graphene.Mutation):
    class Arguments:
        user_data = UserInput(required=True)

    user = graphene.Field(User)
    id = graphene.Int()

    @staticmethod
    def mutate(root, info, user_data=None):
        user = BaseUser.objects.create_user(
            username=user_data.username,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            email=user_data.email,
            password=user_data.password
        )
        return CreateUser(user=user, id=user.id)

class Query(graphene.ObjectType):
    users = graphene.List(User)

    user = graphene.Field(User,
        id=graphene.Int(),
        username=graphene.String(),
        first_name=graphene.String(),
        last_name=graphene.String(),
        email=graphene.String())

    @graphene.resolve_only_args
    def resolve_users(self):
        return BaseUser.objects.all()

    @graphene.resolve_only_args
    def resolve_user(self, **kwargs):
        id = kwargs.get('id')
        username = kwargs.get('username')
        email = kwargs.get('email')

        if id is not None:
            return BaseUser.objects.get(pk=id)

        if username is not None:
            return BaseUser.objects.get(username=username)

        if email is not None:
            return BaseUser.objects.get(email=email)

        return None


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)

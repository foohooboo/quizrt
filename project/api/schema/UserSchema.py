from django.contrib.auth import authenticate, login, logout

from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from graphene import relay
import graphene

from graphql_relay import from_global_id

from project.api.models import User, ClassProfile
# from .ClassProfileSchema import ClassProfileNode

# class ProfilesConnection(Connection):
#     class Meta:
#         node = ClassProfileNode

def add_profiles_to_user(user, prof_ids):
    rids = list(map(from_global_id, prof_ids))
    profiles = ClassProfile.objects.filter(pk__in=[i[1] for i in rids])
    user.class_profiles.set(profiles.all())


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


class CreateUser(relay.ClientIDMutation):
    class Input:
        username = graphene.String(required=False)
        profile_list = graphene.List(graphene.ID, required=False)
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    user = graphene.Field(UserNode)
    
    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        username = (input.get('username')
                    if input.get('username') is not None
                    else input.get('email'))
        user = User.objects.create_user(
            username=username,
            name=input.get('name'),
            email=input.get('email'),
            password=input.get('password')
        )
        if input.get('profile_list'):
            add_profiles_to_user(user, input.get('profile_list'))
            user.save()
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
        id = graphene.ID(required=True)
        # we exracted the fields from UserInput because we need to specify these
        # fields as optional (required=False) - I don't think there's a way to do this in graphene
        # but if these were typescript types, we could do something like user_input = Partial<UserInput>
        # which would change all of the fields to be nullable
        username = graphene.String(required=False)
        profile_list = graphene.List(graphene.ID, required=False)
        name = graphene.String(required=False)
        email = graphene.String(required=False)
        password = graphene.String(required=False)

    user = graphene.Field(UserNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        rid = from_global_id(input['id'])
        current_user = info.context.user
        if current_user.is_authenticated():
            if input.get('username'):
                current_user.username = input.get('username')
            if input.get('name'):
                current_user.name = input.get('name')
            if input.get('email'):
                current_user.email = input.get('email')
            if input.get('profile_list'):
                add_profiles_to_user(current_user, input.get('profile_list'))
            # TODO:  Add password change functionality
        else:
            raise Exception('403 Forbidden')
        current_user.save()
        return UpdateUser(user=current_user)


class LoginUser(relay.ClientIDMutation):
    class Input:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    user = graphene.Field(UserNode, required=True)

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

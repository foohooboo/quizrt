import graphene
from . import UserSchema

class Query(UserSchema.Query, graphene.ObjectType):
    pass

class Mutation(UserSchema.Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)

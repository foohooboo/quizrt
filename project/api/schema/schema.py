import graphene
from . import UserSchema, AnswerSchema, ClassProfileSchema, QuestionSchema, QuizSchema

class Query(UserSchema.Query, graphene.ObjectType):
    pass

class Mutation(UserSchema.Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)

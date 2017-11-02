import graphene
from . import UserSchema, AnswerSchema, ClassProfileSchema, QuestionSchema, QuizSchema

class Query(UserSchema.Query,
            ClassProfileSchema.Query,
            QuizSchema.Query,
            QuestionSchema.Query,
            AnswerSchema.Query,
            graphene.ObjectType):
    pass

class Mutation(UserSchema.Mutation,
               ClassProfileSchema.Mutation,
               QuizSchema.Mutation,
               QuestionSchema.Mutation,
               AnswerSchema.Mutation,
               graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)

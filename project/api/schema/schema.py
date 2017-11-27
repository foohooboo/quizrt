import graphene
from . import (UserSchema, 
               AnswerSchema, 
               ClassProfileSchema, 
               QuestionSchema, 
               QuizSchema,
               ResponseSchema,
               QuizSessionSchema,
               QuizResultSchema,
              )

class Query(UserSchema.Query,
            ClassProfileSchema.Query,
            QuizSchema.Query,
            QuestionSchema.Query,
            AnswerSchema.Query,
            ResponseSchema.Query,
            QuizSessionSchema.Query,
            QuizResultSchema.Query,
            graphene.ObjectType):
    pass

class Mutation(UserSchema.Mutation,
               ClassProfileSchema.Mutation,
               QuizSchema.Mutation,
               QuestionSchema.Mutation,
               AnswerSchema.Mutation,
               ResponseSchema.Mutation,
               QuizSessionSchema.Mutation, 
               QuizResultSchema.Mutation,              
               graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)

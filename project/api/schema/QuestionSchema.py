from django.http import Http404

from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from graphene import relay, ObjectType, Mutation
from graphene.relay import Connection, ConnectionField
import graphene

from project.api.models import Question, Quiz


class QuestionNode(DjangoObjectType):
    class Meta:
        model = Question
        filter_fields = ['prompt', 'id', 'quiz']
        interfaces = (relay.Node, )


class QuestionInput(graphene.InputObjectType):
    prompt = graphene.String(required=True)
    quiz = graphene.Int(required=True)


class CreateQuestion(relay.ClientIDMutation):
    class Input:
        question_data = QuestionInput(required=True)

    question = graphene.Field(QuestionNode)
    id = graphene.Int()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        question = Question.objects.create(
            prompt=input['question_data'].prompt,
            quiz=Quiz.objects.get(id=input['question_data'].quiz)
        )
        question.save()
        return CreateQuestion(question=question, id=question.id)


class Query(graphene.AbstractType):
        questions = DjangoFilterConnectionField(QuestionNode)
        question = relay.Node.Field(QuestionNode)


class Mutation(graphene.AbstractType):
    create_question = CreateQuestion.Field()

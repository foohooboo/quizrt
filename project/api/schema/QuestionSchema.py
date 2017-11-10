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
    quiz = graphene.String(required=True)


class CreateQuestion(relay.ClientIDMutation):
    class Input:
        question_data = QuestionInput(required=True)

    question = graphene.Field(QuestionNode)
    uuid = graphene.String()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        question = Question.objects.create(
            prompt=input['question_data'].prompt,
            quiz=Quiz.objects.get(uuid=input['question_data'].quiz)
        )
        question.save()
        return CreateQuestion(question=question, uuid=question.uuid)


class DeleteQuestion(relay.ClientIDMutation):
    class Input:
        uuid = graphene.String(required=True)


    ok = graphene.Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        try:
            question = Question.objects.get(uuid=input['uuid'])
            question.delete()
            return DeleteQuestion(ok=True)
        except Question.DoesNotExist:
            return DeleteQuestion(ok=False)


class UpdateQuestion(relay.ClientIDMutation):
    class Input:
        uuid = graphene.String(required=True)
        prompt = graphene.String(required=False)


    question = graphene.Field(QuestionNode)
    uuid = graphene.String()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        # TODO: only allow modification of items owned by user
        question = Question.objects.get(uuid=input['uuid'])
        if input['prompt']:
            question.prompt = input['prompt']
        question.save()
        return UpdateQuestion(question=question, uuid=question.uuid)


class Query(graphene.AbstractType):
        questions = DjangoFilterConnectionField(QuestionNode)
        question = relay.Node.Field(QuestionNode)


class Mutation(graphene.AbstractType):
    create_question = CreateQuestion.Field()
    update_question = UpdateQuestion.Field()
    delete_question = DeleteQuestion.Field(0)

from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from graphene import relay
import graphene

from graphql_relay import from_global_id

from project.api.models import Answer, Question


class AnswerNode(DjangoObjectType):
    class Meta:
        model = Answer
        filter_fields = {
            'description': ['icontains'],
            'question': ['exact'],
            'is_correct': ['exact'],
            'id': ['exact']
        }
        interfaces = (relay.Node, )


class AnswerInput(graphene.InputObjectType):
    description = graphene.String(required=True)
    question = graphene.ID(required=True)
    is_correct = graphene.Boolean(required=True)


class CreateAnswer(relay.ClientIDMutation):
    class Input:
        answer_data = AnswerInput(required=True)

    answer = graphene.Field(AnswerNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        print(input['answer_data'])
        rid = from_global_id(input['answer_data'].get('question'))
        answer = Answer.objects.create(
            description=input['answer_data'].get('description'),
            is_correct=input['answer_data'].get('is_correct'),
            question=Question.objects.get(pk=rid[1])
        )
        return CreateAnswer(answer=answer)


class DeleteAnswer(relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        rid = from_global_id(input.get('id'))
        try:
            answer = Answer.objects.get(pk=rid[1])
            answer.delete()
            return DeleteAnswer(success=True)
        except Answer.DoesNotExist:
            raise Exception('404 Not Found')


class UpdateAnswer(relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)
        description = graphene.String(required=False)
        is_correct = graphene.Boolean(required=False)

    answer = graphene.Field(AnswerNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        rid = from_global_id(input.get('id'))
        # TODO: only allow modification of items owned by user
        answer = Answer.objects.get(pk=rid[1])
        if input.get('description'):
            answer.description = input['description']
        if input.get('is_correct') is not None:
            answer.is_correct = input['is_correct']
        answer.save()
        return UpdateAnswer(answer=answer)


class Query(object):
        answers = DjangoFilterConnectionField(AnswerNode)
        answer = relay.Node.Field(AnswerNode)


class Mutation(object):
    create_answer = CreateAnswer.Field()
    update_answer = UpdateAnswer.Field()
    delete_answer = DeleteAnswer.Field()

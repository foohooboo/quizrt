from django.http import Http404

from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from graphene import relay, ObjectType, Mutation
from graphene.relay import Connection, ConnectionField
from graphql_relay import from_global_id
import graphene

from project.api.models import Question, Quiz


class QuestionNode(DjangoObjectType):
    class Meta:
        model = Question
        filter_fields = {
            'prompt': ['exact', 'icontains'],
            'id': ['exact'],
            'quiz': ['exact'],
            'name': ['exact', 'icontains']
        }
        interfaces = (relay.Node, )


class CreateQuestion(relay.ClientIDMutation):
    class Input:
        # question_data = QuestionInput(required=True)
        prompt = graphene.String(required=True)
        name = graphene.String(required=True)
        quiz = graphene.ID(required=True)
        order_number = graphene.Int(required=False)
        question_duration = graphene.Int(required=False)
        

    question = graphene.Field(QuestionNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        rid = from_global_id(input.get('quiz'))
        
        kwargs = {
            'prompt': input.get('prompt'),
            'name': input.get('name'),
            'quiz': Quiz.objects.get(pk=rid[1])
        }
        if(input.get('order_number')):
            kwargs['order_number'] = input['order_number']
        if(input.get('question_duration')):
            kwargs['question_duration'] = input['question_duration']
        question = Question.objects.create(**kwargs)
        # question = Question.objects.create(
        #     prompt=input['question_data'].get('prompt'),
        #     name=input['question_data'].get('name'),
        #     quiz=Quiz.objects.get(pk=rid[1]))
        question.save()
        return CreateQuestion(question=question)


class DeleteQuestion(relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        rid = from_global_id(input.get('id'))
        try:
            question = Question.objects.get(pk=rid[1])
            question.delete()
            return DeleteQuestion(success=True)
        except Question.DoesNotExist:
            raise Exception('404 Not Found')


class UpdateQuestion(relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)
        prompt = graphene.String(required=False)
        name = graphene.String(required=False)
        order_number = graphene.Int(required=False)
        question_duration = graphene.Int(required=False)

    question = graphene.Field(QuestionNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        rid = from_global_id(input.get('id'))
        # TODO: only allow modification of items owned by user
        question = Question.objects.get(pk=rid[1])
        if input.get('prompt'):
            question.prompt = input['prompt']
        if input.get('name'):
            question.name = input['name']
        if input.get('order_number'):
            question.order_number = input['order_number']
        if input.get('question_duration'):
            question.question_duration = input['question_duration']
        question.save()
        return UpdateQuestion(question=question)


class Query(object):
    questions = DjangoFilterConnectionField(QuestionNode)
    question = relay.Node.Field(QuestionNode)


class Mutation(object):
    create_question = CreateQuestion.Field()
    update_question = UpdateQuestion.Field()
    delete_question = DeleteQuestion.Field(0)

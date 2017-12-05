import datetime
import json

from django.test import TestCase, Client
from django.db import IntegrityError

from graphene.test import Client
from graphql_relay import from_global_id

from .schema import schema

from .models import (User, ClassProfile, Quiz, Question, Answer,
                     Response, QuizSession)

class ApiTests(TestCase):
    fixtures = ['datadump.json']

    def get_user_ids(self):
        query = '''
        query getUIDS{
            users{edges{node{
                id
            }}}
        }
        '''
        uids = []
        result = schema.execute(query).data
        users = result['users'].get('edges')
        for user in users:
            uids.append(user['node']['id'])
        return uids

    def setup(self):
        pass

    def test_db_setup_success(self):
        self.assertTrue(User.objects.all().count() > 0)

    def test_query_first_user(self):
        query = '''
        query FirstUserQuery {
            users(first: 1){
                edges{
                    node{
                        username
                        name
                        email
                    }
                }
            }
        }
        '''
        expected = {
            'users': {
                'edges': [
                    {
                        'node': {
                            'username': 'foohooboo',
                            'name': 'Daniel Evans',
                            'email': 'foohooboo@test.com'
                        }
                    }
                ]
            }
        }
        result = schema.execute(query)
        assert not result.errors
        self.assertEqual(result.data, expected)

    def test_create_user(self):
        mutation = '''
        mutation NewUser{
            createUser(input: {
                name: "billy",
                username: "thorton",
                email: "billy@test.com",
                password: "meo12345"
            }){
                user{
                    name
                    username
                    email
                    classProfiles{
                        edges{
                            node{
                                id
                                name
                                description
                            }
                        }
                    }
                    quizsessionSet{
                        edges{
                            node{
                                owner{
                                    username
                                }
                                quiz{
                                    name
                                }
                            }
                        }
                    }
                }
            }
        }
        '''
        expected = {
            'createUser': {
                'user': {
                    'name': 'billy',
                    'username': 'thorton',
                    'email': 'billy@test.com',
                    'classProfiles': {
                        'edges': []
                    },
                    'quizsessionSet': {
                        'edges': []
                    }
                }
            }
        }
        result = schema.execute(mutation)
        assert not result.errors
        self.assertEqual(result.data, expected)

    # def test_create_profile(self):
    #     # uids = self.get_user_ids()

    #     mutation = '''
    #     mutation newProfile{
    #         createProfile(input:{profileData:{
    #             name: "yolo profile",
    #             description: "holla of test profile",
    #             isPrivate: false
    #         }}){
    #             profile{
    #                 name
    #                 description
    #                 isPrivate
    #             }
    #         }
    #     }
    #     '''
    #     expected = {
    #         'createProfile': {
    #             'profile':{
    #                 'name': 'test profile',
    #                 'description': 'description of test profile',
    #                 'isPrivate': 'false',
    #             }
    #         }
    #     }
    #     result = schema.execute(mutation)
    #     print(result.errors)
    #     assert not result.errors
    #     self.assertEqual(result.data, expected)

from django.conf.urls import url, include
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    url(r'^graphql', csrf_exempt(GraphQLView.as_view(graphiql=True)))
]

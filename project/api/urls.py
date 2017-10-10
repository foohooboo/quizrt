from django.conf.urls import url, include
from graphene_django.views import GraphQLView

urlpatterns = [
    url(r'^graphql', GraphQLView.as_view(graphiql=True))
]

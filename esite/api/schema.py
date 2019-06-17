# typings
from typing import Any  # noqa
# django
from django.utils.text import camel_case_to_spaces
# graphql
from graphql import ResolveInfo
# graphene
import graphene
# graphene_django
from graphene_django.converter import String
# app
from .relay import RelayMixin
from .registry import registry
from .actions import add_apps
# add all the apps from the settings
add_apps()
# mixins
from .types import (  # noqa: E402
    AuthQueryMixin, LoginMutation, LogoutMutation,
    DocumentQueryMixin,
    ImageQueryMixin,
    InfoQueryMixin,
    MenusQueryMixin,
    PagesQueryMixin,
    SettingsQueryMixin,
    SnippetsQueryMixin,
)

import graphql_jwt
import esite.kisy.schema_relay
import esite.kisy.schema
import esite.users.schema

# api version
GRAPHQL_API_FORMAT = (0, 2, 1)

# mixins
AuthQueryMixin_ = AuthQueryMixin()          # type: Any
DocumentQueryMixin_ = DocumentQueryMixin()  # type: Any
ImageQueryMixin_ = ImageQueryMixin()        # type: Any
InfoQueryMixin_ = InfoQueryMixin()          # type: Any
MenusQueryMixin_ = MenusQueryMixin()        # type: Any
PagesQueryMixin_ = PagesQueryMixin()        # type: Any
SettingsQueryMixin_ = SettingsQueryMixin()  # type: Any
SnippetsQueryMixin_ = SnippetsQueryMixin()  # type: Any


class Query(esite.kisy.schema.Query,
            esite.users.schema.Query,
            esite.kisy.schema_relay.RelayQuery,
            graphene.ObjectType,
            #AuthQueryMixin_,
            DocumentQueryMixin_,
            ImageQueryMixin_,
            InfoQueryMixin_,
            MenusQueryMixin_,
            PagesQueryMixin_,
            SettingsQueryMixin_,
            SnippetsQueryMixin_,
            RelayMixin,
            ):
    # API Version
    format = graphene.Field(String)

    def resolve_format(self, _info: ResolveInfo):
        return '%d.%d.%d' % GRAPHQL_API_FORMAT


#def mutation_parameters() -> dict:
#    dict_params = {
#        'login': LoginMutation.Field(),
#        'logout': LogoutMutation.Field(),
#    }
#    dict_params.update((camel_case_to_spaces(n).replace(' ', '_'), mut.Field())
#                       for n, mut in registry.forms.items())
#    return dict_params


#Mutations = type("Mutation",
#                 (graphene.ObjectType,),
#                 mutation_parameters()
#                 )

class Mutations(esite.kisy.schema.Mutation, esite.users.schema.Mutation, esite.kisy.schema_relay.RelayMutation, graphene.ObjectType):

    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(
    query=Query,
    mutation=Mutations,
    types=list(registry.models.values())
)

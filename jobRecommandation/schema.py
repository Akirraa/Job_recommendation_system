import graphene

import Recommendations.schema as recommendations_schema

class Query(
    recommendations_schema.Query,
    graphene.ObjectType,
):
    pass

class Mutation(
    recommendations_schema.Mutation,
    graphene.ObjectType,
):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)

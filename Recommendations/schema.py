import graphene
from graphene_django.types import DjangoObjectType
from Recommendations.models import Recommendation, UserVector, JobVector
from Jobs.models import Job
from UserAuth.models import User


# Types
class JobType(DjangoObjectType):
    class Meta:
        model = Job
        fields = ("id", "title", "description", "required_skills", "location", "job_type", "industry", "salary_range")

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "username", "email", "full_name", "bio", "role")

class RecommendationType(DjangoObjectType):
    class Meta:
        model = Recommendation
        fields = ("id", "user", "job", "score", "generated_at")

    job = graphene.Field(JobType)
    user = graphene.Field(UserType)

class UserVectorType(DjangoObjectType):
    class Meta:
        model = UserVector
        fields = ("id", "user", "vector")


class JobVectorType(DjangoObjectType):
    class Meta:
        model = JobVector
        fields = ("id", "job", "vector")


# Queries
class Query(graphene.ObjectType):
    recommendations = graphene.List(
        RecommendationType,
        user_id=graphene.ID(required=True),
        top=graphene.Int(default_value=10)
    )

    my_recommendations = graphene.List(
        RecommendationType,
        top=graphene.Int(default_value=10)
    )

    user_vector = graphene.Field(
        UserVectorType,
        user_id=graphene.ID(required=True)
    )

    job_vector = graphene.Field(
        JobVectorType,
        job_id=graphene.ID(required=True)
    )

    def resolve_recommendations(self, info, user_id, top):
        return Recommendation.objects.filter(user__id=user_id).order_by("-score")[:top]

    def resolve_my_recommendations(self, info, top):
        user = info.context.user
        if user.is_anonymous:
            return Recommendation.objects.none()
        return Recommendation.objects.filter(user=user).order_by("-score")[:top]

    def resolve_user_vector(self, info, user_id):
        return UserVector.objects.filter(user__id=user_id).first()

    def resolve_job_vector(self, info, job_id):
        return JobVector.objects.filter(job__id=job_id).first()


# Mutations
class SaveRecommendation(graphene.Mutation):
    class Arguments:
        recommendation_id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, recommendation_id):
        rec = Recommendation.objects.get(id=recommendation_id)
        rec.status = 'saved'
        rec.save()
        return SaveRecommendation(success=True)


class SkipRecommendation(graphene.Mutation):
    class Arguments:
        recommendation_id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, recommendation_id):
        rec = Recommendation.objects.get(id=recommendation_id)
        rec.status = 'skipped'
        rec.save()
        return SkipRecommendation(success=True)


class Mutation(graphene.ObjectType):
    save_recommendation = SaveRecommendation.Field()
    skip_recommendation = SkipRecommendation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)

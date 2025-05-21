import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql import GraphQLError
from django_filters import FilterSet, CharFilter, ChoiceFilter
from django.db.models import Q

from Recommendations.models import Recommendation, UserVector, JobVector
from Jobs.models import Job, Skill
from UserAuth.models import User
from Resume.models import ResumeData


# === Filters ===
class RecommendationFilter(FilterSet):
    status = CharFilter(field_name="status", lookup_expr="iexact")
    job__industry = CharFilter(field_name="job__industry", lookup_expr="iexact")
    # Filter by skill name in job required skills
    job__skills__name = CharFilter(field_name="job__skills__name", lookup_expr="icontains")
    # Filter by candidate location (resume)
    user__resumedata__location = CharFilter(field_name="user__resumedata__location", lookup_expr="icontains")

    class Meta:
        model = Recommendation
        fields = ["status", "job__industry", "job__skills__name", "user__resumedata__location"]


# === Types ===
class RecommendationType(DjangoObjectType):
    class Meta:
        model = Recommendation
        exclude = ['id']  # hide internal ID
        interfaces = (graphene.relay.Node,)


class UserVectorType(DjangoObjectType):
    class Meta:
        model = UserVector
        exclude = ['vector']
        interfaces = (graphene.relay.Node,)


class JobVectorType(DjangoObjectType):
    class Meta:
        model = JobVector
        exclude = ['vector']
        interfaces = (graphene.relay.Node,)


# === Role check helpers ===
def is_jobseeker(user):
    return user.is_authenticated and user.role == "jobseeker"


def is_recruiter(user):
    return user.is_authenticated and user.role == "recruiter"


# === Mutations ===
class SaveRecommendation(graphene.Mutation):
    class Arguments:
        recommendation_id = graphene.ID(required=True)

    ok = graphene.Boolean()

    def mutate(self, info, recommendation_id):
        user = info.context.user
        if not is_jobseeker(user):
            raise GraphQLError("Only jobseekers can save recommendations.")
        rec = Recommendation.objects.get(pk=recommendation_id)
        if rec.user != user:
            raise GraphQLError("Not authorized")
        rec.status = "saved"
        rec.save()
        return SaveRecommendation(ok=True)


class SkipRecommendation(graphene.Mutation):
    class Arguments:
        recommendation_id = graphene.ID(required=True)

    ok = graphene.Boolean()

    def mutate(self, info, recommendation_id):
        user = info.context.user
        if not is_jobseeker(user):
            raise GraphQLError("Only jobseekers can skip recommendations.")
        rec = Recommendation.objects.get(pk=recommendation_id)
        if rec.user != user:
            raise GraphQLError("Not authorized")
        rec.status = "skipped"
        rec.save()
        return SkipRecommendation(ok=True)


class UpdateUserVector(graphene.Mutation):
    class Arguments:
        text = graphene.String(required=True)

    ok = graphene.Boolean()

    def mutate(self, info, text):
        user = info.context.user
        if not is_jobseeker(user):
            raise GraphQLError("Only jobseekers can update their vector.")
        vector_obj, _ = UserVector.objects.update_or_create(user=user, defaults={'raw_text': text})
        return UpdateUserVector(ok=True)


class UpdateJobVector(graphene.Mutation):
    class Arguments:
        job_id = graphene.ID(required=True)
        text = graphene.String(required=True)

    ok = graphene.Boolean()

    def mutate(self, info, job_id, text):
        user = info.context.user
        if not is_recruiter(user):
            raise GraphQLError("Only recruiters can update job vectors.")
        job = Job.objects.get(pk=job_id)
        # Optionally check if the user owns the job posting here
        vector_obj, _ = JobVector.objects.update_or_create(job=job, defaults={'raw_text': text})
        return UpdateJobVector(ok=True)


# === Queries ===
class Query(graphene.ObjectType):
    recommendation = graphene.relay.Node.Field(RecommendationType)

    all_recommendations = DjangoFilterConnectionField(
        RecommendationType,
        filterset_class=RecommendationFilter,
        description="Filterable, paginated recommendations with role-based access"
    )

    user_vector = graphene.relay.Node.Field(UserVectorType)
    job_vector = graphene.relay.Node.Field(JobVectorType)
    all_user_vectors = DjangoFilterConnectionField(UserVectorType)
    all_job_vectors = DjangoFilterConnectionField(JobVectorType)

    # Custom search query on jobs inside recommendations
    search_recommendations = graphene.List(
        RecommendationType,
        query=graphene.String(required=True),
        description="Search recommendations by job title and description"
    )

    def resolve_all_recommendations(self, info, **kwargs):
        user = info.context.user
        if not user.is_authenticated:
            raise GraphQLError("Authentication required")
        # Jobseekers see only their recommendations, recruiters none or filtered if you want
        if is_jobseeker(user):
            return Recommendation.objects.filter(user=user)
        raise GraphQLError("Only jobseekers can view recommendations.")

    def resolve_search_recommendations(self, info, query, **kwargs):
        user = info.context.user
        if not is_jobseeker(user):
            raise GraphQLError("Only jobseekers can search recommendations.")
        qs = Recommendation.objects.filter(
            user=user
        ).filter(
            Q(job__title__icontains=query) | Q(job__description__icontains=query)
        )
        return qs


# === Mutations root ===
class Mutation(graphene.ObjectType):
    save_recommendation = SaveRecommendation.Field()
    skip_recommendation = SkipRecommendation.Field()
    update_user_vector = UpdateUserVector.Field()
    update_job_vector = UpdateJobVector.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)

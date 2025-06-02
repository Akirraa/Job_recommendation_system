import graphene
from graphene_django.types import DjangoObjectType
from django.core.management import call_command

from Recommendations.models import Recommendation, JobVector, UserVector, SemanticVector
from Resume.models import Resume, ResumeData
from UserAuth.models import User
from Jobs.models import Job, Skill

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "email", "full_name")  

class JobType(DjangoObjectType):
    class Meta:
        model = Job
        fields = ("id", "title", "description")


class skillType(DjangoObjectType):
    class Meta:
        model = Skill
        fields = ("name", "description")

class RecommendationType(DjangoObjectType):
    user = graphene.Field(UserType)   
    job = graphene.Field(JobType) 
    class Meta:
        model = Recommendation
        fields = '__all__'

class JobVectorType(DjangoObjectType):
    class Meta:
        model = JobVector
        fields = '__all__'

class UserVectorType(DjangoObjectType):
    class Meta:
        model = UserVector
        fields = '__all__'

class SemanticVectorType(DjangoObjectType):
    class Meta:
        model = SemanticVector
        fields = '__all__'

class ResumeType(DjangoObjectType):
    class Meta:
        model = Resume
        fields = '__all__'

class ResumeDataType(DjangoObjectType):
    class Meta:
        model = ResumeData
        fields = '__all__'

# Management Command Mutations
class GenerateJobVectors(graphene.Mutation):
    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info):
        try:
            call_command("generate_job_vectors")
            return GenerateJobVectors(success=True, message="Job vectors generated successfully.")
        except Exception as e:
            return GenerateJobVectors(success=False, message=str(e))

class GenerateUserVectors(graphene.Mutation):
    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info):
        try:
            call_command("generate_user_vectors")
            return GenerateUserVectors(success=True, message="User vectors generated successfully.")
        except Exception as e:
            return GenerateUserVectors(success=False, message=str(e))

class GenerateRecommendations(graphene.Mutation):
    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info):
        try:
            call_command("generate_recommendations")
            return GenerateRecommendations(success=True, message="Recommendations generated successfully.")
        except Exception as e:
            return GenerateRecommendations(success=False, message=str(e))

class SemanticRerank(graphene.Mutation):
    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info):
        try:
            call_command("semantic_rerank")
            return SemanticRerank(success=True, message="Semantic rerank completed successfully.")
        except Exception as e:
            return SemanticRerank(success=False, message=str(e))

class ParseResumes(graphene.Mutation):
    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info):
        try:
            call_command("parse_resumes")
            return ParseResumes(success=True, message="Resume parsing completed successfully.")
        except Exception as e:
            return ParseResumes(success=False, message=str(e))

class RecommendationMutation(graphene.ObjectType):
    generate_job_vectors = GenerateJobVectors.Field()
    generate_user_vectors = GenerateUserVectors.Field()
    generate_recommendations = GenerateRecommendations.Field()
    semantic_rerank = SemanticRerank.Field()
    parse_resumes = ParseResumes.Field()

class RecommendationQuery(graphene.ObjectType):
    all_recommendations = graphene.List(RecommendationType)
    all_user_vectors = graphene.List(UserVectorType)
    all_job_vectors = graphene.List(JobVectorType)
    all_semantic_vectors = graphene.List(SemanticVectorType)
    all_resumes = graphene.List(ResumeType)
    all_resume_data = graphene.List(ResumeDataType)

    def resolve_all_recommendations(self, info):
        return Recommendation.objects.all()

    def resolve_all_user_vectors(self, info):
        return UserVector.objects.all()

    def resolve_all_job_vectors(self, info):
        return JobVector.objects.all()

    def resolve_all_semantic_vectors(self, info):
        return SemanticVector.objects.all()

    def resolve_all_resumes(self, info):
        return Resume.objects.all()

    def resolve_all_resume_data(self, info):
        return ResumeData.objects.all()

schema = graphene.Schema(query=RecommendationQuery, mutation=RecommendationMutation)

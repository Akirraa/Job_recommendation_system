import django_filters
from .models import Job


class JobFilter(django_filters.FilterSet):
    min_salary = django_filters.NumberFilter(field_name='salary_range', lookup_expr='gte')
    max_salary = django_filters.NumberFilter(field_name='salary_range', lookup_expr='lte')
    skill_ids = django_filters.BaseInFilter(field_name='required_skills__id', lookup_expr='in')

    class Meta:
        model = Job
        fields = ['job_type', 'industry', 'location', 'min_salary', 'max_salary', 'skill_ids']

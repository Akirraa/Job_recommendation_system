from django.contrib import admin

from Recommendations.models import RecommendationMetric

# Register your models here.
@admin.register(RecommendationMetric)
class RecommendationMetricAdmin(admin.ModelAdmin):
    list_display = ("date", "precision_at_5", "sample_size")
    ordering = ("-date",)
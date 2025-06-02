from django.contrib import admin
from django.urls import path, include
from graphene_django.views import GraphQLView

from Recommendations.schema import schema
from UserAuth.views import placeholderView

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('api/auth/', include('UserAuth.urls')),
    path('api/jobs/', include('Jobs.urls')),
    path('api/applications/', include('Applications.urls')),
    path('api/resume/', include('Resume.urls')),
    
    path(
        'api/recommendations/graphql/',
        GraphQLView.as_view(schema=schema, graphiql=True)
    ),
    
    
    
    path('', placeholderView, name='home'),
]

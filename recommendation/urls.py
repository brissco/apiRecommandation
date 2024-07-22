from django.urls import path
from .views import  RecommendationView

urlpatterns = [
    #  path('collaborative/', CollaborativeFilteringView.as_view(), name='collaborative-filtering'),
    # path('content/', ContentFilteringView.as_view(), name='content-filtering'),
    # path('hybrid/', HybridFilteringView.as_view(), name='hybrid-filtering'),
     path('recommend/', RecommendationView.as_view(), name='recommendation'),
]

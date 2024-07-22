# from rest_framework import serializers

# class RecommendationInputSerializer(serializers.Serializer):
#     workforce_profiles = serializers.ListField(
#         child=serializers.CharField(), 
#         allow_empty=False
#     )
#     job_descriptions = serializers.ListField(
#         child=serializers.CharField(), 
#         allow_empty=False
#     )
#     ratings_matrix = serializers.ListField(
#         child=serializers.ListField(
#             child=serializers.IntegerField()
#         ), 
#         allow_empty=False
#     )

from rest_framework import serializers

class RecommendationInputSerializer(serializers.Serializer):
    workforce_profiles = serializers.ListField(child=serializers.CharField())
    job_descriptions = serializers.ListField(child=serializers.CharField())
    ratings_matrix = serializers.ListField(child=serializers.ListField(child=serializers.FloatField()))

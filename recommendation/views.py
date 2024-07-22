# from django.shortcuts import render
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# import numpy as np
# from django.http import JsonResponse
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
# from .serializers.serializers import RecommendationInputSerializer

# def predict_ratings(user_index, similarities, ratings_matrix):
#     similar_users = similarities[user_index]
#     user_ratings = ratings_matrix[user_index]
#     non_rated_items = np.where(user_ratings == 0)[0]
#     predicted_ratings = {}
#     for item in non_rated_items:
#         weighted_sum = 0
#         similarity_sum = 0
#         for other_user_index in range(len(ratings_matrix)):
#             if ratings_matrix[other_user_index, item] > 0:
#                 weighted_sum += similar_users[other_user_index] * ratings_matrix[other_user_index, item]
#                 similarity_sum += similar_users[other_user_index]
#         if similarity_sum > 0:
#             predicted_ratings[item] = weighted_sum / similarity_sum
#         else:
#             predicted_ratings[item] = 0
#     return predicted_ratings

# def hybrid_recommendations(user_index, content_similarities, collaborative_similarities, ratings_matrix, alpha=0.5):
#     content_scores = content_similarities[user_index]
#     collaborative_scores = predict_ratings(user_index, collaborative_similarities, ratings_matrix)
#     hybrid_scores = {}
#     for item_index in range(len(content_scores)):
#         hybrid_scores[item_index] = alpha * content_scores[item_index] + (1 - alpha) * collaborative_scores.get(item_index, 0)
#     recommended_items = sorted(hybrid_scores, key=hybrid_scores.get, reverse=True)
#     return recommended_items

# # class CollaborativeFilteringView(APIView):
# #     def post(self, request):
# #         serializer = RecommendationInputSerializer(data=request.data)
# #         if serializer.is_valid():
# #             data = serializer.validated_data
# #             ratings_matrix = np.array(data['ratings_matrix'])
# #             collaborative_similarities = cosine_similarity(ratings_matrix)
# #             recommendations = {}
# #             for user_index in range(len(ratings_matrix)):
# #                 recommendations[user_index] = predict_ratings(user_index, collaborative_similarities, ratings_matrix)
# #             return Response(recommendations, status=status.HTTP_200_OK)
# #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class CollaborativeFilteringView(APIView):
#     def post(self, request):
#         serializer = RecommendationInputSerializer(data=request.data)
#         if serializer.is_valid():
#             data = serializer.validated_data
#             ratings_matrix = np.array(data['ratings_matrix'])
#             collaborative_similarities = cosine_similarity(ratings_matrix).astype(float)  # Convertir en float
#             recommendations = {}
#             for user_index in range(len(ratings_matrix)):
#                 recommendations[user_index] = predict_ratings(user_index, collaborative_similarities, ratings_matrix)
#             return JsonResponse(recommendations, status=status.HTTP_200_OK)
#         return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class ContentFilteringView(APIView):
#     def post(self, request):
#         serializer = RecommendationInputSerializer(data=request.data)
#         if serializer.is_valid():
#             data = serializer.validated_data
#             workforce_profiles = data['workforce_profiles']
#             job_descriptions = data['job_descriptions']
#             corpus = workforce_profiles + job_descriptions
#             vectorizer = TfidfVectorizer()
#             tfidf_matrix = vectorizer.fit_transform(corpus)
#             worker_profiles_tfidf = tfidf_matrix[:len(workforce_profiles)]
#             job_descriptions_tfidf = tfidf_matrix[len(workforce_profiles):]
#             content_similarities = cosine_similarity(worker_profiles_tfidf, job_descriptions_tfidf)
#             recommendations = {}
#             for user_index in range(len(workforce_profiles)):
#                 recommendations[user_index] = list(np.argsort(-content_similarities[user_index]))
#             return Response(recommendations, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class HybridFilteringView(APIView):
#     def post(self, request):
#         serializer = RecommendationInputSerializer(data=request.data)
#         if serializer.is_valid():
#             data = serializer.validated_data
#             workforce_profiles = data['workforce_profiles']
#             job_descriptions = data['job_descriptions']
#             ratings_matrix = np.array(data['ratings_matrix'])
#             corpus = workforce_profiles + job_descriptions
#             vectorizer = TfidfVectorizer()
#             tfidf_matrix = vectorizer.fit_transform(corpus)
#             worker_profiles_tfidf = tfidf_matrix[:len(workforce_profiles)]
#             job_descriptions_tfidf = tfidf_matrix[len(workforce_profiles):]
#             content_similarities = cosine_similarity(worker_profiles_tfidf, job_descriptions_tfidf)
#             collaborative_similarities = cosine_similarity(ratings_matrix)
#             recommendations = {}
#             for user_index in range(len(workforce_profiles)):
#                 recommendations[user_index] = hybrid_recommendations(user_index, content_similarities, collaborative_similarities, ratings_matrix)
#             return Response(recommendations, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import numpy as np
from collections import defaultdict
from sklearn.metrics.pairwise import cosine_similarity
import random

# Vue principale
class RecommendationView(APIView):
    def post(self, request):
        worker_profiles = request.data.get('worker_profiles', {})
        mission_data = request.data.get('mission_data', [])
        new_missions = request.data.get('new_missions', [])
        worker_histories = request.data.get('worker_histories', {})
        all_missions = mission_data + new_missions
        new_mission_ids = [mission['id'] for mission in new_missions]

        if not worker_profiles:
            return Response({"error": "No worker profiles provided."}, status=status.HTTP_400_BAD_REQUEST)

        results = {}
        for worker_id, profile in worker_profiles.items():
            recommendations = self.hybrid_recommendation(worker_id, worker_profiles, all_missions, worker_histories, new_mission_ids)
            results[worker_id] = [{'Mission ID': mission_id, 'Score': score} for mission_id, score in recommendations]

        return Response(results, status=status.HTTP_200_OK)

    def hybrid_recommendation(self, worker_id, worker_profiles, missions, worker_histories, new_mission_ids):
        worker_vector = np.random.rand(1, 10)  # Example worker vector
        mission_vectors = np.random.rand(len(missions), 10)  # Example mission vectors
        mission_ids = [mission['id'] for mission in missions]

        content_based = self.content_based_recommendation(worker_vector, mission_vectors, mission_ids)
        similar_workers = self.find_similar_workers(worker_id, worker_profiles)
        collaborative = self.aggregate_recommendations(worker_histories, similar_workers)

        combined_scores = defaultdict(float)
        for mission_id, score in content_based + collaborative:
            combined_scores[mission_id] += score
        sorted_recommendations = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)
        return [(mission_id, score) for mission_id, score in sorted_recommendations if mission_id in new_mission_ids]

    @staticmethod
    def content_based_recommendation(worker_vector, mission_vectors, mission_ids, threshold=0.5):
        similarities = cosine_similarity(worker_vector, mission_vectors).flatten()
        return [(mission_id, similarity) for mission_id, similarity in zip(mission_ids, similarities) if similarity > threshold]

    @staticmethod
    def pearson_correlation(user1_ratings, user2_ratings):
        common_items = set(user1_ratings.keys()).intersection(user2_ratings.keys())
        if not common_items:
            return 0
        user1_common_ratings = [user1_ratings[item] for item in common_items]
        user2_common_ratings = [user2_ratings[item] for item in common_items]
        user1_mean = np.mean(user1_common_ratings)
        user2_mean = np.mean(user2_common_ratings)
        numerator = sum((u1 - user1_mean) * (u2 - user2_mean) for u1, u2 in zip(user1_common_ratings, user2_common_ratings))
        denominator = np.sqrt(sum((u1 - user1_mean) ** 2 for u1 in user1_common_ratings) * sum((u2 - user2_mean) ** 2 for u2 in user2_common_ratings))
        return numerator / denominator if denominator != 0 else 0

    @staticmethod
    def find_similar_workers(worker_id, worker_profiles, k=5):
        similarities = {other_worker: RecommendationView.pearson_correlation(worker_profiles[worker_id]['history'], worker_profiles[other_worker]['history'])
                        for other_worker in worker_profiles if other_worker != worker_id}
        return sorted(similarities, key=similarities.get, reverse=True)[:k]

    @staticmethod
    def aggregate_recommendations(mission_histories, similar_workers):
        recommendations = defaultdict(float)
        for worker in similar_workers:
            for mission, rating in mission_histories[worker].items():
                recommendations[mission] += rating
        return sorted(recommendations.items(), key=lambda x: x[1], reverse=True)
    

    def get(self, request, mission_id):
        worker_profiles = request.data.get('worker_profiles', {})
        mission_data = request.data.get('mission_data', [])
        new_missions = request.data.get('new_missions', [])
        worker_histories = request.data.get('worker_histories', {})
        all_missions = mission_data + new_missions

        recommendations = self.recommend_workers_for_mission(mission_id, worker_profiles, all_missions, worker_histories)
        results = [{'Worker ID': worker_id, 'Score': score} for worker_id, score in recommendations]
        return Response(results, status=status.HTTP_200_OK)

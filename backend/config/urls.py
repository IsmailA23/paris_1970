"""
URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URL configuration
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from app.common import render_react_view
from app import views


def react_view_path(route, component_name):
    """ Convenience function for React views """
    return path(
        route,
        render_react_view,
        {
            'component_name': component_name,
        },
    )


urlpatterns = [
    # Django admin page
    path('admin/', admin.site.urls),

    # API endpoints
    path('api/photo/<int:map_square_number>/<int:photo_number>/', views.photo),
    path('api/prev_next_photos/<int:map_square_number>/<int:photo_number>/',
         views.previous_next_photos),
    path('api/similar_photos/<int:map_square_number>/<int:photo_number>/<int:num_similar_photos>/',
views.         get_photo_by_similarity),
    path('api/photographer/<int:photographer_number>/', views.get_photographer),
    path('api/map_square/<int:map_square_number>/', views.get_map_square),
    path('api/corpus_analysis/', views.get_corpus_analysis_results),
    path('api/all_photos/', views.all_photos),
    path('api/all_analyses/', views.all_analyses),
    path('api/all_map_squares/', views.all_map_squares),
    path('api/similarity/', views.get_all_photos_in_order),
    path('api/analysis/<str:analysis_name>/', views.get_photos_by_analysis),
    path('api/clustering/<int:number_of_clusters>/<int:cluster_number>/',
         views.get_photos_by_cluster),
    path('api/analysis/<str:analysis_name>/<str:object_name>/', views.get_photos_by_analysis),
    path('api/search/', views.search),
    path('api/get_tags/', views.get_tags),
    # path('api/faster_rcnn_object_detection/<str:object_name>/', views.get_photos_by_object_rcnn),
    # path('api/model/<str:model_name>/<str:object_name>/', views.get_photos_by_object),
    path('', views.index),

    # react_view_path('', 'IndexView'),
    react_view_path('photo/<int:mapSquareNumber>/<int:photoNumber>/', 'PhotoView'),
    react_view_path('similar_photos/<int:mapSquareNumber>/<int:photoNumber>/'
                    '<int:numSimilarPhotos>/', 'SimilarityView'),
    react_view_path('photographer/<int:photographerNumber>/', 'PhotographerView'),
    react_view_path('map_square/<int:mapSquareNumber>/', 'MapSquareView'),
    react_view_path('about/', 'About'),
    react_view_path('search/', 'Search'),
    react_view_path('similarity/', 'AllPhotosView'),
    react_view_path('analysis/<str:analysisName>/', 'AnalysisView'),
    react_view_path('analysis/<str:analysisName>/<str:objectName>', 'AnalysisView'),
    react_view_path('all_analysis/', 'AllAnalysisView'),
    react_view_path('clustering/<int:numberOfClusters>/<int:clusterNumber>/', 'ClusterView'),
]

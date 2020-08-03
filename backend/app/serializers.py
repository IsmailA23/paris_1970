"""
Serializers take models or other data structures and present them
in ways that can be transported across the backend/frontend divide, or
allow the frontend to suggest changes to the backend/database.
"""
from rest_framework import serializers
from .models import Photo, MapSquare, Photographer


class PhotoSerializer(serializers.ModelSerializer):
    """
    Serializes a photo
    """
    photographer = serializers.SerializerMethodField()
    map_square = serializers.SerializerMethodField()

    def get_photographer(self, instance):
        return PhotographerForPhotosSerializer(instance.photographer_obj).data

    def get_map_square(self, instance):
        return MapSquareForPhotosSerializer(instance.map_square_obj).data

    class Meta:
        model = Photo
        fields = ['id', 'front_src', 'back_src', 'alt', 'title', 'photographer', 'map_square']


class MapSquareSerializer(serializers.ModelSerializer):
    """
    Serializes a map square
    """
    photos = serializers.SerializerMethodField()

    def get_photos(self, instance):
        photo_obj = Photo.objects.filter(map_square_obj_id=instance.id)
        return PhotosForMapSquareSerializer(photo_obj, many=True).data

    class Meta:
        model = MapSquare
        fields = ['id', 'photos', 'boundaries', 'name']


class PhotographerSerializer(serializers.ModelSerializer):
    """
    Serializes a photographer
    """
    photos = serializers.SerializerMethodField()
    map_square = serializers.SerializerMethodField()

    def get_photos(self, instance):
        photo_obj = Photo.objects.filter(map_square_obj_id=instance.id)
        return PhotosForMapSquareSerializer(photo_obj, many=True).data

    def get_map_square(self, instance):
        return MapSquareForPhotosSerializer(instance.map_square_obj).data

    class Meta:
        model = Photographer
        fields = ['id', 'name', 'type', 'sentiment', 'photos', 'map_square']


# These methods are used to avoid an infinite recursion depth
class PhotographerForPhotosSerializer(serializers.ModelSerializer):
    """
    Serializes a Photographer for the Photo model, but without a reference to the list of photos
    or the map square
    """
    class Meta:
        model = Photographer
        fields = ['id', 'name', 'type', 'sentiment']


class PhotoForPhotographerSerializer(serializers.ModelSerializer):
    """
    Serializes a Photo for the Photographer model, but without a reference to the photographer
    """
    map_square = serializers.SerializerMethodField()

    def get_map_square(self, instance):
        return MapSquareForPhotosSerializer(instance.map_square_obj).data

    class Meta:
        model = Photo
        fields = ['id', 'front_src', 'back_src', 'alt', 'title', 'map_square']


class MapSquareForPhotosSerializer(serializers.ModelSerializer):
    """
    Serializes a Map Square for the Photo model, but without a reference to the list of photos
    """
    class Meta:
        model = MapSquare
        fields = ['id', 'name', 'boundaries']


class PhotosForMapSquareSerializer(serializers.ModelSerializer):
    """
    Serializes a Photo for the Map Square model, but without a reference to the map square
    """
    photographer = serializers.SerializerMethodField()

    def get_photographer(self, instance):
        return PhotographerForPhotosSerializer(instance.photographer_obj).data

    class Meta:
        model = Photo
        fields = ['id', 'front_src', 'back_src', 'alt', 'title', 'photographer']

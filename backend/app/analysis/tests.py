"""
Tests for the main main.
"""

from pathlib import Path
from django.conf import settings
from django.test import TestCase

# NOTE(ra): we have to use absolute imports in this module because the Django test runner
# will resolve imports relative to the backend working directory
# If you do, e.g.,
#   from ..models import Photo
# ... you'll crash the test runner. Please don't!
from app.models import Photo, MapSquare
from app.analysis import (
    photographer_caption_length,
    whitespace_percentage,
    courtyard_frame,
    find_windows,
    detect_sky
)


class AnalysisTestBase(TestCase):
    """
    TestCase for testing our analysis modules
    """
    def setUp(self):
        """
        Setup for all tests -- we initialize a bunch of objects we can use in our tests
        """
        super().setUp()

        self.map_square = MapSquare()
        self.map_square.save()

        self.photo_0 = Photo(number=1, map_square=self.map_square)
        test_photo_path = Path(settings.TEST_PHOTOS_DIR, 'test2.jpg')
        self.photo_0.front_local_path = test_photo_path
        self.photo_0.save()

        self.photo_1 = Photo(number=2, map_square=self.map_square)
        self.photo_1.save()

        self.photo_square = Photo(number=3, map_square=self.map_square)
        test_photo_path = Path(settings.TEST_PHOTOS_DIR, 'find_windows_test_photo.jpg')
        self.photo_square.front_local_path = test_photo_path
        self.photo_square.save()

        self.photo_2 = Photo(number=4, map_square=self.map_square)
        test_photo_path = Path(settings.TEST_PHOTOS_DIR, '29_binder copy.jpg')
        self.photo_2.front_local_path = test_photo_path
        self.photo_2.save()

        self.photo_3 = Photo(number=5, map_square=self.map_square)
        test_photo_path = Path(settings.TEST_PHOTOS_DIR, '94_binder copy.jpg')
        self.photo_3.front_local_path = test_photo_path
        self.photo_3.save()

        self.photo_black = Photo(number=6, map_square=self.map_square)
        test_photo_path = Path(settings.TEST_PHOTOS_DIR, 'fully_black_image.jpg')
        self.photo_black.front_local_path = test_photo_path
        self.photo_black.save()

        self.photo_white = Photo(number=7, map_square=self.map_square)
        test_photo_path = Path(settings.TEST_PHOTOS_DIR, 'fully_white_image.jpg')
        self.photo_white.front_local_path = test_photo_path
        self.photo_white.save()

        self.photo_windows = Photo(number=8, map_square=self.map_square)
        test_photo_path = Path(settings.TEST_PHOTOS_DIR, 'gray_building_with_windows.jpg')
        self.photo_windows.front_local_path = test_photo_path
        self.photo_windows.save()

        self.photo_240_10 = Photo(number=9, map_square=self.map_square)
        test_photo_path = Path(settings.TEST_PHOTOS_DIR, 'ms_240_10_cleaned.jpg')
        self.photo_240_10.front_local_path = test_photo_path
        self.photo_240_10.save()

        self.photo_front_desk = Photo(number=10, map_square=self.map_square)
        test_photo_path = Path(settings.TEST_PHOTOS_DIR, 'indoor_front_desk.jpg')
        self.photo_front_desk.front_local_path = test_photo_path
        self.photo_front_desk.save()

        self.photo_tall_crane = Photo(number=11, map_square=self.map_square)
        test_photo_path = Path(settings.TEST_PHOTOS_DIR, 'tall_crane.jpg')
        self.photo_tall_crane.front_local_path = test_photo_path
        self.photo_tall_crane.save()

        self.photo_far_building = Photo(number=12, map_square=self.map_square)
        test_photo_path = Path(settings.TEST_PHOTOS_DIR, 'far_window_buildings.jpg')
        self.photo_far_building.front_local_path = test_photo_path
        self.photo_far_building.save()

    def test_photographer_caption_length(self):
        self.photo_0.photographer_caption = '123456'
        result = photographer_caption_length.analyze(self.photo_0)
        self.assertEqual(6, result)

    def test_whitespace_percentage(self):
        result = whitespace_percentage.analyze(self.photo_0)
        self.assertEqual(50, result)

    def test_courtyard_frame(self):
        result = courtyard_frame.analyze(self.photo_0)
        print(result)
        #self.assertEqual(True, result)


    def test_find_windows(self):
        square_result = find_windows.analyze(self.photo_square)
        black_result = find_windows.analyze(self.photo_black)
        white_result = find_windows.analyze(self.photo_white)
        many_windows = find_windows.analyze(self.photo_windows)
        building_perspective_view = find_windows.analyze(self.photo_240_10)
        front_desk = find_windows.analyze(self.photo_front_desk)
        tall_crane = find_windows.analyze(self.photo_tall_crane)
        far_building = find_windows.analyze(self.photo_far_building)

        self.assertEqual(True, square_result)
        self.assertEqual(False, black_result)
        self.assertEqual(False, white_result)
        self.assertEqual(True, many_windows)
        self.assertEqual(True, building_perspective_view)
        self.assertEqual(False, front_desk)
        self.assertEqual(False, tall_crane)
        self.assertEqual(True, far_building)

    def test_gradient_analysis(self):
        result = detect_sky.analyze(self.photo_3)
        self.assertEqual(True, result)

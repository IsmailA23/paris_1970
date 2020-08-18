"""

calc_whitespace.py - analysis to calculate ratio of pixels above a certain threshold value (0.6)
to the size of the image

"""
from urllib.error import HTTPError
from http.client import RemoteDisconnected
from textwrap import dedent

from skimage import io
import numpy as np
import cv2

from app.models import Photo

from .tests import AnalysisTestBase


def analysis() -> dict:
    """
    Calculates the whitespace for all sides of the photos in the database

    :returns A dictionary of photo ids with values of { model fields: updated values } to be
    assigned to photo instances
    """
    result = {}
    number_of_photos = len(Photo.objects.all())

    # Iterate through all photos in the database
    for photo in Photo.objects.all():
        photo_srcs = {
            'front_src': photo.front_src,
            'back_src': photo.back_src,
            'binder_src': photo.binder_src
        }
        new_attributes = {}

        # Calculate the whitespace for each source of the photo
        # If src is blank or not a url, then the ratio will not be calculated
        # Values will be stored in new_attributes dictionary with key of 'white_space_ratio_' + side
        for side in ['front', 'back', 'binder']:
            try:
                url = photo_srcs[side + '_src']

                # Get the image from the source url:
                # Will raise ValueError if src url is '' (No image source for side)
                # Will raise FileNotFound error if src is just a filename rather than a url
                # (imread will attempt to load the file from the current working directory)
                image = io.imread(url)

                # Convert image to grayscale
                # (Changes image array shape from (height, width, 3) to (height, width))
                # (Pixels (image[h][w]) will be a value from 0 to 255)
                gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                # Normalize image pixels to range from 0 to 1
                # Normalized values are used instead of absolute pixel values to account for
                # differences in brightness (across all photos) that may cause white areas in
                # some photos, like a piece of paper, to appear dark.
                normalized_gray_image = gray_image / np.max(gray_image)

                # Count number of pixels that have a value greater than .6 (arbitrarily chosen)
                # (uses numpy broadcasting and creates an array of boolean values (0 and 1))
                number_of_pixels = (normalized_gray_image > .6).sum()

                # Ratio of pixels above the threshold to the total number of pixels in the photo
                # (Prevent larger images from being ranked as being composed mostly of whitespace,
                # just because they are larger)
                white_space_ratio = number_of_pixels / gray_image.size

                new_attributes[f'white_space_ratio_{side}'] = white_space_ratio
                print(f'Successfully calculated whitespace ratio for photo {photo.id} {side}')
            except (ValueError, FileNotFoundError):
                pass
            except (HTTPError, RemoteDisconnected):
                print(dedent(f'''
                    *** Right now, the analysis breaks after too many http requests, so it may not
                    calculate whitespace for all the photos, even the first time. If it stops
                    working, you will have to wait a while before it is successfully able to make
                    requests again. ***

                    Successfully calculated whitespace ratio for {photo.id - 1}/{number_of_photos}
                    photos.
                '''))
                return result

        # Assign new attributes to photo id in result
        result[photo.id] = new_attributes
    print('Successfully calculated whitespace ratio for all photos.')
    return result


class TestAnalysis(AnalysisTestBase):
    """
    Test cases to make sure things are running properly
    """

    def test_analysis(self):
        """
        TODO: write me!
        """
        pass

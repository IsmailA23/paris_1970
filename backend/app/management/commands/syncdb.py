"""
Django management command syncdb

Syncs local db with data from project Google Sheet
"""

# Python standard library
import pickle
import os
from textwrap import dedent

# 3rd party
import tqdm
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Django
from django.contrib.auth.models import User
from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand

# Ours
from app.models import Photo, MapSquare, Photographer
from app.common import print_header

# The scope of our access to the Google Sheets Account
# TODO: reduce this scope, if possible, to only access a single specified sheet
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly',
          'https://www.googleapis.com/auth/drive.metadata.readonly']

# Our metadata spreadsheet lives here:
# https://docs.google.com/spreadsheets/d/1R4zBXLwM08yq_d4R9_JrDSGThpoaI46_Vmn9tDu8w9I/edit#gid=0
METADATA_SPREADSHEET_ID = '1R4zBXLwM08yq_d4R9_JrDSGThpoaI46_Vmn9tDu8w9I'


def authorize_google_apps():
    """
    Authorization flow for letting our application talk with the Google API
    """
    credentials = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(settings.GOOGLE_TOKEN_FILE):
        with open(settings.GOOGLE_TOKEN_FILE, 'rb') as token:
            credentials = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                settings.GOOGLE_API_CREDENTIALS_FILE,
                SCOPES
            )
            credentials = flow.run_local_server(port=8080)
        # Save the credentials for the next run
        with open(settings.GOOGLE_TOKEN_FILE, 'wb') as token:
            pickle.dump(credentials, token)

    return credentials


def create_lookup_dict(credentials):
    """
    Creates a quick look up dictionary to get the image URL using map square number and source name
    :param credentials: Credentials object for drive service
    :return Look up dictionary to get the image URL using map square number and source name
    """
    # Resource object for interacting with the google API
    drive_service = build('drive', 'v3', credentials=credentials)

    # Get list of files in google drive folder
    results = drive_service.files().list(
        q="'1aiY1nFJn6T7khu5dhIs3U2o8RdHBu6V7' in parents",
        fields="nextPageToken, files(id, name)"
    ).execute()

    # List of dictionaries containing id and name of map square folder in the google drive
    map_square_folders = results.get('files', [])

    lookup_dict = {}
    # tqdm is a library that shows a progress bar
    for map_square in tqdm.tqdm(map_square_folders):
        result = drive_service.files().list(
            q=f"'{map_square['id']}' in parents",
            fields="files(id, name)"
        ).execute()
        images = result.get('files', [])

        # Creates a dictionary mapping photo number to a list of the photo sources belonging to
        # that number
        map_square_dict = {}
        for image in images:
            photo_number = image['name'].split('_')[0]
            photo_srcs = map_square_dict.get(photo_number, {})
            photo_srcs[image['name']] = \
                f"https://drive.google.com/uc?id={image['id']}&export=download"
            map_square_dict[photo_number] = photo_srcs

        lookup_dict[map_square['name']] = map_square_dict
    return lookup_dict


# Sides of a photo
SIDES = ['front', 'back', 'binder']

MODEL_NAME_TO_MODEL = {"Photo": Photo, "MapSquare": MapSquare, "Photographer": Photographer}


def add_photo_srcs(model_kwargs, map_square_folder, photo_number):
    """
    Takes the map square folder and the photo number to dynamically adds the Google Drive urls
    into the model kwargs
    :param model_kwargs: Dictionary of keyword arguments to be used in creating the model
    :param map_square_folder: Dictionary of photo sources with keys of photo_number
    :param photo_number: The number of the desired photo in the map_square_folder
    """
    photo_urls = map_square_folder.get(str(photo_number), '')
    if photo_urls == '':
        return

    for side in SIDES:
        model_kwargs[f'{side}_src'] = photo_urls.get(f'{photo_number}_{side}.jpg', '')


def call_sheets_api(spreadsheet_ranges, creds):
    """
    Creates list of list of spreadsheet rows
    :param spreadsheet_ranges: Names of spreadsheets to import
    :param creds: Credentials object for drive service
    :return: List of list of spreadsheet rows (by model)
    """
    # Resource object for interacting with the google API
    sheets_service = build('sheets', 'v4', credentials=creds)

    databases = []
    sheet = sheets_service.spreadsheets()
    for spreadsheet_range in spreadsheet_ranges:
        get_values_cmd = \
            sheet.values().get(spreadsheetId=METADATA_SPREADSHEET_ID, range=spreadsheet_range)
        result = get_values_cmd.execute()
        values = result.get('values', [])
        databases.append(values)
    return databases


def populate_database(model_name, values_as_a_dict, photo_url_lookup):
    """
    Adds model instances to the database based on the data imported from the google spreadsheet
    :param model_name: Name of the model to create an instance of
    :param values_as_a_dict: List of dictionaries representing spreadsheet rows in the form of
    { column names: cell values }
    :param photo_url_lookup: Dictionary of map square folders in the form of a dictionary
    """
    for row in values_as_a_dict:
        # Filter column headers for model fields
        model_fields = MODEL_NAME_TO_MODEL[model_name]._meta.get_fields()
        model_field_names = [field.name for field in model_fields]

        model_kwargs = {}
        for header in row.keys():
            if header in model_field_names or header == 'map_square_number':
                # Check if value in column is a number
                value = row[header]
                if header in ['number', 'map_square_number', 'photographer']:
                    if header == 'map_square_number':
                        header = 'map_square'
                    try:
                        value = int(value)
                    except ValueError:
                        continue
                # Evaluate value as a boolean
                elif header == 'contains_sticker':
                    if value.lower() == 'yes':
                        value = True
                    elif value.lower() == 'no':
                        value = False
                    elif value.isdigit() and 0 <= int(value) <= 1:
                        value = bool(value)
                    else:
                        continue
                model_kwargs[header] = value

        # If no model fields found, do not create model instance
        if len(model_kwargs) == 0:
            continue

        if model_name in ['Photo', 'Photographer']:
            map_square_number = model_kwargs.get('map_square', None)
            # Returns the object that matches or None if there is no match
            model_kwargs['map_square'] = \
                MapSquare.objects.filter(number=map_square_number).first()

        if model_name == 'Photo':
            # Gets the Map Square folder and the photo number to look up the URLs
            map_square_number = str(row.get('map_square_number', ''))
            map_square_folder = photo_url_lookup.get(map_square_number, '')
            photo_number = row.get('number', '')

            if map_square_folder:
                add_photo_srcs(model_kwargs, map_square_folder, str(photo_number))

            # Get the corresponding Photographer objects
            photographer_number = model_kwargs.get('photographer', None)
            model_kwargs['photographer'] = \
                Photographer.objects.filter(number=photographer_number).first()

        print_header("Final model_kwargs: " + str(model_kwargs))

        model_instance = MODEL_NAME_TO_MODEL[model_name](**model_kwargs)
        model_instance.save()


class Command(BaseCommand):
    """
    Custom django-admin command used to sync the local db with data from project Google Sheet
    """
    help = 'Syncs local db with data from project Google Sheet and Google Drive'

    def handle(self, *args, **options):
        # pylint: disable=too-many-locals

        # Delete database
        if os.path.exists(settings.DB_PATH):
            print_header('Deleting existing db...')
            try:
                os.remove(settings.DB_PATH)
            except PermissionError:
                # weird indentation because turns out dedent nests weirdly...
                print_header('Permission Error')
                print(dedent('''
                    Unable to delete the database file while the backend is running.
                    Please stop the "Run backend" process and try again.
                '''))

                return

        # Delete all migrations
        for file in os.listdir(settings.MIGRATIONS_DIR):
            if file not in ['__init__.py', '__pycache__']:
                file_path = os.path.join(settings.MIGRATIONS_DIR, file)
                os.remove(file_path)
        print('Done!')

        # Rebuild database
        print_header('Rebuilding db from migrations...')
        call_command('makemigrations')
        call_command('migrate')
        print('Done!')

        # THIS IS JUST FOR PROTOTYPING NEVER EVER EVER EVER IN PRODUCTION do this
        User.objects.create_superuser('admin', password='adminadmin')

        # The order of these ranges matter. The Photographer model needs to have foreign keys to
        # the MapSquare database, so we add the Map Squares first
        spreadsheet_ranges = ['MapSquare', 'Photographer', 'Photo']

        print_header(f'''Will import ranges {", ".join(spreadsheet_ranges)}. (If nothing
          is happening, please try again.)''')

        credentials = authorize_google_apps()
        print_header('Getting the URL for all photos (This might take a couple of minutes)...')

        # Call the Sheets API to get metadata values
        databases = call_sheets_api(spreadsheet_ranges, credentials)

        # Call Drive API to create a lookup dictionary for photo urls
        photo_url_lookup = create_lookup_dict(credentials)

        if not databases:
            print_header('No data found.')
            return

        for model_name, values in zip(spreadsheet_ranges, databases):
            print_header(f'{model_name}: Importing these values from the spreadsheet')

            header = values[0]
            values_as_a_dict = [dict(zip(header, row)) for row in values[1:]]
            populate_database(model_name, values_as_a_dict, photo_url_lookup)

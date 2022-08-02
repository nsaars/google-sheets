from httplib2 import Http
from apiclient import discovery
from googleapiclient.discovery import Resource
from oauth2client.service_account import ServiceAccountCredentials


class SheetsAuthorizer:
    def __init__(self, credentials_file):
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(
            credentials_file,
            ['https://www.googleapis.com/auth/spreadsheets',
             'https://www.googleapis.com/auth/drive'])

        http_auth = self.credentials.authorize(Http())
        self.service = discovery.build('sheets', 'v4', http=http_auth)

    async def get_service(self):
        return self.service

    async def get_credentials(self):
        return self.credentials.to_json()


class Table:
    def __init__(self, service: Resource, spreadsheet_id):
        self.service = service
        self.spreadsheet_id = spreadsheet_id

    async def read(self, sheet_name=None, start_ceil=None, end_ceil=None, major_dimension=None) -> dict:
        if sheet_name is None:
            if start_ceil is None or end_ceil is None:
                raise TypeError("You have to define at least 'sheet_name' or 'start_ceil' and 'end_ceil'")

        if sheet_name is None:
            values_range = f'{start_ceil}:{end_ceil}'
        elif start_ceil is None:
            values_range = sheet_name
        else:
            values_range = f'{sheet_name}!{start_ceil}:{end_ceil}'

        if major_dimension is None:
            major_dimension = 'ROWS'

        response: dict = self.service.spreadsheets().values().get(
            spreadsheetId=self.spreadsheet_id,
            range=values_range,
            majorDimension=major_dimension
        ).execute()

        return response

    async def write(self, data, start_ceil=None, end_ceil=None):
        if start_ceil is None or end_ceil is None:
            raise TypeError("You have to define both 'start_ceil' and 'end_ceil'")
        response: dict = self.service.spreadsheets().values().update(
            spreadsheetId=self.spreadsheet_id,
            range=f"{start_ceil}:{end_ceil}",
            valueInputOption="USER_ENTERED",
            body={'values': data}
        ).execute()
        return response

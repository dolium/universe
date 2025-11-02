import os
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv

load_dotenv()


class GoogleSheetsService:
    def __init__(self):
        self.sheet_id = os.getenv('GOOGLE_SHEET_ID')
        self.credentials_file = os.getenv('GOOGLE_CREDENTIALS_FILE', 'credentials.json')
        self.client = None

    def authenticate(self):
        """Authenticate with Google Sheets API"""
        try:
            scopes = [
                'https://www.googleapis.com/auth/spreadsheets.readonly',
                'https://www.googleapis.com/auth/drive.readonly'
            ]

            # Check if credentials file exists
            if os.path.exists(self.credentials_file):
                creds = Credentials.from_service_account_file(
                    self.credentials_file,
                    scopes=scopes
                )
                self.client = gspread.authorize(creds)
                return True
            else:
                print(f"Credentials file not found: {self.credentials_file}")
                return False
        except Exception as e:
            print(f"Authentication error: {e}")
            return False

    def get_courses(self):
        """Fetch courses from Google Sheet"""
        try:
            if not self.client:
                if not self.authenticate():
                    return self._get_dummy_courses()

            if not self.sheet_id:
                print("GOOGLE_SHEET_ID not set in .env")
                return self._get_dummy_courses()

            # Open the spreadsheet
            sheet = self.client.open_by_key(self.sheet_id)
            worksheet = sheet.get_worksheet(0)  # Get first worksheet

            # Get all records (assumes first row is headers)
            records = worksheet.get_all_records()

            # Transform records into course data
            courses = []
            for record in records:
                course = {
                    'name': record.get('Course', ''),
                    'professor': record.get('Professor', ''),
                    'description': record.get('Description', ''),
                    'icon': record.get('Icon', 'default'),  # Icon type identifier
                }
                if course['name']:  # Only add if name exists
                    courses.append(course)

            return courses

        except Exception as e:
            print(f"Error fetching courses: {e}")
            return self._get_dummy_courses()

    def _get_dummy_courses(self):
        """Return dummy courses as fallback"""
        return [
            {
                'name': 'Mathematics II',
                'professor': 'Prof. Buhl',
                'description': 'Advanced calculus, linear algebra, and differential equations for engineering students.',
                'icon': 'math'
            },
            {
                'name': 'Physics I',
                'professor': 'Prof. Schmidt',
                'description': 'Classical mechanics, thermodynamics, and wave phenomena with laboratory work.',
                'icon': 'physics'
            },
            {
                'name': 'Chemistry Fundamentals',
                'professor': 'Prof. Weber',
                'description': 'Organic and inorganic chemistry principles with hands-on experiments.',
                'icon': 'chemistry'
            },
            {
                'name': 'Biology & Ecology',
                'professor': 'Prof. Mueller',
                'description': 'Molecular biology, genetics, and ecosystem studies with field research.',
                'icon': 'biology'
            },
            {
                'name': 'Computer Science I',
                'professor': 'Prof. Fischer',
                'description': 'Programming fundamentals, data structures, and algorithm design.',
                'icon': 'cs'
            },
            {
                'name': 'Engineering Design',
                'professor': 'Prof. Becker',
                'description': 'Principles of engineering design, CAD modeling, and project development.',
                'icon': 'engineering'
            },
        ]


# Create a singleton instance
sheets_service = GoogleSheetsService()


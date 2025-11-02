import os
import re
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv

load_dotenv()


class GoogleSheetsService:
    def __init__(self):
        self.sheet_id = os.getenv('GOOGLE_SHEET_ID')
        self.credentials_file = os.getenv('GOOGLE_CREDENTIALS_FILE', 'credentials.json')
        self.materials_sheet_name = os.getenv('MATERIALS_SHEET_NAME', 'Materials')
        self.opportunities_sheet_name = os.getenv('OPPORTUNITIES_SHEET_NAME', 'Opportunities')
        self.client = None
        self.last_source = 'unknown'  # 'google' | 'dummy' | 'unknown'

    def _credentials_path(self):
        """Return absolute path to credentials file (robust to CWD)."""
        if os.path.isabs(self.credentials_file):
            return self.credentials_file
        base_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_dir, self.credentials_file)

    def _slugify(self, text: str) -> str:
        """Create URL-friendly slug from course name."""
        if not text:
            return ""
        slug = text.strip().lower()
        slug = re.sub(r"[^a-z0-9]+", "-", slug)
        slug = re.sub(r"-+", "-", slug).strip('-')
        return slug

    def authenticate(self):
        """Authenticate with Google Sheets API"""
        try:
            scopes = [
                'https://www.googleapis.com/auth/spreadsheets.readonly',
                'https://www.googleapis.com/auth/drive.readonly'
            ]

            cred_path = self._credentials_path()
            if os.path.exists(cred_path):
                creds = Credentials.from_service_account_file(
                    cred_path,
                    scopes=scopes
                )
                self.client = gspread.authorize(creds)
                return True
            else:
                print(f"Credentials file not found: {cred_path}")
                return False
        except Exception as e:
            print(f"Authentication error: {e}")
            return False

    def get_courses(self):
        """Fetch courses from Google Sheet"""
        try:
            if not self.client:
                if not self.authenticate():
                    self.last_source = 'dummy'
                    return self._get_dummy_courses()

            if not self.sheet_id:
                print("GOOGLE_SHEET_ID not set in .env")
                self.last_source = 'dummy'
                return self._get_dummy_courses()

            # Open the spreadsheet
            sheet = self.client.open_by_key(self.sheet_id)
            worksheet = sheet.get_worksheet(0)  # Get first worksheet

            # Get all records (assumes first row is headers)
            records = worksheet.get_all_records()

            # Transform records into course data
            courses = []
            for record in records:
                name = record.get('Course', '')
                course = {
                    'name': name,
                    'slug': self._slugify(name),
                    'professor': record.get('Professor', ''),
                    'description': record.get('Description', ''),
                    'icon': record.get('Icon', 'default'),
                }
                if course['name']:
                    courses.append(course)

            self.last_source = 'google'
            return courses

        except Exception as e:
            print(f"Error fetching courses: {e}")
            self.last_source = 'dummy'
            return self._get_dummy_courses()

    def get_course_by_slug(self, slug: str):
        """Return a single course dict by slug, or None if not found."""
        try:
            for course in self.get_courses():
                if course.get('slug') == slug:
                    return course
        except Exception as e:
            print(f"Error finding course by slug '{slug}': {e}")
        return None

    def is_using_google(self) -> bool:
        return self.last_source == 'google'

    def get_materials(self):
        """Fetch materials from 'Materials' worksheet. Returns list of dicts {course_slug,title,url}."""
        try:
            if not self.client:
                if not self.authenticate():
                    return self._get_dummy_materials()

            if not self.sheet_id:
                return self._get_dummy_materials()

            sheet = self.client.open_by_key(self.sheet_id)
            try:
                worksheet = sheet.worksheet(self.materials_sheet_name)
            except Exception:
                # If by name failed, try second sheet (index 1)
                try:
                    worksheet = sheet.get_worksheet(1)
                except Exception:
                    return self._get_dummy_materials()

            records = worksheet.get_all_records()
            mats = []
            for r in records:
                course_name = r.get('Course', '')
                title = r.get('Title', '') or r.get('Name', '')
                url = r.get('URL', '') or r.get('Link', '')
                if not (course_name and title and url):
                    continue
                mats.append({
                    'course_slug': self._slugify(course_name),
                    'title': title,
                    'url': url,
                })
            return mats
        except Exception as e:
            print(f"Error fetching materials: {e}")
            return self._get_dummy_materials()

    def get_course_materials(self, course_slug: str):
        """Return materials filtered by course slug."""
        try:
            return [m for m in self.get_materials() if m.get('course_slug') == course_slug]
        except Exception as e:
            print(f"Error filtering materials for '{course_slug}': {e}")
            return []

    def get_opportunities(self):
        """Fetch opportunities from 'Opportunities' worksheet. Returns list of dicts."""
        try:
            if not self.client:
                if not self.authenticate():
                    return self._get_dummy_opportunities()

            if not self.sheet_id:
                return self._get_dummy_opportunities()

            sheet = self.client.open_by_key(self.sheet_id)
            # Try by name, then fallback to a likely index (2: third tab)
            worksheet = None
            try:
                worksheet = sheet.worksheet(self.opportunities_sheet_name)
            except Exception:
                try:
                    worksheet = sheet.get_worksheet(2)
                except Exception:
                    return self._get_dummy_opportunities()

            records = worksheet.get_all_records()

            def pick(d, keys):
                for k in keys:
                    if k in d and d[k]:
                        return d[k]
                return ''

            items = []
            for r in records:
                title = pick(r, ['Title', 'Opportunity', 'Name'])
                type_ = pick(r, ['Type', 'Category'])
                programme = pick(r, ['Study Programme', 'StudyProgram', 'Programme', 'Program'])
                description = pick(r, ['Description', 'Details'])
                if not title:
                    continue
                items.append({
                    'title': title,
                    'type': type_,
                    'programme': programme,
                    'description': description,
                })
            return items
        except Exception as e:
            print(f"Error fetching opportunities: {e}")
            return self._get_dummy_opportunities()

    def _get_dummy_courses(self):
        """Return dummy courses as fallback"""
        dummy = [
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
        for c in dummy:
            c['slug'] = self._slugify(c['name'])
        return dummy

    def _get_dummy_materials(self):
        """Fallback materials list for demo purposes."""
        return [
            { 'course_slug': 'mathematics-ii', 'title': 'Exam Cheat Sheet (2024)', 'url': 'https://example.com/maths-cheatsheet.pdf' },
            { 'course_slug': 'physics-i', 'title': 'Lab Report Template', 'url': 'https://example.com/physics-lab-template.docx' },
            { 'course_slug': 'computer-science-i', 'title': 'Data Structures Notes', 'url': 'https://example.com/ds-notes' },
        ]

    def _get_dummy_opportunities(self):
        return [
            { 'title': 'Part‑time Lab Assistant', 'type': 'job', 'programme': 'Physics', 'description': 'Assist in undergraduate lab sessions 10h/week.' },
            { 'title': 'Hackathon Weekend', 'type': 'fun', 'programme': 'CS', 'description': '48‑hour hackathon with mentors and prizes.' },
            { 'title': 'Tutoring Group: Calculus', 'type': 'study', 'programme': 'Engineering', 'description': 'Weekly peer tutoring for Calculus I.' },
        ]


# Create a singleton instance
sheets_service = GoogleSheetsService()

import os
import re
from typing import List, Dict, Optional
import gspread
from google.oauth2.service_account import Credentials
from config import Config


class GoogleSheetsService:
    """
    Service class for interacting with Google Sheets API.
    Handles fetching courses, materials, and opportunities data.
    Falls back to dummy data if Google Sheets is not configured.
    """

    # Constants for data sources
    DATA_SOURCE_GOOGLE = 'google'
    DATA_SOURCE_FALLBACK = 'fallback'
    DATA_SOURCE_UNKNOWN = 'unknown'

    def __init__(self, config: Config = None):
        """
        Initialize the Google Sheets service with configuration.

        Args:
            config: Configuration object. If None, uses default Config.
        """
        if config is None:
            config = Config()

        self.spreadsheet_id = config.GOOGLE_SHEET_ID
        self.credentials_file_path = config.GOOGLE_CREDENTIALS_FILE
        self.materials_worksheet_name = config.MATERIALS_WORKSHEET_NAME
        self.opportunities_worksheet_name = config.OPPORTUNITIES_WORKSHEET_NAME
        self.professor_availability_worksheet_name = config.PROFESSOR_AVAILABILITY_WORKSHEET_NAME
        self.google_client = None
        self.current_data_source = self.DATA_SOURCE_UNKNOWN

    def _get_absolute_credentials_path(self) -> str:
        """
        Return absolute path to credentials file (robust to current working directory changes).

        Returns:
            str: Absolute path to the credentials JSON file
        """
        if os.path.isabs(self.credentials_file_path):
            return self.credentials_file_path
        current_directory = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(current_directory, self.credentials_file_path)

    def _create_url_slug(self, text: str) -> str:
        """
        Create URL-friendly slug from text (typically course names).

        Args:
            text: The text to convert to a slug

        Returns:
            str: URL-safe slug string (lowercase, hyphen-separated)

        Example:
            "Mathematics II" -> "mathematics-ii"
        """
        if not text:
            return ""
        slug = text.strip().lower()
        # Replace non-alphanumeric characters with hyphens
        slug = re.sub(r"[^a-z0-9]+", "-", slug)
        # Remove duplicate hyphens and trim leading/trailing hyphens
        slug = re.sub(r"-+", "-", slug).strip('-')
        return slug

    def authenticate_with_google(self) -> bool:
        """
        Authenticate with Google Sheets API using service account credentials.

        Returns:
            bool: True if authentication successful, False otherwise
        """
        try:
            required_scopes = [
                'https://www.googleapis.com/auth/spreadsheets.readonly',
                'https://www.googleapis.com/auth/drive.readonly'
            ]

            credentials_path = self._get_absolute_credentials_path()
            if not os.path.exists(credentials_path):
                print(f"[WARNING] Credentials file not found: {credentials_path}")
                return False

            credentials = Credentials.from_service_account_file(
                credentials_path,
                scopes=required_scopes
            )
            self.google_client = gspread.authorize(credentials)
            return True

        except Exception as error:
            print(f"[ERROR] Authentication failed: {error}")
            return False

    def get_courses(self) -> List[Dict[str, str]]:
        """
        Fetch all courses from Google Sheet or fallback data.

        Returns:
            List[Dict]: List of course dictionaries with keys: name, slug, professor, description, icon
        """
        try:
            # Ensure client is authenticated
            if not self.google_client:
                if not self.authenticate_with_google():
                    self.current_data_source = self.DATA_SOURCE_FALLBACK
                    return self._get_fallback_courses()

            # Verify spreadsheet ID is configured
            if not self.spreadsheet_id:
                print("[WARNING] GOOGLE_SHEET_ID not set in .env file")
                self.current_data_source = self.DATA_SOURCE_FALLBACK
                return self._get_fallback_courses()

            # Open the spreadsheet and get first worksheet (courses)
            spreadsheet = self.google_client.open_by_key(self.spreadsheet_id)
            courses_worksheet = spreadsheet.get_worksheet(0)

            # Get all records (assumes first row contains headers)
            raw_records = courses_worksheet.get_all_records()

            # Transform raw records into standardized course data
            courses = []
            for record in raw_records:
                course_name = record.get('Course', '').strip()
                if not course_name:
                    continue

                course = {
                    'name': course_name,
                    'slug': self._create_url_slug(course_name),
                    'professor': record.get('Professor', '').strip(),
                    'description': record.get('Description', '').strip(),
                    'icon': record.get('Icon', 'default').strip(),
                }
                courses.append(course)

            self.current_data_source = self.DATA_SOURCE_GOOGLE
            return courses

        except Exception as error:
            print(f"[ERROR] Failed to fetch courses: {error}")
            self.current_data_source = self.DATA_SOURCE_FALLBACK
            return self._get_fallback_courses()

    def get_course_by_slug(self, slug: str) -> Optional[Dict[str, str]]:
        """
        Find and return a single course by its URL slug.

        Args:
            slug: URL-friendly slug identifier for the course

        Returns:
            Dict or None: Course dictionary if found, None otherwise
        """
        try:
            all_courses = self.get_courses()
            for course in all_courses:
                if course.get('slug') == slug:
                    return course
        except Exception as error:
            print(f"[ERROR] Failed to find course with slug '{slug}': {error}")
        return None

    def is_using_google_sheets(self) -> bool:
        """
        Check if the service is currently using Google Sheets as data source.

        Returns:
            bool: True if using Google Sheets, False if using fallback data
        """
        return self.current_data_source == self.DATA_SOURCE_GOOGLE

    def get_materials(self) -> List[Dict[str, str]]:
        """
        Fetch all course materials from 'Materials' worksheet.

        Returns:
            List[Dict]: List of material dictionaries with keys: course_slug, title, url
        """
        try:
            # Ensure client is authenticated
            if not self.google_client:
                if not self.authenticate_with_google():
                    return self._get_fallback_materials()

            if not self.spreadsheet_id:
                return self._get_fallback_materials()

            spreadsheet = self.google_client.open_by_key(self.spreadsheet_id)

            # Try to get worksheet by name, fallback to index-based access
            try:
                materials_worksheet = spreadsheet.worksheet(self.materials_worksheet_name)
            except Exception:
                # If by name failed, try second worksheet (index 1)
                try:
                    materials_worksheet = spreadsheet.get_worksheet(1)
                except Exception:
                    return self._get_fallback_materials()

            raw_records = materials_worksheet.get_all_records()
            materials = []

            for record in raw_records:
                course_name = record.get('Course', '').strip()
                # Try multiple possible column names for flexibility
                title = (record.get('Title', '') or record.get('Name', '')).strip()
                url = (record.get('URL', '') or record.get('Link', '')).strip()

                # Skip incomplete records
                if not (course_name and title and url):
                    continue

                materials.append({
                    'course_slug': self._create_url_slug(course_name),
                    'title': title,
                    'url': url,
                })
            return materials

        except Exception as error:
            print(f"[ERROR] Failed to fetch materials: {error}")
            return self._get_fallback_materials()

    def get_course_materials(self, course_slug: str) -> List[Dict[str, str]]:
        """
        Get all materials for a specific course.

        Args:
            course_slug: URL slug of the course

        Returns:
            List[Dict]: List of materials belonging to the specified course
        """
        try:
            all_materials = self.get_materials()
            course_materials = [
                material for material in all_materials
                if material.get('course_slug') == course_slug
            ]
            return course_materials
        except Exception as error:
            print(f"[ERROR] Failed to filter materials for course '{course_slug}': {error}")
            return []

    def get_opportunities(self) -> List[Dict[str, str]]:
        """
        Fetch all opportunities from 'Opportunities' worksheet.

        Returns:
            List[Dict]: List of opportunity dictionaries with keys: title, type, programme, description
        """
        try:
            # Ensure client is authenticated
            if not self.google_client:
                if not self.authenticate_with_google():
                    return self._get_fallback_opportunities()

            if not self.spreadsheet_id:
                return self._get_fallback_opportunities()

            spreadsheet = self.google_client.open_by_key(self.spreadsheet_id)

            # Try to get worksheet by name, fallback to index-based access (third tab)
            try:
                opportunities_worksheet = spreadsheet.worksheet(self.opportunities_worksheet_name)
            except Exception:
                try:
                    opportunities_worksheet = spreadsheet.get_worksheet(2)
                except Exception:
                    return self._get_fallback_opportunities()

            raw_records = opportunities_worksheet.get_all_records()
            opportunities = []

            for record in raw_records:
                # Extract data with flexible column name matching
                title = self._extract_field_value(record, ['Title', 'Opportunity', 'Name'])
                opportunity_type = self._extract_field_value(record, ['Type', 'Category'])
                programme = self._extract_field_value(record, ['Study Programme', 'StudyProgram', 'Programme', 'Program'])
                description = self._extract_field_value(record, ['Description', 'Details'])

                # Skip records without a title
                if not title:
                    continue

                opportunities.append({
                    'title': title,
                    'type': opportunity_type,
                    'programme': programme,
                    'description': description,
                })

            return opportunities

        except Exception as error:
            print(f"[ERROR] Failed to fetch opportunities: {error}")
            return self._get_fallback_opportunities()

    def _extract_field_value(self, record: Dict, possible_keys: List[str]) -> str:
        """
        Extract a field value from a record, trying multiple possible column names.

        Args:
            record: Dictionary record from spreadsheet
            possible_keys: List of possible column names to try

        Returns:
            str: First non-empty value found, or empty string
        """
        for key in possible_keys:
            if key in record and record[key]:
                return str(record[key]).strip()
        return ''

    def _get_fallback_courses(self) -> List[Dict[str, str]]:
        """
        Return fallback course data when Google Sheets is unavailable.

        Returns:
            List[Dict]: List of sample course dictionaries
        """
        fallback_courses = [
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
        # Generate slugs for all fallback courses
        for course in fallback_courses:
            course['slug'] = self._create_url_slug(course['name'])
        return fallback_courses

    def _get_fallback_materials(self) -> List[Dict[str, str]]:
        """
        Return fallback materials data when Google Sheets is unavailable.

        Returns:
            List[Dict]: List of sample material dictionaries
        """
        return [
            { 'course_slug': 'mathematics-ii', 'title': 'Exam Cheat Sheet (2024)', 'url': 'https://example.com/maths-cheatsheet.pdf' },
            { 'course_slug': 'physics-i', 'title': 'Lab Report Template', 'url': 'https://example.com/physics-lab-template.docx' },
            { 'course_slug': 'computer-science-i', 'title': 'Data Structures Notes', 'url': 'https://example.com/ds-notes' },
        ]

    def _get_fallback_opportunities(self) -> List[Dict[str, str]]:
        """
        Return fallback opportunities data when Google Sheets is unavailable.

        Returns:
            List[Dict]: List of sample opportunity dictionaries
        """
        return [
            { 'title': 'Part‑time Lab Assistant', 'type': 'job', 'programme': 'Physics', 'description': 'Assist in undergraduate lab sessions 10h/week.' },
            { 'title': 'Hackathon Weekend', 'type': 'fun', 'programme': 'CS', 'description': '48‑hour hackathon with mentors and prizes.' },
            { 'title': 'Tutoring Group: Calculus', 'type': 'study', 'programme': 'Engineering', 'description': 'Weekly peer tutoring for Calculus I.' },
        ]

    def _norm(self, s: str) -> str:
        """Normalize strings for comparison (strip, collapse spaces, lowercase)."""
        if s is None:
            return ''
        return ' '.join(str(s).strip().split()).lower()

    def _detect_program_sem_key(self, keys: List[str]) -> Optional[str]:
        """
        Try to detect the Program/Semester-like column key.
        Accepts variants like 'Program/Semester', 'Programm/Semester', 'Studiengang/Semester',
        or any key that has tokens for program/studien and sem/semester.
        """
        if not keys:
            return None
        # Strong candidates (common exact headers)
        preferred = [
            'Program/Semester', 'Programm/Semester', 'Studiengang/Semester',
            'Program - Semester', 'Programm - Semester'
        ]
        for k in keys:
            if any(self._norm(k) == self._norm(p) for p in preferred):
                return k
        # Regex-based fallback
        pattern = re.compile(r"(program|programm|studien\w*)\s*[/\-]?\s*(sem|semester)", re.IGNORECASE)
        for k in keys:
            if pattern.search(str(k)):
                return k
        # Separate columns fallback (if present): combine 'Program(me|m|Studiengang)' + 'Semester'
        # We'll handle combination later during merge if needed
        return None

    def _merge_timetable_by_program_sem(self, entries: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        Merge rows that are identical across all columns except the Program/Semester column.
        Concatenate Program/Semester values with '/' in the resulting single row.
        """
        if not entries:
            return entries

        # Detect program/semester column
        keys = list(entries[0].keys())
        program_key = self._detect_program_sem_key(keys)

        # If Program/Semester column not found, try to build a synthetic key from separate columns
        separate_program_keys = []
        semester_key = None
        if program_key is None:
            # find program-like
            for k in keys:
                kl = self._norm(k)
                if ('program' in kl or 'programm' in kl or 'studien' in kl) and 'sem' not in kl:
                    separate_program_keys.append(k)
                if semester_key is None and ('semester' in kl or kl.endswith('sem')):
                    semester_key = k

        # If neither combined nor separate found, nothing to merge
        can_merge = program_key is not None or (separate_program_keys and semester_key)
        if not can_merge:
            return entries

        def build_group_key(entry: Dict[str, str]) -> tuple:
            items = []
            for k, v in entry.items():
                if program_key:
                    if k == program_key:
                        continue
                else:
                    # skip separate components when building grouping key
                    if k in separate_program_keys or k == semester_key:
                        continue
                items.append((k, self._norm(v)))
            # sort to make deterministic
            return tuple(sorted(items, key=lambda x: x[0]))

        def get_program_value(entry: Dict[str, str]) -> str:
            if program_key:
                return str(entry.get(program_key, '')).strip()
            # Combine separate components into one display string like "{Program}/{Semester}" or "{Program} {Semester}"
            parts = []
            # Some rows might have multiple program-like columns; concatenate them with space
            prog_parts = [str(entry.get(k, '')).strip() for k in separate_program_keys if str(entry.get(k, '')).strip()]
            if prog_parts:
                parts.append(' '.join(prog_parts))
            sem_val = str(entry.get(semester_key, '')).strip()
            if sem_val:
                # Use dot between program and semester if both exist, else just semester
                if parts:
                    parts[-1] = f"{parts[-1]}.{sem_val}"
                else:
                    parts.append(sem_val)
            return '/'.join([p for p in parts if p])

        merged = []
        index = {}  # group_key -> idx in merged
        value_sets = {}  # idx -> set of normalized program values

        for entry in entries:
            gk = build_group_key(entry)
            prog_val_raw = get_program_value(entry)
            prog_val_norm = self._norm(prog_val_raw)

            if gk in index:
                i = index[gk]
                # Append program value if new
                if prog_val_norm and prog_val_norm not in value_sets[i]:
                    value_sets[i].add(prog_val_norm)
                    # merge display string
                    display = merged[i].get(program_key or 'Program/Semester', '')
                    if display:
                        display = f"{display}/{prog_val_raw}"
                    else:
                        display = prog_val_raw
                    # set back to appropriate key
                    if program_key:
                        merged[i][program_key] = display
                    else:
                        # create synthetic combined column if needed
                        merged[i]['Program/Semester'] = display
                # else nothing to add
            else:
                # New group: clone row and initialize program value
                new_row = dict(entry)
                if program_key:
                    new_row[program_key] = prog_val_raw
                else:
                    # ensure synthetic column exists and drop separate columns? Keep them for display consistency.
                    new_row['Program/Semester'] = prog_val_raw
                merged.append(new_row)
                idx = len(merged) - 1
                index[gk] = idx
                value_sets[idx] = set()
                if prog_val_norm:
                    value_sets[idx].add(prog_val_norm)
        return merged

    def get_professor_availability(self) -> List[Dict[str, str]]:
        """
        Fetch all professor availability entries from 'Timetable' worksheet.

        Returns:
            List[Dict]: List of availability dictionaries with all column data
        """
        try:
            # Ensure client is authenticated
            if not self.google_client:
                if not self.authenticate_with_google():
                    return self._get_fallback_professor_availability()

            if not self.spreadsheet_id:
                return self._get_fallback_professor_availability()

            spreadsheet = self.google_client.open_by_key(self.spreadsheet_id)

            # Try to get worksheet by name
            try:
                timetable_worksheet = spreadsheet.worksheet(self.professor_availability_worksheet_name)
            except Exception as e:
                print(f"[WARNING] Could not find '{self.professor_availability_worksheet_name}' worksheet: {e}")
                return self._get_fallback_professor_availability()

            raw_records = timetable_worksheet.get_all_records()
            availability_entries = []

            for record in raw_records:
                entry = {}
                for key, value in record.items():
                    entry[key] = str(value).strip() if value else ''
                if any(entry.values()):
                    availability_entries.append(entry)

            # Merge duplicates differing only in Program/Semester
            availability_entries = self._merge_timetable_by_program_sem(availability_entries)

            return availability_entries

        except Exception as error:
            print(f"[ERROR] Failed to fetch professor availability: {error}")
            return self._get_fallback_professor_availability()

    def _get_fallback_professor_availability(self) -> List[Dict[str, str]]:
        """
        Return fallback professor availability data when Google Sheets is unavailable.

        Returns:
            List[Dict]: List of sample availability dictionaries
        """
        return [
            { 'Tag': 'Montag', 'Zeit': '08:00-10:00', 'Fach': 'Mathematik II', 'Professor': 'Prof. Buhl', 'Raum': 'A101' },
            { 'Tag': 'Montag', 'Zeit': '10:15-12:00', 'Fach': 'Physik I', 'Professor': 'Prof. Schmidt', 'Raum': 'B205' },
            { 'Tag': 'Dienstag', 'Zeit': '08:00-10:00', 'Fach': 'Informatik I', 'Professor': 'Prof. Fischer', 'Raum': 'C302' },
            { 'Tag': 'Mittwoch', 'Zeit': '14:00-16:00', 'Fach': 'Chemie', 'Professor': 'Prof. Weber', 'Raum': 'Lab 1' },
        ]


# Create a singleton instance
sheets_service = GoogleSheetsService()

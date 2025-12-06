#IDEA: CREATE A TIMETABLE BUT FOR EACH PROFESSOR SO YOU CAN SEE THE PROFESSORS' SCHEDULES



"""
Flask application for UniVerse - A social-academic hub for students.
Provides courses, materials, and opportunities management.
"""
from typing import Dict, List
from flask import Flask, render_template, abort, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import bcrypt
from config import get_config
from google_sheets_service import sheets_service


class User(UserMixin):
    """User class for Flask-Login."""
    def __init__(self, email: str, name: str = ''):
        self.id = email
        self.email = email
        self.name = name

    @staticmethod
    def get(email: str):
        """Get user by email from Google Sheets."""
        user_data = sheets_service.get_user_by_email(email)
        if user_data:
            return User(user_data['email'], user_data['name'])
        return None


def create_app(config_name: str = None) -> Flask:
    """
    Create and configure the Flask application.

    Args:
        config_name: Configuration environment name (development, production, testing)

    Returns:
        Flask: Configured Flask application instance
    """
    application = Flask(__name__)

    # Load configuration
    config = get_config(config_name)
    application.config.from_object(config)

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(application)
    login_manager.login_view = 'login'
    login_manager.login_message = 'Please log in to access this page.'

    @login_manager.user_loader
    def load_user(email):
        return User.get(email)

    def get_common_template_context() -> Dict[str, str]:
        """
        Get common context variables used across all templates.

        Returns:
            Dict: Common template context with site name and analytics ID
        """
        return {
            'site_name': config.APP_NAME,
            'ga_id': config.GOOGLE_ANALYTICS_ID,
            'current_user': current_user,
        }

    @application.route('/')
    def index():
        """Render the main landing page."""
        return render_template('index.html', **get_common_template_context())

    @application.route('/courses')
    def courses():
        """Render the courses listing page with optional filtering by study programme."""
        all_courses = sheets_service.get_courses()

        # Собираем уникальные программы из курсов
        available_programmes = _extract_unique_values(all_courses, 'programme')

        # Множественный выбор программ: ?programme=CS&programme=Math
        selected_programmes = request.args.getlist('programme')
        selected_programmes_norm = {p.strip().lower() for p in selected_programmes if p.strip()}

        if selected_programmes_norm:
            def _matches_programme(course: Dict) -> bool:
                prog = (course.get('programme') or '').strip().lower()
                return prog in selected_programmes_norm

            filtered_courses = [c for c in all_courses if _matches_programme(c)]
        else:
            filtered_courses = all_courses

        template_context = get_common_template_context()
        template_context.update({
            'courses': filtered_courses,
            'filters_programmes': available_programmes,
            'selected_programmes': list(selected_programmes_norm),
            'total_courses_count': len(all_courses),
        })

        return render_template('courses.html', **template_context)

    @application.route('/opportunities')
    def opportunities():
        """Render the opportunities page with filtering capabilities.
        Supports filtering by type and multiple programmes from query parameters.
        """
        all_opportunities = sheets_service.get_opportunities()

        # Extract unique filter options from current data
        available_types = _extract_unique_values(all_opportunities, 'type')
        available_programmes = _extract_unique_values(all_opportunities, 'programme')

        # Get filter parameters from request
        selected_type = request.args.get('type', '').strip()
        selected_programmes = request.args.getlist('programme')
        selected_programmes_norm = {p.strip().lower() for p in selected_programmes if p.strip()}

        # Apply filters
        filtered_opportunities = _filter_opportunities(
            all_opportunities,
            selected_type,
            selected_programmes_norm
        )

        template_context = get_common_template_context()
        template_context.update({
            'opportunities': filtered_opportunities,
            'opportunities_form_url': config.ADD_OPPORTUNITY_SHEET_URL,
            'filters_types': available_types,
            'filters_programmes': available_programmes,
            'selected_type': selected_type,
            'selected_programmes': list(selected_programmes_norm),
            'total_count': len(all_opportunities)
        })

        return render_template('opportunities.html', **template_context)

    def _extract_unique_values(items: List[Dict], field_name: str) -> List[str]:
        """
        Extract unique non-empty values for a specific field from a list of dictionaries.

        Args:
            items: List of dictionaries
            field_name: Name of the field to extract

        Returns:
            List[str]: Sorted list of unique values
        """
        unique_values = {
            (item.get(field_name) or '').strip()
            for item in items
            if (item.get(field_name) or '').strip()
        }
        return sorted(unique_values)

    def _filter_opportunities(
        opportunities: List[Dict],
        filter_type: str,
        filter_programmes: set
    ) -> List[Dict]:
        """Filter opportunities by type and/or a set of programmes (case-insensitive)."""
        filtered = opportunities

        if filter_type:
            filtered = [
                opp for opp in filtered
                if (opp.get('type') or '').strip().lower() == filter_type.lower()
            ]

        if filter_programmes:
            filtered = [
                opp for opp in filtered
                if (opp.get('programme') or '').strip().lower() in filter_programmes
            ]

        return filtered

    @application.route('/courses/<slug>')
    def course_detail(slug: str):
        """
        Render the detailed page for a specific course.

        Args:
            slug: URL-friendly course identifier

        Returns:
            Rendered template or 404 error if course not found
        """
        course = sheets_service.get_course_by_slug(slug)

        if not course:
            abort(404)

        # Load materials associated with this course
        course_materials = sheets_service.get_course_materials(slug)

        template_context = get_common_template_context()
        template_context.update({
            'course': course,
            'materials': course_materials,
            'materials_form_url': config.ADD_MATERIAL_SHEET_URL
        })

        return render_template('course_detail.html', **template_context)

    @application.route('/timetable')
    def timetable():
        """
        Render the professor availability page with filtering capabilities.
        Supports filtering by professor, day and search query from query parameters.
        """
        all_entries = sheets_service.get_professor_availability()

        # Extract unique professors and days from current data
        available_professors = _extract_unique_professors(all_entries)
        professor_options = [{ 'value': _normalize_prof_name(p), 'label': p } for p in available_professors]
        available_days = _extract_unique_days(all_entries)
        day_options = [{ 'value': _normalize_day_value(d), 'label': d } for d in available_days]

        # Get filter parameters from request
        selected_professor = request.args.get('professor', '').strip()
        selected_professor_value = _normalize_prof_name(selected_professor)
        selected_day = request.args.get('day', '').strip()
        selected_day_value = _normalize_day_value(selected_day)
        search_query = request.args.get('search', '').strip()

        # Apply filters
        filtered_entries = _filter_availability(
            all_entries,
            selected_professor,
            selected_day,
            search_query
        )

        template_context = get_common_template_context()
        template_context.update({
            'availability_entries': filtered_entries,
            'filters_professors': available_professors,
            'professor_options': professor_options,
            'filters_days': available_days,
            'day_options': day_options,
            'selected_professor': selected_professor,
            'selected_professor_value': selected_professor_value,
            'selected_day': selected_day,
            'selected_day_value': selected_day_value,
            'search_query': search_query,
            'total_count': len(all_entries)
        })

        return render_template('timetable.html', **template_context)

    # --- Professor Availability helpers (professor and day detection) ---
    PROFESSOR_KEY_TOKENS = (
        'prof',        # Professor, Professor/in
        'dozent',      # Dozent, Dozent/in
        'lehr',        # Lehrer, Lehrperson, Lehrkraft
        'dozier',      # Dozierende
        'unterricht',  # Unterrichtende
    )

    DAY_KEY_TOKENS = (
        'tag',        # Tag, Wochentag
        'woch',       # Woche, Wochentag
        'day',        # Day, Weekday
        'wochen',
    )

    def _get_professor_name(entry: Dict) -> str:
        """
        Extract professor name from availability entry by checking common German/English key variants.
        It detects keys that CONTAIN tokens like 'prof', 'dozent', 'lehr', etc. (case-insensitive).
        """
        # Direct fast-path for common names
        val = (entry.get('Professor') or entry.get('Dozent') or entry.get('Lehrer') or
               entry.get('Professor/in') or entry.get('Dozent/in') or entry.get('Lehrperson') or
               entry.get('Lehrkraft') or entry.get('Dozierende') or '')
        val = str(val).strip() if val else ''
        if val:
            return val
        # Fallback: scan keys for token matches
        for key, value in entry.items():
            key_lower = str(key).lower()
            if any(token in key_lower for token in PROFESSOR_KEY_TOKENS):
                v = str(value).strip() if value else ''
                if v:
                    return v
        return ''

    def _get_day_value(entry: Dict) -> str:
        """Extract day-of-week value from availability entry using common key variants."""
        val = (entry.get('Tag') or entry.get('Wochentag') or entry.get('Day') or entry.get('Weekday') or '')
        val = str(val).strip() if val else ''
        if val:
            return val
        for key, value in entry.items():
            key_lower = str(key).lower()
            if any(token in key_lower for token in DAY_KEY_TOKENS):
                v = str(value).strip() if value else ''
                if v:
                    return v
        return ''

    def _normalize_prof_name(name: str) -> str:
        """Normalize professor name for consistent comparison (strip, collapse spaces)."""
        if not name:
            return ''
        return ' '.join(name.strip().split())

    def _normalize_day_value(name: str) -> str:
        """Normalize day value (strip, collapse spaces, lowercase)."""
        if not name:
            return ''
        return ' '.join(str(name).strip().split()).lower()

    def _extract_unique_professors(entries: List[Dict]) -> List[str]:
        """Extract unique professor names from availability entries (normalized, original preserved)."""
        professors = {}
        for entry in entries:
            prof_raw = _get_professor_name(entry)
            prof_norm = _normalize_prof_name(prof_raw)
            if prof_norm and prof_norm not in professors:
                professors[prof_norm] = prof_raw  # keep original formatting
        return [professors[k] for k in sorted(professors.keys())]

    def _extract_unique_days(entries: List[Dict]) -> List[str]:
        """Extract unique day values from availability entries (normalized, original preserved)."""
        days = {}
        for entry in entries:
            day_raw = _get_day_value(entry)
            day_norm = _normalize_day_value(day_raw)
            if day_norm and day_norm not in days:
                days[day_norm] = day_raw
        # order by the common German weekday order if possible, otherwise alpha
        order_map = {
            'montag': 1, 'dienstag': 2, 'mittwoch': 3, 'donnerstag': 4, 'freitag': 5, 'samstag': 6, 'sonntag': 7
        }
        return [days[k] for k in sorted(days.keys(), key=lambda x: (order_map.get(x, 99), x))]

    def _filter_availability(
        entries: List[Dict],
        filter_professor: str,
        filter_day: str,
        search_query: str
    ) -> List[Dict]:
        """Filter availability entries by professor, day and/or search query (normalized)."""
        filtered = entries
        if filter_professor:
            fp_norm = _normalize_prof_name(filter_professor).lower()
            filtered = [
                e for e in filtered
                if _normalize_prof_name(_get_professor_name(e)).lower() == fp_norm
            ]
        if filter_day:
            fd_norm = _normalize_day_value(filter_day)
            filtered = [
                e for e in filtered
                if _normalize_day_value(_get_day_value(e)) == fd_norm
            ]
        if search_query:
            q = search_query.lower().strip()
            if q:
                filtered = [
                    e for e in filtered
                    if q in _normalize_prof_name(_get_professor_name(e)).lower()
                ]
        return filtered

    @application.route('/login', methods=['GET', 'POST'])
    def login():
        """Render login page and handle login form submission."""
        if current_user.is_authenticated:
            return redirect(url_for('index'))

        if request.method == 'POST':
            email = request.form.get('email', '').strip()
            password = request.form.get('password', '')

            if not email or not password:
                flash('Please provide both email and password.', 'error')
                return render_template('login.html', **get_common_template_context())

            # Get user from Google Sheets
            user_data = sheets_service.get_user_by_email(email)

            if not user_data:
                flash('Invalid email or password.', 'error')
                return render_template('login.html', **get_common_template_context())

            # Verify password
            password_hash = user_data['password_hash']
            if bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8')):
                user = User(user_data['email'], user_data['name'])
                login_user(user)
                flash(f'Welcome back, {user.name}!', 'success')

                # Redirect to next page or index
                next_page = request.args.get('next')
                return redirect(next_page if next_page else url_for('index'))
            else:
                flash('Invalid email or password.', 'error')

        return render_template('login.html', **get_common_template_context())

    @application.route('/register', methods=['GET', 'POST'])
    def register():
        """Render registration page and handle registration form submission."""
        if current_user.is_authenticated:
            return redirect(url_for('index'))

        if request.method == 'POST':
            name = request.form.get('name', '').strip()
            email = request.form.get('email', '').strip()
            password = request.form.get('password', '')
            confirm_password = request.form.get('confirm_password', '')

            # Validation
            if not all([name, email, password, confirm_password]):
                flash('All fields are required.', 'error')
                return render_template('register.html', **get_common_template_context())

            if password != confirm_password:
                flash('Passwords do not match.', 'error')
                return render_template('register.html', **get_common_template_context())

            if len(password) < 6:
                flash('Password must be at least 6 characters long.', 'error')
                return render_template('register.html', **get_common_template_context())

            # Check if user already exists
            if sheets_service.get_user_by_email(email):
                flash('An account with this email already exists.', 'error')
                return render_template('register.html', **get_common_template_context())

            # Hash password
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            # Create user in Google Sheets
            if sheets_service.create_user(email, password_hash, name):
                flash('Registration successful! Please log in.', 'success')
                return redirect(url_for('login'))
            else:
                flash('Registration failed. Please try again later.', 'error')

        return render_template('register.html', **get_common_template_context())

    @application.route('/logout')
    @login_required
    def logout():
        """Log out the current user."""
        logout_user()
        flash('You have been logged out.', 'info')
        return redirect(url_for('index'))

    return application


# Create application instance
app = create_app()

if __name__ == '__main__':
    # Run development server
    app.run(debug=True)

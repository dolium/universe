"""
Flask application for UniVerse - A social-academic hub for students.
Provides courses, materials, and opportunities management.
"""
from typing import Dict, List
from flask import Flask, render_template, abort, request
from config import get_config
from google_sheets_service import sheets_service


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

    def get_common_template_context() -> Dict[str, str]:
        """
        Get common context variables used across all templates.

        Returns:
            Dict: Common template context with site name and analytics ID
        """
        return {
            'site_name': config.APP_NAME,
            'ga_id': config.GOOGLE_ANALYTICS_ID,
        }

    @application.route('/')
    def index():
        """Render the main landing page."""
        return render_template('index.html', **get_common_template_context())

    @application.route('/courses')
    def courses():
        """
        Render the courses listing page.
        Fetches all courses from Google Sheets or fallback data.
        """
        all_courses = sheets_service.get_courses()

        template_context = get_common_template_context()
        template_context['courses'] = all_courses

        return render_template('courses.html', **template_context)

    @application.route('/opportunities')
    def opportunities():
        """
        Render the opportunities page with filtering capabilities.
        Supports filtering by type and programme from query parameters.
        """
        all_opportunities = sheets_service.get_opportunities()

        # Extract unique filter options from current data
        available_types = _extract_unique_values(all_opportunities, 'type')
        available_programmes = _extract_unique_values(all_opportunities, 'programme')

        # Get filter parameters from request
        selected_type = request.args.get('type', '').strip()
        selected_programme = request.args.get('programme', '').strip()

        # Apply filters
        filtered_opportunities = _filter_opportunities(
            all_opportunities,
            selected_type,
            selected_programme
        )

        template_context = get_common_template_context()
        template_context.update({
            'opportunities': filtered_opportunities,
            'opportunities_form_url': config.ADD_OPPORTUNITY_SHEET_URL,
            'filters_types': available_types,
            'filters_programmes': available_programmes,
            'selected_type': selected_type,
            'selected_programme': selected_programme,
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
        filter_programme: str
    ) -> List[Dict]:
        """
        Filter opportunities by type and/or programme.

        Args:
            opportunities: List of opportunity dictionaries
            filter_type: Type filter (case-insensitive), empty string means no filter
            filter_programme: Programme filter (case-insensitive), empty string means no filter

        Returns:
            List[Dict]: Filtered opportunities
        """
        filtered = opportunities

        if filter_type:
            filtered = [
                opp for opp in filtered
                if (opp.get('type') or '').strip().lower() == filter_type.lower()
            ]

        if filter_programme:
            filtered = [
                opp for opp in filtered
                if (opp.get('programme') or '').strip().lower() == filter_programme.lower()
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

    return application


# Create application instance
app = create_app()

if __name__ == '__main__':
    # Run development server
    app.run(debug=True)


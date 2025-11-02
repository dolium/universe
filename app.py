import os
from flask import Flask, render_template, abort, request
from dotenv import load_dotenv
from google_sheets_service import sheets_service
import urllib.parse

load_dotenv()

ADD_OPPORTUNITY_URL = "https://docs.google.com/spreadsheets/d/1-bH05NhyJ1WFOcrmX0BtVVuvd4wWX4jx8VB-AYrOdQY/edit?gid=998865460#gid=998865460"
ADD_MATERIAL_URL = "https://docs.google.com/spreadsheets/d/1-bH05NhyJ1WFOcrmX0BtVVuvd4wWX4jx8VB-AYrOdQY/edit?gid=935728683#gid=935728683"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-change-me')

    @app.route('/')
    def index():
        return render_template(
            'index.html',
            site_name=os.getenv('SITE_NAME', 'UniVerse'),
            ga_id=os.getenv('GA_MEASUREMENT_ID', '')
        )

    @app.route('/courses')
    def courses():
        # Fetch courses from Google Sheets
        courses_data = sheets_service.get_courses()

        return render_template(
            'courses.html',
            site_name=os.getenv('SITE_NAME', 'UniVerse'),
            ga_id=os.getenv('GA_MEASUREMENT_ID', ''),
            courses=courses_data
        )

    @app.route('/opportunities')
    def opportunities():
        items = sheets_service.get_opportunities()
        # derive unique filters from current data
        all_types = sorted({(i.get('type') or '').strip() for i in items if (i.get('type') or '').strip()})
        all_programmes = sorted({(i.get('programme') or '').strip() for i in items if (i.get('programme') or '').strip()})

        sel_type = (request.args.get('type') or '').strip()
        sel_prog = (request.args.get('programme') or '').strip()

        filtered = items
        if sel_type:
            filtered = [i for i in filtered if (i.get('type') or '').strip().lower() == sel_type.lower()]
        if sel_prog:
            filtered = [i for i in filtered if (i.get('programme') or '').strip().lower() == sel_prog.lower()]

        form_url = ADD_OPPORTUNITY_URL
        return render_template(
            'opportunities.html',
            site_name=os.getenv('SITE_NAME', 'UniVerse'),
            ga_id=os.getenv('GA_MEASUREMENT_ID', ''),
            opportunities=filtered,
            opportunities_form_url=form_url,
            filters_types=all_types,
            filters_programmes=all_programmes,
            selected_type=sel_type,
            selected_programme=sel_prog,
            total_count=len(items)
        )

    @app.route('/courses/<slug>')
    def course_detail(slug):
        course = sheets_service.get_course_by_slug(slug)
        if not course:
            abort(404)
        # Load materials for this course
        materials = sheets_service.get_course_materials(slug)
        # Use provided spreadsheet link for adding materials
        materials_form_url = ADD_MATERIAL_URL

        return render_template(
            'course_detail.html',
            site_name=os.getenv('SITE_NAME', 'UniVerse'),
            ga_id=os.getenv('GA_MEASUREMENT_ID', ''),
            course=course,
            materials=materials,
            materials_form_url=materials_form_url
        )

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
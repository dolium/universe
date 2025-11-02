import os
from flask import Flask, render_template
from dotenv import load_dotenv
from google_sheets_service import sheets_service

load_dotenv()


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

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
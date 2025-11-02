"""
Test script to verify the courses functionality.
Tests data loading from Google Sheets (or fallback) and route accessibility.
"""

from typing import List, Dict
from google_sheets_service import sheets_service
from app import app as flask_application


def test_courses_functionality():
    """
    Main test function that validates:
    1. Course data loading
    2. Routes accessibility
    3. Data source verification
    """
    print("=" * 60)
    print("TESTING COURSE LOADING FUNCTIONALITY")
    print("=" * 60)

    # Fetch all courses
    all_courses = sheets_service.get_courses()

    # Determine and display data source
    data_source = 'Google Sheets' if sheets_service.is_using_google_sheets() else 'Fallback data'
    print(f"\n📊 Data source: {data_source}")
    print(f"✓ Successfully loaded {len(all_courses)} courses\n")

    # Display detailed information for each course
    _display_course_details(all_courses)

    # Test Flask routes
    _test_flask_routes(all_courses)

    # Display completion message and setup instructions
    _display_completion_message()


def _display_course_details(courses: List[Dict]):
    """
    Display detailed information for each course.

    Args:
        courses: List of course dictionaries
    """
    print("📚 COURSES DETAILS:")
    print("-" * 60)

    for index, course in enumerate(courses, 1):
        print(f"\n{index}. {course['name']}")
        if course.get('professor'):
            print(f"   👤 Professor: {course.get('professor')}")
        print(f"   🔗 Slug: {course.get('slug', 'N/A')}")
        print(f"   📝 Description: {course.get('description', 'N/A')}")
        print(f"   🎨 Icon: {course.get('icon', 'N/A')}")


def _test_flask_routes(courses: List[Dict]):
    """
    Test Flask application routes for accessibility.

    Args:
        courses: List of course dictionaries
    """
    print("\n" + "=" * 60)
    print("TESTING FLASK ROUTES")
    print("=" * 60)

    with flask_application.test_client() as test_client:
        # Test courses listing page
        courses_response = test_client.get("/courses")
        print(f"\n✓ /courses endpoint status: {courses_response.status_code}")
        assert courses_response.status_code == 200, "Courses page should return 200"
        assert b"STEM Courses" in courses_response.data, "Courses page should contain 'STEM Courses'"

        # Test course detail page (if courses exist)
        if courses:
            first_course_slug = courses[0].get('slug')
            detail_url = f"/courses/{first_course_slug}"
            print(f"✓ Testing detail page: {detail_url}")

            detail_response = test_client.get(detail_url)
            print(f"✓ Detail page status: {detail_response.status_code}")
            assert detail_response.status_code == 200, "Course detail page should return 200"


def _display_completion_message():
    """Display test completion message and setup instructions."""
    print("\n" + "=" * 60)
    print("✅ ALL TESTS COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print("\n📌 Note: If Google Sheets is not configured,")
    print("   the application will use fallback data.")
    print("\n🔧 To use Google Sheets:")
    print("   1. Follow instructions in GOOGLE_SHEETS_SETUP.md")
    print("   2. Add GOOGLE_SHEET_ID to .env file")
    print("   3. Ensure credentials.json is valid and readable")
    print("   4. Re-run this test script to verify the setup")


if __name__ == "__main__":
    test_courses_functionality()

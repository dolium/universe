"""
Quick test script to verify the courses functionality
"""

from google_sheets_service import sheets_service
from app import app as flask_app


def test_courses():
    print("=" * 50)
    print("TESTING COURSE LOADING FUNCTIONALITY")
    print("=" * 50)

    # Get courses
    courses = sheets_service.get_courses()

    source = 'Google Sheets' if sheets_service.is_using_google() else 'Fallback data'
    print(f"\nData source: {source}")
    print(f"\n✓ Successfully loaded {len(courses)} courses\n")

    # Display each course
    for i, course in enumerate(courses, 1):
        print(f"{i}. {course['name']}, {course.get('professor','')}")
        print(f"   Slug: {course.get('slug','')}")
        print(f"   Description: {course.get('description','')}")
        print(f"   Icon: {course.get('icon','')}")
        print()

    with flask_app.test_client() as c:
        # List page
        resp_list = c.get("/courses")
        print(f"/courses status: {resp_list.status_code}")
        assert resp_list.status_code == 200
        assert b"STEM Courses" in resp_list.data

        # Detail page
        if courses:
            slug = courses[0].get('slug')
            print(f"Testing detail page for slug: /courses/{slug}")
            resp = c.get(f"/courses/{slug}")
            print(f"Detail page status: {resp.status_code}")
            assert resp.status_code == 200

    print("=" * 50)
    print("TEST COMPLETED SUCCESSFULLY!")
    print("=" * 50)
    print("\nNote: If Google Sheets is not configured,")
    print("the app will use dummy data (which is what you're seeing above).")
    print("\nTo use Google Sheets:")
    print("1. Follow instructions in GOOGLE_SHEETS_SETUP.md")
    print("2. Add GOOGLE_SHEET_ID to .env file")
    print("3. Ensure credentials.json is valid and readable")


if __name__ == "__main__":
    test_courses()

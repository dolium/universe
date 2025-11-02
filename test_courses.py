"""
Quick test script to verify the courses functionality
"""

from google_sheets_service import sheets_service

def test_courses():
    print("=" * 50)
    print("TESTING COURSE LOADING FUNCTIONALITY")
    print("=" * 50)

    # Get courses
    courses = sheets_service.get_courses()

    print(f"\n✓ Successfully loaded {len(courses)} courses\n")

    # Display each course
    for i, course in enumerate(courses, 1):
        print(f"{i}. {course['name']}, {course['professor']}")
        print(f"   Description: {course['description']}")
        print(f"   Icon: {course['icon']}")
        print()

    print("=" * 50)
    print("TEST COMPLETED SUCCESSFULLY!")
    print("=" * 50)
    print("\nNote: If Google Sheets is not configured,")
    print("the app will use dummy data (which is what you're seeing above).")
    print("\nTo use Google Sheets:")
    print("1. Follow instructions in GOOGLE_SHEETS_SETUP.md")
    print("2. Add GOOGLE_SHEET_ID to .env file")
    print("3. Run this test again")

if __name__ == "__main__":
    test_courses()


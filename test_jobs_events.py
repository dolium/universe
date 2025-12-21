"""
Test script to verify the jobs and events functionality.
Tests data loading from Google Sheets (or fallback) and route accessibility.
"""

from typing import List, Dict
from google_sheets_service import sheets_service
from app import app as flask_application


def test_jobs_and_events_functionality():
    """
    Main test function that validates:
    1. Jobs data loading
    2. Events data loading
    3. Routes accessibility
    4. Data source verification
    """
    print("=" * 60)
    print("TESTING JOBS AND EVENTS FUNCTIONALITY")
    print("=" * 60)

    # Fetch all jobs
    all_jobs = sheets_service.get_jobs()

    # Determine and display data source
    data_source = 'Google Sheets' if sheets_service.is_using_google_sheets() else 'Fallback data'
    print(f"\n📊 Data source: {data_source}")
    print(f"✓ Successfully loaded {len(all_jobs)} jobs\n")

    # Display detailed information for each job
    _display_jobs_details(all_jobs)

    # Fetch all events
    all_events = sheets_service.get_events()
    print(f"\n✓ Successfully loaded {len(all_events)} events\n")

    # Display detailed information for each event
    _display_events_details(all_events)

    # Test Flask routes
    _test_flask_routes()

    # Display completion message
    _display_completion_message()


def _display_jobs_details(jobs: List[Dict]):
    """
    Display detailed information for each job.

    Args:
        jobs: List of job dictionaries
    """
    print("💼 JOBS DETAILS:")
    print("-" * 60)

    for index, job in enumerate(jobs, 1):
        print(f"\n{index}. {job['title']}")
        if job.get('type'):
            print(f"   📋 Type: {job.get('type')}")
        if job.get('programme'):
            print(f"   🎓 Programme: {job.get('programme')}")
        print(f"   📝 Description: {job.get('description', 'N/A')}")


def _display_events_details(events: List[Dict]):
    """
    Display detailed information for each event.

    Args:
        events: List of event dictionaries
    """
    print("\n📅 EVENTS DETAILS:")
    print("-" * 60)

    for index, event in enumerate(events, 1):
        print(f"\n{index}. {event['title']}")
        if event.get('type'):
            print(f"   📋 Type: {event.get('type')}")
        if event.get('programme'):
            print(f"   🎓 Programme: {event.get('programme')}")
        print(f"   📝 Description: {event.get('description', 'N/A')}")


def _test_flask_routes():
    """
    Test Flask application routes for accessibility.
    """
    print("\n" + "=" * 60)
    print("TESTING FLASK ROUTES")
    print("=" * 60)

    with flask_application.test_client() as test_client:
        # Test jobs listing page
        jobs_response = test_client.get("/jobs")
        print(f"\n✓ /jobs endpoint status: {jobs_response.status_code}")
        assert jobs_response.status_code == 200, "Jobs page should return 200"
        assert b"Jobs" in jobs_response.data or b"Stellen" in jobs_response.data, "Jobs page should contain 'Jobs' or 'Stellen'"

        # Test events listing page
        events_response = test_client.get("/events")
        print(f"✓ /events endpoint status: {events_response.status_code}")
        assert events_response.status_code == 200, "Events page should return 200"
        assert b"Events" in events_response.data or b"Veranstaltungen" in events_response.data, "Events page should contain 'Events' or 'Veranstaltungen'"


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
    print("   4. Create 'Jobs' and 'Events' worksheets in your Google Sheet")
    print("   5. Re-run this test script to verify the setup")


if __name__ == "__main__":
    test_jobs_and_events_functionality()

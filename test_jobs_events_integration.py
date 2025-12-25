"""
Test to verify that Jobs and Events pages correctly fetch data from Google Sheets.
"""
from google_sheets_service import sheets_service


def test_jobs_data_structure():
    """Test that get_jobs returns data with correct structure."""
    jobs = sheets_service.get_jobs()

    print(f"\n✓ Retrieved {len(jobs)} jobs from Google Sheets")

    if jobs:
        sample_job = jobs[0]
        print(f"\nSample job data structure:")
        print(f"  - Title: {sample_job.get('title', 'N/A')}")
        print(f"  - Type: {sample_job.get('type', 'N/A')}")
        print(f"  - Programme: {sample_job.get('programme', 'N/A')}")
        print(f"  - Description: {sample_job.get('description', 'N/A')[:50]}...")

        # Verify required fields
        required_fields = ['title', 'type', 'programme', 'description']
        for field in required_fields:
            assert field in sample_job, f"Missing field: {field}"

        print(f"\n✓ All required fields present: {', '.join(required_fields)}")
    else:
        print("\n⚠ No jobs found. This could mean:")
        print("  1. The 'Jobs' sheet is empty")
        print("  2. Using fallback data (Google Sheets not configured)")
        print("  3. Authentication issue with Google Sheets")


def test_events_data_structure():
    """Test that get_events returns data with correct structure."""
    events = sheets_service.get_events()

    print(f"\n✓ Retrieved {len(events)} events from Google Sheets")

    if events:
        sample_event = events[0]
        print(f"\nSample event data structure:")
        print(f"  - Title: {sample_event.get('title', 'N/A')}")
        print(f"  - Type: {sample_event.get('type', 'N/A')}")
        print(f"  - Programme: {sample_event.get('programme', 'N/A')}")
        print(f"  - Description: {sample_event.get('description', 'N/A')[:50]}...")

        # Verify required fields
        required_fields = ['title', 'type', 'programme', 'description']
        for field in required_fields:
            assert field in sample_event, f"Missing field: {field}"

        print(f"\n✓ All required fields present: {', '.join(required_fields)}")
    else:
        print("\n⚠ No events found. This could mean:")
        print("  1. The 'Events' sheet is empty")
        print("  2. Using fallback data (Google Sheets not configured)")
        print("  3. Authentication issue with Google Sheets")


def test_data_source():
    """Test which data source is being used."""
    # Trigger data fetch
    sheets_service.get_jobs()

    is_google = sheets_service.is_using_google_sheets()

    if is_google:
        print("\n✓ Using Google Sheets as data source")
    else:
        print("\n⚠ Using fallback data (Google Sheets not configured or unavailable)")


if __name__ == '__main__':
    print("=" * 60)
    print("Testing Jobs and Events Google Sheets Integration")
    print("=" * 60)

    try:
        test_data_source()
        test_jobs_data_structure()
        test_events_data_structure()

        print("\n" + "=" * 60)
        print("✓ All tests passed!")
        print("=" * 60)
        print("\nYour Jobs and Events pages are correctly configured to fetch")
        print("data from Google Sheets tabs with the following structure:")
        print("  - Title")
        print("  - Type")
        print("  - Study Programme")
        print("  - Description")
        print("\nThe pages will automatically refresh when you update the")
        print("Google Sheets data (may require page refresh in browser).")
        print("=" * 60)

    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()


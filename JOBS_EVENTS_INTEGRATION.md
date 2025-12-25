# Jobs and Events Google Sheets Integration

## Overview
The Jobs and Events pages are fully integrated with Google Sheets and automatically refresh their data from dedicated tabs in your Google Spreadsheet.

## Google Sheets Setup

### Sheet Structure
Your Google Sheets document should have the following tabs:

1. **Jobs** tab with columns:
   - **Title** - Name of the job opportunity
   - **Type** - Job type (e.g., Part-time, Full-time, Mini job, Internship)
   - **Study Programme** - Related study programme (e.g., CS, Physics, Mathematics, Any)
   - **Description** - Detailed description of the job

2. **Events** tab with columns:
   - **Title** - Name of the event
   - **Type** - Event type (e.g., Competition, Seminar, Networking, Workshop)
   - **Study Programme** - Related study programme (e.g., CS, Physics, Engineering, DTM)
   - **Description** - Detailed description of the event

## Configuration

### Environment Variables
The configuration is set in your `.env` file and `config.py`:

```python
JOBS_SHEET_NAME=Jobs          # Name of the Jobs tab in Google Sheets
EVENTS_SHEET_NAME=Events      # Name of the Events tab in Google Sheets
```

### Adding Data URLs
Users can add new jobs and events via Google Forms or direct sheet access:

```python
ADD_JOB_SHEET_URL = "https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit"
ADD_EVENT_SHEET_URL = "https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit"
```

## How It Works

### Data Fetching Process

1. **Authentication**: The system authenticates with Google Sheets using service account credentials (`credentials.json`)

2. **Data Retrieval**: 
   - `sheets_service.get_jobs()` fetches all rows from the "Jobs" tab
   - `sheets_service.get_events()` fetches all rows from the "Events" tab

3. **Field Mapping**: The system supports flexible column naming:
   - Title: 'Title', 'Job', 'Event', 'Name'
   - Type: 'Type', 'Category'
   - Study Programme: 'Study Programme', 'StudyProgram', 'Programme', 'Program'
   - Description: 'Description', 'Details'

4. **Filtering**: Both pages support filtering by:
   - Type (dropdown selection)
   - Multiple Study Programmes (checkbox selection)

5. **Real-time Updates**: Changes in Google Sheets are reflected immediately on page refresh

### Fallback Mechanism

If Google Sheets is unavailable (credentials missing, authentication failure, or network issues), the system automatically falls back to sample data to keep the site functional.

## Features

### Jobs Page (`/jobs`)
- Displays all job opportunities from the "Jobs" sheet
- Filterable by job type and study programmes
- Shows count of filtered vs. total jobs
- "Add new job" button links to the Google Sheet
- Mobile-responsive card layout

### Events Page (`/events`)
- Displays all events from the "Events" sheet
- Filterable by event type and study programmes
- Shows count of filtered vs. total events
- "Add new event" button links to the Google Sheet
- Mobile-responsive card layout

## API Methods

### `sheets_service.get_jobs()` → `List[Dict]`
Returns a list of job dictionaries with structure:
```python
{
    'title': str,      # Job title
    'type': str,       # Job type
    'programme': str,  # Study programme
    'description': str # Job description
}
```

### `sheets_service.get_events()` → `List[Dict]`
Returns a list of event dictionaries with structure:
```python
{
    'title': str,      # Event title
    'type': str,       # Event type
    'programme': str,  # Study programme
    'description': str # Event description
}
```

## Testing

Run the integration test to verify everything is working:

```bash
python test_jobs_events_integration.py
```

This test will:
- Verify data source (Google Sheets or fallback)
- Check data structure for jobs
- Check data structure for events
- Validate required fields

## Maintenance

### Adding New Jobs/Events
1. Open your Google Sheets document
2. Navigate to the "Jobs" or "Events" tab
3. Add a new row with all required fields filled
4. Refresh the website - changes appear immediately

### Modifying Existing Entries
1. Edit the row directly in Google Sheets
2. Refresh the website to see changes

### Removing Entries
1. Delete the row from Google Sheets
2. Refresh the website - entry disappears

## Troubleshooting

### Data Not Updating
- Verify Google Sheets credentials are valid
- Check that sheet names match configuration
- Ensure column headers match expected names
- Try clearing browser cache

### Seeing Fallback Data
If you see sample data instead of your Google Sheets data:
1. Check `credentials.json` exists and is valid
2. Verify `GOOGLE_SHEET_ID` in `.env` file
3. Ensure service account has access to the sheet
4. Run `test_jobs_events_integration.py` for diagnostic info

### Authentication Errors
- Regenerate service account credentials
- Share the Google Sheet with the service account email
- Verify credentials file path is correct

## Architecture

```
User Browser
    ↓
Flask App (app.py)
    ↓
/jobs or /events route
    ↓
sheets_service.get_jobs() or sheets_service.get_events()
    ↓
Google Sheets API
    ↓
Jobs/Events Tab
    ↓
Return formatted data
    ↓
Render jobs.html or events.html template
    ↓
Display with filtering options
```

## Related Files

- `app.py` - Flask routes for `/jobs` and `/events`
- `google_sheets_service.py` - Data fetching logic
- `config.py` - Configuration constants
- `templates/jobs.html` - Jobs page template
- `templates/events.html` - Events page template
- `test_jobs_events_integration.py` - Integration tests

## Summary

✅ Jobs and Events pages are **fully integrated** with Google Sheets
✅ Data automatically refreshes from "Jobs" and "Events" tabs
✅ Supports required fields: Title, Type, Study Programme, Description
✅ Includes filtering by type and study programmes
✅ Fallback mechanism ensures site remains functional
✅ Real-time updates on page refresh


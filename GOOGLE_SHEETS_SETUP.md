# Google Sheets Integration Guide

## Overview

This application can dynamically load course data from a Google Sheet, allowing you to manage courses without editing code.

## Setup Steps

### 1. Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the **Google Sheets API**:
   - Navigate to "APIs & Services" > "Library"
   - Search for "Google Sheets API"
   - Click "Enable"

### 2. Create Service Account Credentials

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "Service Account"
3. Fill in the service account details:
   - Name: `course-manager` (or any name you prefer)
   - ID: Auto-generated
   - Click "Create and Continue"
4. Skip the optional steps (roles not required for this use case)
5. Click "Done"

### 3. Generate and Download Credentials

1. Click on the service account you just created
2. Go to the "Keys" tab
3. Click "Add Key" > "Create new key"
4. Choose "JSON" format
5. Click "Create"
6. The credentials file will be downloaded automatically
7. Rename the file to `credentials.json` and move it to your project root

### 4. Create Your Google Sheet

1. Create a new Google Sheet
2. Set up the following columns in the first row (headers):

| Column | Description | Example |
|--------|-------------|---------|
| **Course** | Full course name | Mathematics II |
| **Professor** | Professor name with title | Prof. Buhl |
| **Description** | Course description (2-3 sentences) | Advanced calculus and linear algebra for engineering students. |
| **Icon** | Icon identifier | math |

3. Available icon identifiers:
   - `math` - Mathematics icon
   - `physics` - Physics/atom icon
   - `chemistry` - Chemistry/beaker icon
   - `biology` - Biology/DNA icon
   - `cs` - Computer Science/code icon
   - `engineering` - Engineering/gear icon
   - `default` - Generic icon

### 5. Share the Sheet with Service Account

1. Open the Google Sheet
2. Click the "Share" button
3. Paste the service account email (found in `credentials.json` under `client_email`)
4. Set permission to "Viewer"
5. Uncheck "Notify people"
6. Click "Share"

### 6. Get the Sheet ID

From your Google Sheet URL:
```
https://docs.google.com/spreadsheets/d/1abc123xyz456/edit
                                       ^^^^^^^^^^^^^^^^
                                       This is your Sheet ID
```

Copy the Sheet ID (the part between `/d/` and `/edit`)

### 7. Configure Environment Variables

Add these lines to your `.env` file:

```env
GOOGLE_SHEET_ID=your_sheet_id_here
GOOGLE_CREDENTIALS_FILE=credentials.json
```

### 8. Test the Integration

Restart your Flask application:

```bash
python app.py
```

Visit `http://localhost:5000/courses` to see your courses loaded from Google Sheets.

## Example Google Sheet

You can import the `courses_template.csv` file into Google Sheets as a starting point:

1. Open Google Sheets
2. File > Import
3. Upload the `courses_template.csv` file
4. Choose "Replace current sheet"
5. Follow the setup steps above

## Troubleshooting

### "Template file 'courses.html' not found"
- This is usually an IDE cache issue, restart your IDE

### "Credentials file not found"
- Make sure `credentials.json` is in your project root
- Check the `GOOGLE_CREDENTIALS_FILE` path in `.env`

### "Permission denied" when accessing sheet
- Ensure you've shared the sheet with the service account email
- Check that the service account has at least "Viewer" permission

### Courses not updating
- The app fetches data on each page load
- If using cached data, clear your browser cache
- Check the console for error messages

## Fallback Behavior

If Google Sheets integration is not configured or fails, the application will automatically fall back to displaying dummy course data. This ensures the site remains functional even without Google Sheets access.

## Security Notes

- Never commit `credentials.json` to version control
- Add `credentials.json` to your `.gitignore` file
- Keep your service account credentials secure
- Only grant "Viewer" permission to the service account (not Editor)


# Professor Availability Feature Implementation

## Overview
Added a new professor availability page that displays schedule data from Google Sheets with filtering capabilities for professors and search functionality.

## Changes Made

### 1. Configuration (`config.py`)
- Added `PROFESSOR_AVAILABILITY_WORKSHEET_NAME` configuration to specify the worksheet name (defaults to 'Timetable')

### 2. Google Sheets Service (`google_sheets_service.py`)
- Added `professor_availability_worksheet_name` property to service initialization
- Implemented `get_professor_availability()` method that:
  - Fetches all data from the 'Timetable' worksheet
  - Supports any column structure (dynamic table headers)
  - Falls back to sample data if Google Sheets is unavailable
- Added `_get_fallback_professor_availability()` method with sample German availability data

### 3. Flask Application (`app.py`)
- Added `/timetable` route with filtering capabilities
- Implemented helper functions:
  - `_extract_unique_professors()`: Extracts unique professor names from availability entries
  - `_filter_availability()`: Filters entries by professor selection or search query
  - `_get_professor_name()`: Handles multiple possible column names for professors (Professor, Dozent, Lehrer)

### 4. Template (`templates/timetable.html`)
- Created new template with:
  - Dark theme styling consistent with the rest of the site
  - Search input for finding professors
  - Dropdown filter for selecting specific professors
  - Day-of-week filter dropdown
  - Dynamic table that displays all columns from the Google Sheet
  - Responsive design for mobile devices
  - Filter count showing "X of Y entries displayed"
  - German language labels

### 5. Navigation (`templates/base.html`)
- Added "Professor Availability" link to the main navigation menu
- Removed "Notes" navigation item

## Features

- **Professor Dropdown**: Select a specific professor to filter availability
- **Day Dropdown**: Filter by specific day of the week
- **Search Bar**: Type to search for professors by name (case-insensitive)
- **Professor Dropdown**: Select a specific professor to filter the timetable
- **Reset Button**: Clear all filters and show all entries
- **Entry Count**: Shows how many entries match the current filters

### Dynamic Table Display
- Automatically displays all columns from your Google Sheet
- Automatically merges duplicate rows that differ only in Program/Semester column
- No hardcoded column names - works with any table structure
- Supports German column names (Tag, Zeit, Fach, Professor, Raum, etc.)

### Professor Name Recognition
The system recognizes multiple German/English terms for professor:
- Professor
- Dozent
- Lehrer

## Google Sheets Setup

Your 'Timetable' worksheet should have:
- First row as headers (e.g., Tag, Zeit, Fach, Professor, Raum)
- Data rows below with schedule information
- A column containing professor names (any of: Professor, Dozent, or Lehrer)

Example structure:
```
Tag       | Zeit        | Fach           | Professor      | Raum
Montag    | 08:00-10:00 | Mathematik II  | Prof. Buhl     | A101
Dienstag  | 10:15-12:00 | Physik I       | Prof. Schmidt  | B205
1. Navigate to `/timetable` or click "Professor Availability" in the navigation menu

## Usage
4. Filter by day of the week using the day dropdown
5. Click "Zurücksetzen" (Reset) to clear filters
6. The table will update automatically based on your filters
2. Use the search bar to find specific professors
3. Or use the dropdown to filter by a specific professor
4. Click "Zurücksetzen" (Reset) to clear filters
The professor availability page uses the same dark theme as the rest of the application:

## Styling

The timetable uses the same dark theme as the rest of the application:
- Dark panel background (`var(--panel)`)
- Accent color for headers (`var(--accent)` - purple)
- Hover effects on rows
- Responsive design for mobile devices
- Smooth transitions and modern UI elements


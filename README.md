# UniVerse - Educational Platform

A Flask-based educational platform with dynamic course management via Google Sheets integration.

## Features

- 🎨 Beautiful dark theme design
- 📊 Dynamic course loading from Google Sheets
- 🚀 Fast and responsive interface
- 📱 Mobile-friendly design

## Quick Start

### 1. Installation

```bash
python -m venv .venv
# Activate your virtual environment
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Create a `.env` file based on `.env.example`:

```bash
cp .env.example .env
```

Edit `.env` and configure:
- `SITE_NAME`: Your site name
- `SECRET_KEY`: A secure random string
- `GOOGLE_SHEET_ID`: Your Google Sheet ID (optional)
- `GOOGLE_CREDENTIALS_FILE`: Path to Google credentials JSON file (optional)

### 3. Google Sheets Setup (Optional)

If you want to manage courses via Google Sheets:

1. Create a Google Cloud Project and enable Google Sheets API
2. Create a Service Account and download credentials as JSON
3. Save the credentials file as `credentials.json` in the project root
4. Create a Google Sheet with the following columns:
   - **Course**: Course name (e.g., "Mathematics II")
   - **Professor**: Professor name (e.g., "Prof. Buhl")
   - **Description**: Course description
   - **Icon**: Icon identifier (math, physics, chemistry, biology, cs, engineering, or default)
5. Share the Google Sheet with the service account email (found in credentials.json)
6. Copy the Sheet ID from the URL and add it to `.env`

**Google Sheet URL Format:**
```
https://docs.google.com/spreadsheets/d/[SHEET_ID]/edit
```

**Example Google Sheet Structure:**

| Course | Professor | Description | Icon |
|--------|-----------|-------------|------|
| Mathematics II | Prof. Buhl | Advanced calculus and linear algebra | math |
| Physics I | Prof. Schmidt | Classical mechanics and thermodynamics | physics |
| Chemistry Fundamentals | Prof. Weber | Organic and inorganic chemistry | chemistry |

**Note:** If Google Sheets is not configured, the app will use dummy data as fallback.

### 4. Run the Application

```bash
python app.py
```

Visit `http://localhost:5000` in your browser.

## Project Structure

```
.
├── app.py                      # Main Flask application
├── google_sheets_service.py    # Google Sheets integration
├── requirements.txt            # Python dependencies
├── .env                        # Environment configuration
├── static/
│   ├── css/
│   │   └── main.css           # Styles with dark theme
│   ├── img/                   # Icons and images
│   └── js/
│       └── main.js            # JavaScript
└── templates/
    ├── base.html              # Base template
    ├── index.html             # Homepage
    └── courses.html           # Courses page (dynamic)
```

## Development

To modify the design or add features:

1. Edit templates in `templates/` folder
2. Update styles in `static/css/main.css`
3. Modify Google Sheets integration in `google_sheets_service.py`

## License

MIT License


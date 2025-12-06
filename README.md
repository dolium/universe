# UniVerse - Educational Platform

A Flask-based educational platform with dynamic course management via Google Sheets integration.

## Features

- 🎨 Beautiful dark theme design
- 📊 Dynamic course loading from Google Sheets
- 🚀 Fast and responsive interface
- 📱 Mobile-friendly design
- 👤 User authentication and account management
- 📚 Material sharing with authorship tracking
- ⭐ Material rating system (1-5 stars)
- 👥 User account pages showing contributions
- 🔒 Secure password hashing with bcrypt

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

If you want to manage courses and materials via Google Sheets:

1. Create a Google Cloud Project and enable Google Sheets API
2. Create a Service Account and download credentials as JSON
3. Save the credentials file as `credentials.json` in the project root
4. Create a Google Sheet with multiple worksheets:

#### Courses Worksheet (Tab 1)
   - **Course**: Course name (e.g., "Mathematics II")
   - **Professor**: Professor name (e.g., "Prof. Buhl")
   - **Description**: Course description
   - **Icon**: Icon identifier (math, physics, chemistry, biology, cs, engineering, or default)
   - **Study Programme**: Program name (optional)

#### Materials Worksheet (Tab 2)
   - **Course**: Course name (must match a course from Tab 1)
   - **Title**: Material title (e.g., "Exam Cheat Sheet 2024")
   - **URL**: Link to the material
   - **Author Email**: Email of person who added it (optional)
   - **Rating**: Average rating 0-5 (optional, auto-updated)
   - **Rating Count**: Number of ratings (optional, auto-updated)

#### Users Worksheet (Tab 4)
   - Created automatically when users register
   - **Email**: User email address
   - **Password**: Hashed password
   - **Name**: User's full name
   - **Created**: Timestamp

5. Share the Google Sheet with the service account email (found in credentials.json) with **Editor** permissions
6. Copy the Sheet ID from the URL and add it to `.env`

For detailed setup instructions, see:
- [GOOGLE_SHEETS_SETUP.md](GOOGLE_SHEETS_SETUP.md) - General Google Sheets setup
- [MATERIALS_SHEET_SETUP.md](MATERIALS_SHEET_SETUP.md) - Materials sheet structure and rating system
- [AUTHENTICATION_SETUP.md](AUTHENTICATION_SETUP.md) - User authentication setup

**Google Sheet URL Format:**
```
https://docs.google.com/spreadsheets/d/[SHEET_ID]/edit
```

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
├── config.py                   # Configuration management
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
    ├── courses.html           # Courses listing page
    ├── course_detail.html     # Individual course page with materials
    ├── opportunities.html     # Opportunities page
    ├── timetable.html         # Professor availability
    ├── login.html             # Login page
    ├── register.html          # Registration page
    └── account.html           # User account page
```

## User Features

### For Students
- **Browse Courses**: View all available courses with filtering by study programme
- **Access Materials**: Find study materials, cheat sheets, notes, and templates
- **Rate Materials**: Give 1-5 star ratings to materials (requires login)
- **Share Materials**: Add your own materials via Google Forms (linked on course pages)
- **View Contributions**: See all materials you've added on your account page
- **User Profiles**: Click on any author's email to see their contributions

### For Administrators
- **Dynamic Content**: Manage courses, materials, and opportunities via Google Sheets
- **No Code Changes**: Add/update content without deploying code
- **User Management**: Track registered users in the Users worksheet
- **Analytics Ready**: Google Analytics integration available

## Development

To modify the design or add features:

1. Edit templates in `templates/` folder
2. Update styles in `static/css/main.css`
3. Modify Google Sheets integration in `google_sheets_service.py`

## License

MIT License


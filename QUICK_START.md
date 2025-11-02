# Quick Start Guide - Course Management

## ✅ What's Been Added

Your courses page now supports **dynamic course loading from Google Sheets**!

### Key Features:
- 📊 **Automatic updates** - Just update your Google Sheet, refresh the page
- 🎨 **Beautiful dark theme** - Modern, responsive design
- 📝 **Course format** - "Course Name, Prof. Name" format
- 🔄 **Fallback data** - Works without Google Sheets (uses dummy data)

## 🚀 How It Works

### Without Google Sheets (Default)
The app will display 6 example courses with professors:
- Mathematics II, Prof. Buhl
- Physics I, Prof. Schmidt
- Chemistry Fundamentals, Prof. Weber
- Biology & Ecology, Prof. Mueller
- Computer Science I, Prof. Fischer
- Engineering Design, Prof. Becker

### With Google Sheets (Optional)
1. Set up Google Sheets API (see `GOOGLE_SHEETS_SETUP.md`)
2. Create a sheet with columns: **Course**, **Professor**, **Description**, **Icon**
3. Add your courses in format: "Mathematics II" in Course, "Prof. Buhl" in Professor
4. Share with service account
5. Add Sheet ID to `.env` file
6. Restart the app

## 📋 Example Course Entry

| Course | Professor | Description | Icon |
|--------|-----------|-------------|------|
| Mathematics II | Prof. Buhl | Advanced calculus and linear algebra for engineering students. | math |

## 🎨 Available Icons

- `math` - For mathematics courses
- `physics` - For physics courses
- `chemistry` - For chemistry courses
- `biology` - For biology courses
- `cs` - For computer science courses
- `engineering` - For engineering courses
- `default` - For any other course

## 📁 Files Created

- `google_sheets_service.py` - Handles Google Sheets integration
- `courses_template.csv` - Template for your course data
- `GOOGLE_SHEETS_SETUP.md` - Detailed setup instructions
- `.gitignore` - Security (keeps credentials safe)
- `.env.example` - Configuration template

## 🔧 Usage

### Run the app:
```bash
python app.py
```

### View courses:
Open `http://localhost:5000/courses`

### Update courses:
- **Without Google Sheets**: Edit dummy data in `google_sheets_service.py` (method `_get_dummy_courses()`)
- **With Google Sheets**: Just edit your Google Sheet and refresh the page

## 🎯 Page Design

The courses page features:
- ✨ Gradient animated header
- 🎴 Grid of course cards
- 🖼️ SVG icons with hover effects
- 📱 Fully responsive design
- 🌙 Beautiful dark theme
- 💫 Smooth animations

## 🔒 Security

- Never commit `credentials.json`
- Keep your `.env` file secret
- `.gitignore` is configured to protect sensitive files

## 📝 Notes

- No "STEM Courses" mention - it's just "Available Courses"
- Course naming format: "[Course Name], [Prof. Name]"
- Fallback ensures site always works
- Page auto-updates on each visit when using Google Sheets

Enjoy your new course management system! 🎓


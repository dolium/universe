# Materials Sheet Structure Guide

## Overview

The Materials worksheet in your Google Sheet allows you to add course materials that will be displayed on course detail pages. Materials now support authorship tracking and rating functionality.

## Required Columns

The Materials worksheet (typically the second tab in your spreadsheet) should have the following columns:

| Column Name | Required | Description | Example |
|-------------|----------|-------------|---------|
| **Course** | Yes | The exact course name (must match a course in the Courses sheet) | Mathematics II |
| **Title** or **Name** | Yes | Title of the material | Exam Cheat Sheet (2024) |
| **URL** or **Link** | Yes | Link to the material | https://drive.google.com/... |
| **Author Email** or **Author** or **Email** or **Added By** | Optional | Email address of the person who added the material | student@university.edu |
| **Rating** or **Average Rating** or **Stars** | Optional | Average rating (0-5 stars) | 4.5 |
| **Rating Count** or **Ratings** or **Number of Ratings** | Optional | Number of ratings received | 10 |

## Column Details

### Course (Required)
- **Type**: Text
- **Description**: Must exactly match a course name from the Courses worksheet
- **Example**: `Mathematics II`, `Physics I`, `Computer Science I`
- **Note**: The system creates a URL slug from this name, so consistency matters

### Title/Name (Required)
- **Type**: Text
- **Description**: A descriptive title for the material
- **Example**: `Exam Cheat Sheet (2024)`, `Lab Report Template`, `Lecture Notes Week 1-5`
- **Note**: This is what users will see when browsing materials

### URL/Link (Required)
- **Type**: URL
- **Description**: A link to access the material
- **Example**: `https://drive.google.com/file/d/...`, `https://example.com/notes.pdf`
- **Note**: Can be any accessible URL (Google Drive, Dropbox, website, etc.)

### Author Email (Optional but Recommended)
- **Type**: Email
- **Description**: Email address of the person who added this material
- **Example**: `student@university.edu`
- **Features**:
  - Links to the user's account page
  - Allows viewing all materials by a specific author
  - Must match a registered user's email for the link to work
- **Note**: If left empty, the material will show without author attribution

### Rating (Optional)
- **Type**: Number (decimal)
- **Description**: Average rating from 0 to 5
- **Example**: `4.5`, `3.8`, `5.0`
- **Default**: `0` if not specified
- **Note**: 
  - Updated automatically when users submit ratings through the website
  - Displayed as stars (★) on the course detail page
  - Can be manually set or left at 0

### Rating Count (Optional)
- **Type**: Integer
- **Description**: Total number of ratings received
- **Example**: `10`, `5`, `23`
- **Default**: `0` if not specified
- **Note**: 
  - Increments automatically when users submit ratings
  - Displayed alongside the star rating
  - Helps users gauge rating reliability

## Example Materials Sheet

Here's an example of how your Materials sheet might look:

| Course | Title | URL | Author Email | Rating | Rating Count |
|--------|-------|-----|--------------|--------|--------------|
| Mathematics II | Exam Cheat Sheet (2024) | https://drive.google.com/file/d/abc123 | student@university.edu | 4.5 | 10 |
| Physics I | Lab Report Template | https://example.com/template.docx | physics.ta@university.edu | 5.0 | 5 |
| Computer Science I | Data Structures Notes | https://github.com/user/notes | cs.student@university.edu | 3.8 | 15 |
| Mathematics II | Practice Problems Set 1 | https://example.com/problems.pdf | | 0 | 0 |

## How Ratings Work

### User Rating Submission
1. Logged-in users can rate materials on course detail pages
2. Users select 1-5 stars and submit
3. The system calculates a new average rating:
   - `New Average = (Current Average × Current Count + New Rating) / (Current Count + 1)`
4. Both Rating and Rating Count are automatically updated in the sheet

### Rating Display
- **Full stars** (★) show the whole number portion of the rating
- **Half stars** (☆) show when there's a 0.5 or greater decimal
- **Empty stars** (☆) complete the 5-star display
- Example: `4.5` shows as `★★★★☆` with "4.5/5 (10 ratings)"

### No Rating Yet
- If Rating is 0 or empty, shows "No ratings yet"
- Encourages logged-in users to be the first to rate

## Integration with Other Features

### Account Pages
- When a user clicks on an author's email, they're taken to that user's account page
- The account page shows all materials added by that user
- Users can see their own contributions on their account page

### Course Detail Pages
- Materials are displayed with:
  - Clickable title linking to the resource
  - Author attribution (clickable email)
  - Star rating display
  - Rating submission form (for logged-in users)

## Setting Up the Materials Sheet

### Option 1: Add to Existing Spreadsheet
1. Open your Google Sheets spreadsheet (the one with Courses)
2. Create a new tab/sheet named "Materials"
3. Add the column headers in row 1
4. Fill in your materials data
5. Make sure the spreadsheet is shared with your service account

### Option 2: Manual Setup
1. Create the Materials worksheet with the headers above
2. Add materials one by one
3. For new materials, you can leave Rating and Rating Count at 0
4. Add Author Email if you know who added it

### Option 3: Import from Form
If you're using a Google Form to collect materials:
1. Set up form fields for: Course, Title, URL, and Email
2. Link form responses to the Materials sheet
3. Manually add Rating and Rating Count columns (initialized to 0)

## Tips and Best Practices

### For Authors
- Always include your email when adding materials
- This helps build your contribution profile
- Other students can find more of your helpful resources

### For Ratings
- Start with Rating = 0 and Rating Count = 0 for new materials
- Let the community rate materials organically
- Don't manually set high ratings without actual user input

### For Course Matching
- Use exact course names from the Courses sheet
- Case and spacing matter for matching
- Check the course detail URL to verify the slug if unsure

### Data Quality
- Keep URLs accessible (avoid broken links)
- Use descriptive titles
- Update or remove outdated materials
- Verify author emails are correct

## Troubleshooting

### Material Not Showing Up
- Check that the Course name exactly matches a course in the Courses sheet
- Verify both Title and URL are filled in
- Make sure the Materials worksheet is in the same spreadsheet
- Check worksheet name is "Materials" (or update config if different)

### Author Link Not Working
- Verify the email matches a registered user's email exactly
- Check that the user account exists in the Users sheet
- Email comparison is case-insensitive

### Ratings Not Updating
- Ensure your Google Sheet has write permissions for the service account
- Check that credentials.json has the correct scopes
- Verify Rating and Rating Count columns exist and are spelled correctly

### Permission Errors
- Make sure the service account has "Editor" permissions (not just "Viewer")
- For rating functionality to work, write access is required
- Update sharing settings in Google Sheets

## Column Name Variations

The system supports multiple column name variations for flexibility:

**Title**: Title, Name  
**URL**: URL, Link  
**Author**: Author Email, Author, Email, Added By  
**Rating**: Rating, Average Rating, Stars  
**Count**: Rating Count, Ratings, Number of Ratings

This allows you to use natural column names that make sense for your use case.

## Security Considerations

- **Email Validation**: The system only displays emails; it doesn't send or validate them
- **Rating Limits**: Individual users can rate the same material multiple times (by design)
- **Public Display**: All material information is publicly visible on the site
- **Data Integrity**: Only service account can modify the sheet through the app

## Future Enhancements

Potential features that could be added:
- One rating per user per material (requires tracking in separate sheet)
- Material categories or tags
- Download counters
- Material approval workflow
- User comments on materials


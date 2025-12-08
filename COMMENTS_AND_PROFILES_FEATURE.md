# Comments and Profiles Feature Documentation

## Overview

This document describes the new commenting and user profiles features added to UniVerse.

## Features

### 1. Comments on Materials (Notes)

Users can now comment on course materials to:
- Ask questions about the material
- Share insights or tips
- Discuss the quality or usefulness
- Provide feedback to the author

**Location:** Each material on a course detail page has a comments section below it.

**Access:** Anyone can view comments, but you must be logged in to post.

### 2. Comments on User Profiles

Users can leave comments on other users' profile pages to:
- Give kudos for helpful materials
- Ask questions about their contributions
- Connect with other students

**Location:** User profile pages (`/account/<email>`) have a comments section.

**Access:** Anyone can view profile comments, but you must be logged in to post.

### 3. User Profiles Directory

A searchable directory of all registered users.

**Location:** `/profiles` page (accessible from navigation menu)

**Features:**
- View all registered users in a grid layout
- Search by name or email
- Click to view individual profiles
- See join date for each user

## Google Sheets Setup

### Comments Worksheet

If using Google Sheets, a new "Comments" worksheet will be automatically created when the first comment is posted.

**Structure:**
| Column | Description |
|--------|-------------|
| Type | Either "material" or "profile" |
| Reference ID | For materials: "course-slug::material-title", for profiles: user email |
| Author Email | Email of the person who posted the comment |
| Author Name | Name of the person who posted the comment |
| Comment | The comment text |
| Created | Timestamp of when comment was posted |

## API Endpoints

### POST /add_comment
Posts a new comment.

**Parameters:**
- `comment_type`: "material" or "profile"
- `reference_id`: Identifier for what's being commented on
- `comment_text`: The comment content

**Authentication:** Required (login)

### GET /profiles
Lists all registered users with optional search.

**Parameters:**
- `search` (optional): Search query for name/email

**Authentication:** Not required

## Implementation Notes

### Reference ID Format

Material comments use the format: `course-slug::material-title`

The `::` separator was chosen to avoid conflicts with material titles that might contain colons.

### Security

- All comment posting requires authentication
- XSS protection through Jinja2 auto-escaping
- Input validation on all forms
- CodeQL security scan: 0 vulnerabilities

### Fallback Mode

If Google Sheets is not configured:
- Comments will not be stored (returns empty list)
- User profiles page will show "No users registered yet"
- UI remains functional, just returns empty data

## Future Enhancements

Potential improvements for future versions:
- Comment editing/deletion
- Comment threading (replies)
- Upvote/downvote for comments
- Notification system for new comments
- Comment moderation tools
- Rich text formatting in comments

## Testing

Run the test suite:
```bash
python test_comments_profiles.py
```

This validates:
- Google Sheets service methods
- Route accessibility and permissions
- Template rendering
- Authentication requirements

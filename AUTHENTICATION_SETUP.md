# Authentication System Setup Guide

## Overview

The UniVerse application now includes a complete user authentication system with login and registration functionality. User credentials are securely stored in Google Sheets with password hashing.

## Features

- ✅ User Registration with email, name, and password
- ✅ Secure Login with email and password
- ✅ Password hashing using bcrypt
- ✅ Session management with Flask-Login
- ✅ User data stored in Google Sheets
- ✅ Flash messages for user feedback
- ✅ Protected routes (can be made login-required)
- ✅ Beautiful, modern UI for auth pages

## Google Sheets Setup

### 1. Create Users Worksheet

You need to add a new worksheet called **"Users"** to your Google Spreadsheet:

1. Open your Google Spreadsheet (the one with ID in `GOOGLE_SHEET_ID`)
2. Create a new sheet/tab
3. Name it exactly: **Users** (or customize in `.env` using `USERS_SHEET_NAME`)
4. Add the following headers in the first row:
   - Column A: `Email`
   - Column B: `Password`
   - Column C: `Name`
   - Column D: `Created`

**Example:**

| Email | Password | Name | Created |
|-------|----------|------|---------|
| student@uni.edu | $2b$12$hash... | John Doe | 2025-12-06 10:30:00 |

### 2. Update Google Sheets Permissions

The service account needs **write access** to create new users:

1. In your Google Spreadsheet, click **Share**
2. Add your service account email (found in `credentials.json` - the `client_email` field)
3. Grant **Editor** permissions (not just Viewer)
4. Click **Done**

### 3. Update Scopes (Already Done in Code)

The `create_user()` method automatically requests write permissions:
- `https://www.googleapis.com/auth/spreadsheets` (full access)
- `https://www.googleapis.com/auth/drive` (for file operations)

## Environment Variables

Add to your `.env` file (optional):

```env
# Authentication
SECRET_KEY=your-secret-key-here-change-in-production

# Google Sheets - Users worksheet name (default: "Users")
USERS_SHEET_NAME=Users
```

**Important:** The `SECRET_KEY` is required for session management. Generate a secure random key for production:

```python
import secrets
print(secrets.token_hex(32))
```

## How It Works

### Registration Flow

1. User visits `/register`
2. Fills in name, email, password, and confirm password
3. Form validation checks:
   - All fields are filled
   - Passwords match
   - Password is at least 6 characters
   - Email doesn't already exist
4. Password is hashed using bcrypt with a salt
5. User data is added to Google Sheets "Users" worksheet
6. User redirected to login page with success message

### Login Flow

1. User visits `/login`
2. Enters email and password
3. System fetches user from Google Sheets by email
4. Password is verified against stored hash using bcrypt
5. If valid, user session is created with Flask-Login
6. User redirected to homepage (or requested page)

### Logout Flow

1. User clicks Logout
2. Flask-Login clears the session
3. User redirected to homepage with info message

## Security Features

### Password Hashing

Passwords are **never** stored in plain text. We use bcrypt which:
- Generates a unique salt for each password
- Creates a one-way hash that cannot be reversed
- Is resistant to rainbow table and brute-force attacks

Example stored password:
```
$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqXfj1nQOa
```

### Session Management

- Flask-Login manages user sessions securely
- Sessions are server-side and encrypted with `SECRET_KEY`
- Automatic session expiration on browser close
- Protection against session hijacking

## Usage Examples

### Making a Route Login-Required

```python
from flask_login import login_required

@application.route('/my-protected-page')
@login_required
def protected_page():
    """This page requires login."""
    return render_template('protected.html', **get_common_template_context())
```

### Accessing Current User in Templates

```html
{% if current_user.is_authenticated %}
  <p>Welcome, {{ current_user.name }}!</p>
  <p>Email: {{ current_user.email }}</p>
{% else %}
  <p>Please log in.</p>
{% endif %}
```

### Accessing Current User in Routes

```python
from flask_login import current_user

@application.route('/profile')
@login_required
def profile():
    """User profile page."""
    user_email = current_user.email
    user_name = current_user.name
    # ... your code
```

## UI Components

### Navigation Bar

The navigation automatically shows:
- **Not logged in:** Login and Register buttons
- **Logged in:** "Hi, [Name]!" greeting and Logout button

### Flash Messages

Four types of flash messages are supported:

```python
flash('Registration successful!', 'success')  # Green
flash('Invalid credentials.', 'error')        # Red
flash('You have been logged out.', 'info')    # Blue
```

### Forms

All auth forms include:
- Modern, clean design
- Input validation
- Responsive layout
- Accessible labels and placeholders
- Password visibility toggle (can be added)

## Customization

### Changing Validation Rules

Edit in `app.py`:

```python
# Minimum password length
if len(password) < 6:  # Change 6 to your requirement
    flash('Password must be at least 6 characters long.', 'error')
```

### Changing Worksheet Name

In `.env`:
```env
USERS_SHEET_NAME=MyCustomUsersSheet
```

### Styling

Edit `static/css/main.css`:
- `.auth-page` - Page layout
- `.auth-card` - Form container
- `.form-input` - Input fields
- `.flash-message` - Alert messages

## Troubleshooting

### Issue: "Users worksheet not found"

**Solution:** Create the "Users" worksheet in your Google Sheet with proper headers.

### Issue: "Failed to create user"

**Possible causes:**
1. Service account doesn't have Editor permissions
2. Worksheet name mismatch
3. Missing credentials.json file

**Solution:** Check permissions and worksheet name.

### Issue: "Template file not found" errors

**Solution:** The templates are created. Restart your IDE or clear cache.

### Issue: Login fails with correct password

**Possible causes:**
1. Password was manually added to sheet without hashing
2. Character encoding issues

**Solution:** Register new user through the registration form.

### Issue: Sessions not persisting

**Solution:** Ensure `SECRET_KEY` is set in config.py or .env file.

## Testing

### Manual Testing

1. **Register a new user:**
   - Go to http://localhost:5000/register
   - Fill in the form
   - Check Google Sheets for new row
   - Verify password is hashed (starts with $2b$)

2. **Login:**
   - Go to http://localhost:5000/login
   - Use the email/password you registered
   - Verify you see greeting in navigation

3. **Logout:**
   - Click Logout button
   - Verify session is cleared

### Checking Google Sheets

After registration, your Users sheet should look like:

| Email | Password | Name | Created |
|-------|----------|------|---------|
| test@example.com | $2b$12$abcd... | Test User | 2025-12-06 15:30:00 |

## Next Steps

### Recommended Enhancements

1. **Password Reset:** Add "Forgot Password" functionality
2. **Email Verification:** Send verification emails
3. **Profile Page:** Let users update their info
4. **Remember Me:** Add "Remember Me" checkbox
5. **Social Login:** Google/GitHub OAuth integration
6. **Two-Factor Auth:** Add 2FA for extra security
7. **Password Strength Meter:** Visual feedback during registration
8. **Account Deletion:** Let users delete their accounts
9. **Admin Dashboard:** Manage users through web interface

### Security Hardening

For production deployment:

1. Use HTTPS only
2. Set strong `SECRET_KEY` (64+ characters)
3. Implement rate limiting for login attempts
4. Add CAPTCHA to prevent bots
5. Log authentication events
6. Implement password complexity requirements
7. Add session timeout
8. Use environment-based configuration

## API Documentation

### User Methods in `google_sheets_service.py`

#### `get_user_by_email(email: str) -> Optional[Dict]`
Retrieves user data from Google Sheets.

**Returns:**
```python
{
    'email': 'user@example.com',
    'password_hash': '$2b$12$...',
    'name': 'John Doe'
}
```

#### `create_user(email: str, password_hash: str, name: str) -> bool`
Creates a new user in Google Sheets.

**Returns:** `True` if successful, `False` otherwise.

### User Class in `app.py`

```python
class User(UserMixin):
    def __init__(self, email: str, name: str = ''):
        self.id = email          # Required by Flask-Login
        self.email = email
        self.name = name
```

## Support

If you encounter issues:
1. Check this documentation
2. Review error messages in terminal
3. Verify Google Sheets setup
4. Check service account permissions
5. Ensure all dependencies are installed

---

**Happy coding! 🚀**


# Quick Start - Authentication Feature

## What Was Added

✅ **User Login/Register System** with Google Sheets backend
✅ **Secure Password Hashing** using bcrypt
✅ **Session Management** with Flask-Login
✅ **Modern UI** for login and registration pages
✅ **Flash Messages** for user feedback

## Files Created/Modified

### New Files:
- `templates/login.html` - Login page
- `templates/register.html` - Registration page
- `AUTHENTICATION_SETUP.md` - Complete setup guide

### Modified Files:
- `app.py` - Added auth routes and Flask-Login setup
- `config.py` - Added USERS_WORKSHEET_NAME
- `google_sheets_service.py` - Added user CRUD methods
- `templates/base.html` - Added login/logout buttons and flash messages
- `static/css/main.css` - Added auth page styles
- `requirements.txt` - Added Flask-Login and bcrypt

## Setup Steps

### 1. Create Users Worksheet in Google Sheets

1. Open your Google Spreadsheet
2. Add a new sheet/tab named **"Users"**
3. Add headers in row 1:
   - A1: `Email`
   - B1: `Password`
   - C1: `Name`
   - D1: `Created`

### 2. Grant Editor Permissions

1. In Google Sheets, click **Share**
2. Add your service account email (from `credentials.json`)
3. Set role to **Editor**
4. Save

### 3. Set SECRET_KEY (Important!)

Edit your `.env` file or `config.py`:

```env
SECRET_KEY=your-very-secure-random-key-here
```

Generate a secure key:
```python
import secrets
print(secrets.token_hex(32))
```

### 4. Dependencies Already Installed ✓

Flask-Login and bcrypt are already installed.

## Test It!

### 1. Start the Server

```bash
python app.py
```

### 2. Register a New User

1. Go to: http://localhost:5000/register
2. Fill in:
   - Full Name: Test User
   - Email: test@example.com
   - Password: password123
   - Confirm Password: password123
3. Click "Create Account"
4. You'll be redirected to login

### 3. Check Google Sheets

Open your Users worksheet - you should see the new user with hashed password!

### 4. Login

1. Go to: http://localhost:5000/login
2. Enter your email and password
3. You should see "Hi, Test User!" in the navigation bar

### 5. Logout

Click the "Logout" button in the navigation.

## URLs

- **Home:** http://localhost:5000/
- **Login:** http://localhost:5000/login
- **Register:** http://localhost:5000/register
- **Logout:** http://localhost:5000/logout

## Features

### Navigation Bar (Automatic)
- Not logged in: Shows "Login" and "Register" buttons
- Logged in: Shows "Hi, [Name]!" and "Logout" button

### Flash Messages
- Success messages (green)
- Error messages (red)
- Info messages (blue)

### Form Validation
- All fields required
- Email format validation
- Password minimum 6 characters
- Password confirmation must match
- Duplicate email check

### Security
- Passwords hashed with bcrypt (never stored in plain text)
- Secure session management
- CSRF protection (Flask built-in)

## Making Routes Protected

To require login for a page:

```python
from flask_login import login_required

@application.route('/my-page')
@login_required
def my_page():
    return render_template('my_page.html')
```

## Accessing Current User

In templates:
```html
{% if current_user.is_authenticated %}
  <p>Welcome, {{ current_user.name }}!</p>
{% endif %}
```

In routes:
```python
from flask_login import current_user

user_email = current_user.email
user_name = current_user.name
```

## Troubleshooting

**Problem:** "Users worksheet not found"  
**Solution:** Create the "Users" worksheet with proper headers

**Problem:** "Failed to create user"  
**Solution:** Give service account Editor permissions

**Problem:** Password doesn't work  
**Solution:** Make sure you registered through /register (not manually in sheets)

**Problem:** Sessions not working  
**Solution:** Set a SECRET_KEY in config.py

## What's Next?

Read `AUTHENTICATION_SETUP.md` for:
- Detailed documentation
- Security best practices
- API reference
- Customization options
- Advanced features

---

🎉 **You're all set! Your app now has user authentication!**


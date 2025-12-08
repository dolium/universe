"""
Test script for verifying comments and profiles functionality.
"""
from app import create_app
from google_sheets_service import GoogleSheetsService

def test_google_sheets_service():
    """Test Google Sheets service methods for comments and profiles."""
    print("\n=== Testing Google Sheets Service ===\n")
    
    service = GoogleSheetsService()
    
    # Test 1: Get all users
    print("Test 1: Getting all users...")
    users = service.get_all_users()
    print(f"  Result: Found {len(users)} users")
    if users:
        print(f"  Sample user: {users[0]}")
    
    # Test 2: Get comments (should return empty list or comments)
    print("\nTest 2: Getting comments...")
    comments = service.get_comments()
    print(f"  Result: Found {len(comments)} comments")
    if comments:
        print(f"  Sample comment: {comments[0]}")
    
    # Test 3: Get material comments
    print("\nTest 3: Getting material comments...")
    material_comments = service.get_material_comments('test-course', 'Test Material')
    print(f"  Result: Found {len(material_comments)} comments for material")
    
    # Test 4: Get profile comments
    print("\nTest 4: Getting profile comments...")
    profile_comments = service.get_profile_comments('test@example.com')
    print(f"  Result: Found {len(profile_comments)} comments for profile")
    
    print("\n✅ All Google Sheets Service tests completed successfully!\n")

def test_app_routes():
    """Test app routes for comments and profiles."""
    print("\n=== Testing App Routes ===\n")
    
    app = create_app()
    client = app.test_client()
    
    # Test 1: Profiles page
    print("Test 1: Testing /profiles route...")
    response = client.get('/profiles')
    print(f"  Status code: {response.status_code}")
    assert response.status_code == 200, "Profiles page should return 200"
    print("  ✅ Profiles page loads successfully")
    
    # Test 2: Account page
    print("\nTest 2: Testing /account route (without login)...")
    response = client.get('/account')
    # Should redirect to login
    print(f"  Status code: {response.status_code}")
    assert response.status_code == 302, "Account page should redirect when not logged in"
    print("  ✅ Account page redirects correctly when not logged in")
    
    # Test 3: Add comment route (should require login)
    print("\nTest 3: Testing /add_comment route (without login)...")
    response = client.post('/add_comment', data={
        'comment_type': 'material',
        'reference_id': 'test:test',
        'comment_text': 'Test comment'
    })
    print(f"  Status code: {response.status_code}")
    assert response.status_code == 302, "Add comment should redirect when not logged in"
    print("  ✅ Add comment redirects correctly when not logged in")
    
    print("\n✅ All App Route tests completed successfully!\n")

def test_templates():
    """Test that templates render without errors."""
    print("\n=== Testing Templates ===\n")
    
    app = create_app()
    
    with app.test_request_context():
        from flask import render_template
        
        # Test profiles template with dummy data
        print("Test 1: Rendering profiles.html...")
        try:
            html = render_template('profiles.html', 
                                  users=[{'name': 'Test User', 'email': 'test@example.com', 'created': '2024-01-01'}],
                                  search_query='',
                                  total_count=1,
                                  site_name='UniVerse',
                                  ga_id='',
                                  current_user=None,
                                  verification_email='admin@example.com')
            print("  ✅ profiles.html renders successfully")
        except Exception as e:
            print(f"  ❌ Error rendering profiles.html: {e}")
            raise
        
        # Test account template with comments
        print("\nTest 2: Rendering account.html with comments...")
        try:
            html = render_template('account.html',
                                  user={'name': 'Test User', 'email': 'test@example.com'},
                                  materials=[],
                                  comments=[{'author_name': 'John', 'author_email': 'john@example.com', 
                                           'comment': 'Test comment', 'created': '2024-01-01'}],
                                  is_own_account=False,
                                  site_name='UniVerse',
                                  ga_id='',
                                  current_user=None,
                                  verification_email='admin@example.com')
            print("  ✅ account.html with comments renders successfully")
        except Exception as e:
            print(f"  ❌ Error rendering account.html: {e}")
            raise
    
    print("\n✅ All Template tests completed successfully!\n")

if __name__ == '__main__':
    print("\n" + "="*60)
    print("  RUNNING TESTS FOR COMMENTS AND PROFILES FEATURES")
    print("="*60)
    
    try:
        test_google_sheets_service()
        test_app_routes()
        test_templates()
        
        print("\n" + "="*60)
        print("  ✅ ALL TESTS PASSED!")
        print("="*60 + "\n")
        
    except Exception as e:
        print("\n" + "="*60)
        print(f"  ❌ TEST FAILED: {e}")
        print("="*60 + "\n")
        raise

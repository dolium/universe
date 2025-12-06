"""
Test script to verify that the rating bug fix works correctly.
This test verifies that each material has unique radio button IDs.
"""

from app import app as flask_app
from bs4 import BeautifulSoup


def test_unique_star_ids():
    """Test that each material has unique star rating IDs."""
    print("=" * 60)
    print("TESTING RATING BUG FIX")
    print("=" * 60)
    
    # Create test client
    with flask_app.test_client() as client:
        # Get a course detail page
        response = client.get('/courses/computer-science-i')
        
        if response.status_code != 200:
            print(f"⚠ Course page returned status {response.status_code}")
            return
        
        # Parse HTML
        html = response.data.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        
        # Find all star rating inputs
        star_inputs = soup.find_all('input', {'type': 'radio', 'name': 'rating'})
        
        print(f"\n1. Found {len(star_inputs)} star rating inputs")
        
        if len(star_inputs) == 0:
            print("⚠ No star rating inputs found (user might not be logged in or no materials)")
            return
        
        # Check for duplicate IDs
        ids = [inp.get('id') for inp in star_inputs if inp.get('id')]
        unique_ids = set(ids)
        
        print(f"2. Total IDs: {len(ids)}")
        print(f"3. Unique IDs: {len(unique_ids)}")
        
        if len(ids) != len(unique_ids):
            duplicates = [id_val for id_val in ids if ids.count(id_val) > 1]
            duplicate_set = set(duplicates)
            print(f"\n❌ FAIL: Found {len(duplicate_set)} duplicate IDs:")
            for dup_id in duplicate_set:
                print(f"   - {dup_id} appears {ids.count(dup_id)} times")
            return False
        else:
            print("\n✅ PASS: All star rating IDs are unique!")
        
        # Verify ID pattern (should be star<N>-<M> where N=1-5 and M=material_index)
        print("\n4. Verifying ID patterns:")
        materials_count = len(ids) // 5 if len(ids) % 5 == 0 else 0
        print(f"   Expected {materials_count} materials (5 stars each)")
        
        # Group IDs by material
        material_groups = {}
        for id_val in ids:
            if '-' in id_val:
                parts = id_val.split('-')
                if len(parts) == 2:
                    material_idx = parts[1]
                    if material_idx not in material_groups:
                        material_groups[material_idx] = []
                    material_groups[material_idx].append(id_val)
        
        print(f"   Found {len(material_groups)} material groups:")
        for mat_idx, group_ids in sorted(material_groups.items()):
            print(f"   - Material {mat_idx}: {', '.join(sorted(group_ids))}")
        
        # Verify each material has exactly 5 stars
        all_correct = True
        for mat_idx, group_ids in material_groups.items():
            if len(group_ids) != 5:
                print(f"   ❌ Material {mat_idx} has {len(group_ids)} stars (expected 5)")
                all_correct = False
            expected_ids = [f"star{i}-{mat_idx}" for i in range(1, 6)]
            if sorted(group_ids) != sorted(expected_ids):
                print(f"   ❌ Material {mat_idx} has incorrect IDs")
                all_correct = False
        
        if all_correct:
            print("\n✅ PASS: All materials have correct star rating structure!")
        else:
            print("\n❌ FAIL: Some materials have incorrect star rating structure")
            return False
        
        # Check that labels point to correct inputs
        print("\n5. Verifying label 'for' attributes:")
        star_labels = soup.find_all('label', {'class': 'star-label'})
        print(f"   Found {len(star_labels)} star labels")
        
        label_targets = [label.get('for') for label in star_labels if label.get('for')]
        orphaned_labels = [target for target in label_targets if target not in ids]
        
        if orphaned_labels:
            print(f"   ❌ FAIL: Found {len(orphaned_labels)} labels pointing to non-existent inputs:")
            for target in orphaned_labels[:5]:  # Show first 5
                print(f"      - {target}")
            return False
        else:
            print("   ✅ All labels correctly point to existing inputs")
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED - RATING BUG IS FIXED!")
        print("=" * 60)
        return True


if __name__ == "__main__":
    try:
        result = test_unique_star_ids()
        exit(0 if result else 1)
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)

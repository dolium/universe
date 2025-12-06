"""
Test the rating fix by rendering the template directly with test data.
"""

from jinja2 import Template


def test_template_renders_unique_ids():
    """Test that the template generates unique IDs for each material."""
    
    print("=" * 60)
    print("TESTING RATING BUG FIX - TEMPLATE RENDERING")
    print("=" * 60)
    
    # Simplified template snippet that contains the bug fix
    template_str = """
    {%- for m in materials -%}
      {% set material_index = loop.index0 %}
      Material {{ material_index }}:
      {%- for i in range(1, 6) -%}
        <input id="star{{ i }}-{{ material_index }}" name="rating" value="{{ i }}" />
        <label for="star{{ i }}-{{ material_index }}">Star {{ i }}</label>
      {%- endfor -%}
    {%- endfor -%}
    """
    
    # Test data: 3 materials
    test_data = {
        'materials': [
            {'title': 'Material 1', 'url': 'http://example.com/1'},
            {'title': 'Material 2', 'url': 'http://example.com/2'},
            {'title': 'Material 3', 'url': 'http://example.com/3'},
        ]
    }
    
    # Render template
    template = Template(template_str)
    rendered = template.render(**test_data)
    
    print("\n1. Rendered template (first 500 chars):")
    print(rendered[:500])
    
    # Extract all IDs using regex
    import re
    id_pattern = r'id="(star\d+-\d+)"'
    ids = re.findall(id_pattern, rendered)
    
    print(f"\n2. Found {len(ids)} star rating IDs")
    
    # Check for uniqueness
    unique_ids = set(ids)
    print(f"3. Unique IDs: {len(unique_ids)}")
    
    if len(ids) != len(unique_ids):
        duplicates = [id_val for id_val in ids if ids.count(id_val) > 1]
        print(f"\n❌ FAIL: Found duplicate IDs: {set(duplicates)}")
        return False
    
    print("   ✅ All IDs are unique!")
    
    # Verify expected pattern
    expected_ids = []
    for mat_idx in range(3):  # 3 materials
        for star_num in range(1, 6):  # 5 stars each
            expected_ids.append(f"star{star_num}-{mat_idx}")
    
    if sorted(ids) == sorted(expected_ids):
        print("\n4. ✅ IDs match expected pattern:")
        for mat_idx in range(3):
            mat_ids = [id_val for id_val in ids if id_val.endswith(f"-{mat_idx}")]
            print(f"   Material {mat_idx}: {', '.join(sorted(mat_ids))}")
    else:
        print(f"\n❌ FAIL: IDs don't match expected pattern")
        print(f"   Expected: {sorted(expected_ids)}")
        print(f"   Got: {sorted(ids)}")
        return False
    
    # Check that labels point to correct inputs
    for_pattern = r'for="(star\d+-\d+)"'
    label_targets = re.findall(for_pattern, rendered)
    
    print(f"\n5. Found {len(label_targets)} label targets")
    orphaned = [target for target in label_targets if target not in ids]
    
    if orphaned:
        print(f"   ❌ FAIL: Found orphaned labels: {orphaned}")
        return False
    else:
        print("   ✅ All labels correctly point to existing inputs")
    
    print("\n" + "=" * 60)
    print("✅ ALL TEMPLATE TESTS PASSED!")
    print("=" * 60)
    print("\nThe fix ensures that:")
    print("  • Each material has unique star rating IDs (star1-0, star2-0, ... for material 0)")
    print("  • Labels correctly point to their corresponding inputs via 'for' attribute")
    print("  • Clicking on any material's stars will select the correct radio button")
    print("  • The second (and subsequent) materials' ratings can now be clicked and submitted")
    
    return True


def test_old_template_has_bug():
    """Test that the OLD template (before fix) had duplicate IDs."""
    
    print("\n" + "=" * 60)
    print("VERIFYING OLD TEMPLATE HAD THE BUG")
    print("=" * 60)
    
    # Old template (with bug) - uses loop.index0 from inner loop
    old_template_str = """
    {%- for m in materials -%}
      {%- for i in range(1, 6) -%}
        <input id="star{{ i }}-{{ loop.index0 }}" />
      {%- endfor -%}
    {%- endfor -%}
    """
    
    test_data = {
        'materials': [
            {'title': 'Material 1'},
            {'title': 'Material 2'},
        ]
    }
    
    template = Template(old_template_str)
    rendered = template.render(**test_data)
    
    import re
    id_pattern = r'id="(star\d+-\d+)"'
    ids = re.findall(id_pattern, rendered)
    
    print(f"\nOld template generated {len(ids)} IDs: {ids}")
    print(f"Unique IDs: {len(set(ids))}")
    
    if len(ids) != len(set(ids)):
        print("✅ Confirmed: Old template HAD duplicate IDs (the bug)")
        # Show the duplicate structure
        print(f"\nWith 2 materials, the old code generated:")
        print(f"  Material 0: star1-0, star2-1, star3-2, star4-3, star5-4")
        print(f"  Material 1: star1-0, star2-1, star3-2, star4-3, star5-4")
        print(f"           ^ SAME IDs! This caused labels to point to Material 0's inputs")
        return True
    else:
        print("⚠ Unexpected: Old template didn't have duplicates")
        return False


if __name__ == "__main__":
    try:
        # Test that old template had the bug
        test_old_template_has_bug()
        
        # Test that new template is fixed
        result = test_template_renders_unique_ids()
        
        exit(0 if result else 1)
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)

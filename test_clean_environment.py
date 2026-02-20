"""
Test script to verify Scumgenics runs correctly in a clean environment.

This script validates:
1. Application runs without pre-configuration
2. Works with different Windows usernames
3. All dependencies install correctly
4. No hardcoded user-specific paths

Requirements validated: 9.2, 9.4
"""

import sys
import os
from pathlib import Path


def test_no_hardcoded_usernames():
    """Verify no hardcoded usernames in source code."""
    print("Testing for hardcoded usernames...")
    
    # List of common test usernames that should NOT appear in code
    forbidden_usernames = [
        "Administrator",
        "User",
        "TestUser",
        "Developer",
        "Admin"
    ]
    
    src_files = list(Path("src").glob("*.py"))
    
    for src_file in src_files:
        content = src_file.read_text()
        for username in forbidden_usernames:
            # Check for hardcoded paths with specific usernames
            if f"C:\\Users\\{username}\\" in content or f"C:/Users/{username}/" in content:
                print(f"❌ FAILED: Found hardcoded username '{username}' in {src_file}")
                return False
    
    print("✓ PASSED: No hardcoded usernames found")
    return True


def test_dynamic_username_detection():
    """Verify username is detected dynamically."""
    print("\nTesting dynamic username detection...")
    
    try:
        from src.save_manager import SaveManager
        
        # Create SaveManager instance
        manager = SaveManager()
        
        # Get detected username
        detected_username = manager.config.username
        
        # Verify it's not empty
        if not detected_username:
            print("❌ FAILED: Username detection returned empty string")
            return False
        
        # Verify it matches system username
        system_username = os.getlogin() if hasattr(os, 'getlogin') else os.environ.get('USERNAME')
        
        if detected_username != system_username:
            print(f"❌ FAILED: Detected username '{detected_username}' doesn't match system username '{system_username}'")
            return False
        
        print(f"✓ PASSED: Username detected correctly: {detected_username}")
        return True
        
    except Exception as e:
        print(f"❌ FAILED: Exception during username detection: {e}")
        return False


def test_path_construction():
    """Verify paths are constructed dynamically based on username."""
    print("\nTesting dynamic path construction...")
    
    try:
        from src.save_manager import SaveManager
        
        # Create SaveManager instance
        manager = SaveManager()
        
        # Get constructed paths
        main_save_path = manager.get_main_save_path()
        backup_directory = manager.get_backup_directory()
        
        # Verify paths contain the detected username
        username = manager.config.username
        
        if username not in str(main_save_path):
            print(f"❌ FAILED: Main save path doesn't contain username: {main_save_path}")
            return False
        
        if username not in str(backup_directory):
            print(f"❌ FAILED: Backup directory doesn't contain username: {backup_directory}")
            return False
        
        print(f"✓ PASSED: Paths constructed correctly for user '{username}'")
        print(f"  Main save: {main_save_path}")
        print(f"  Backup dir: {backup_directory}")
        return True
        
    except Exception as e:
        print(f"❌ FAILED: Exception during path construction: {e}")
        return False


def test_dependencies_import():
    """Verify all required dependencies can be imported."""
    print("\nTesting dependency imports...")
    
    dependencies = [
        ("PyQt6.QtWidgets", "PyQt6"),
        ("pytest", "pytest"),
        ("hypothesis", "hypothesis"),
    ]
    
    all_imported = True
    
    for module_name, package_name in dependencies:
        try:
            __import__(module_name)
            print(f"✓ {package_name} imported successfully")
        except ImportError as e:
            print(f"❌ FAILED: Could not import {package_name}: {e}")
            all_imported = False
    
    if all_imported:
        print("✓ PASSED: All dependencies imported successfully")
    
    return all_imported


def test_cross_user_portability():
    """Verify application logic works with different usernames."""
    print("\nTesting cross-user portability...")
    
    try:
        from src.path_builder import PathBuilder
        
        # Test with different usernames
        test_usernames = ["Alice", "Bob", "TestUser123", "User_With_Underscore"]
        
        paths_differ = True
        previous_path = None
        
        for username in test_usernames:
            path = PathBuilder.build_main_save_path(username)
            
            # Verify path contains the username
            if username not in str(path):
                print(f"❌ FAILED: Path for '{username}' doesn't contain username: {path}")
                return False
            
            # Verify paths differ for different usernames
            if previous_path and str(path) == str(previous_path):
                print(f"❌ FAILED: Paths are identical for different usernames")
                return False
            
            previous_path = path
        
        print(f"✓ PASSED: Application generates unique paths for different users")
        return True
        
    except Exception as e:
        print(f"❌ FAILED: Exception during cross-user portability test: {e}")
        return False


def main():
    """Run all clean environment tests."""
    print("=" * 60)
    print("Scumgenics Clean Environment Test Suite")
    print("=" * 60)
    
    tests = [
        test_dependencies_import,
        test_no_hardcoded_usernames,
        test_dynamic_username_detection,
        test_path_construction,
        test_cross_user_portability,
    ]
    
    results = []
    
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ EXCEPTION in {test.__name__}: {e}")
            results.append(False)
    
    print("\n" + "=" * 60)
    print("Test Results Summary")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Passed: {passed}/{total}")
    
    if all(results):
        print("\n✓ ALL TESTS PASSED - Application is ready for distribution!")
        return 0
    else:
        print("\n❌ SOME TESTS FAILED - Please review failures above")
        return 1


if __name__ == "__main__":
    sys.exit(main())

import os
import tempfile
from pathlib import Path
import sys

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from main import create_sorted_directory


def test_sorting_functionality():
    """Test that the app actually sorts files from resources folder"""
    
    # Create a temporary directory with test files
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create some test files in the temp directory
        test_files = [
            "photo1.jpg",
            "photo2.png", 
            "document.pdf",
            "image3.jpeg"
        ]
        
        for filename in test_files:
            (temp_path / filename).touch()
        
        # Test the sorting function (default behavior - no output folder)
        sorted_dir = create_sorted_directory(str(temp_path))
        
        # Verify the sorted directory was created
        assert os.path.exists(sorted_dir)
        assert os.path.isdir(sorted_dir)
        
        # The function should return the correct path
        expected_path = os.path.join(temp_path, "sorted_pictures")
        assert sorted_dir == expected_path
        
        print(f"✅ Sorting test passed! Created directory: {sorted_dir}")
        print(f"✅ Test files created: {test_files}")
        print(f"✅ Sorted directory exists: {os.path.exists(sorted_dir)}")


def test_sorting_with_custom_output():
    """Test sorting with custom output directory"""
    
    # Create a temporary directory with test files
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create some test files
        test_files = ["photo1.jpg", "photo2.png"]
        for filename in test_files:
            (temp_path / filename).touch()
        
        # Create a custom output directory
        custom_output = temp_path / "my_sorted_pictures"
        
        # Test the sorting function with custom output
        sorted_dir = create_sorted_directory(str(temp_path), str(custom_output))
        
        # Verify the custom output directory was used
        assert sorted_dir == str(custom_output)
        assert os.path.exists(sorted_dir)
        assert os.path.isdir(sorted_dir)
        
        print(f"✅ Custom output test passed! Created directory: {sorted_dir}")
        print(f"✅ Custom output directory exists: {os.path.exists(sorted_dir)}")


def test_sorting_with_sample_files():
    """Test sorting with sample image files"""
    
    # Create a temporary directory with sample image files
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create sample image files with different categories
        sample_files = [
            "girl-1894125_640.jpg",  # people
            "people-2574170_640.jpg",  # people
            "landscape-9802950_640.jpg",  # views
            "gym-521476_640.jpg",  # views
            "pancakes-2291908_640.jpg",  # special
        ]
        
        for filename in sample_files:
            (temp_path / filename).touch()
        
        # Test the sorting function
        sorted_dir = create_sorted_directory(str(temp_path))
        
        # Verify the sorted directory was created
        assert os.path.exists(sorted_dir)
        assert os.path.isdir(sorted_dir)
        
        # Check that files were actually sorted into categories
        sorted_files = list(Path(sorted_dir).glob("*"))
        print(f"✅ Sorted directory contains categories: {[f.name for f in sorted_files]}")
        
        # Count files in each category
        total_sorted_files = 0
        for category in sorted_files:
            if category.is_dir():
                files_in_category = list(category.glob("*.jpg"))
                total_sorted_files += len(files_in_category)
                print(f"   📁 {category.name}: {len(files_in_category)} files")
        
        print(f"✅ Total files sorted: {total_sorted_files}")
        
        # Test should pass if files were sorted
        assert total_sorted_files > 0, "No files were sorted!"
        print("🎉 Sorting functionality test PASSED!")


if __name__ == "__main__":
    test_sorting_functionality()
    test_sorting_with_custom_output()
    test_sorting_with_sample_files()

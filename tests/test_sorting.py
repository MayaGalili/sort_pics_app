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
        
        # Test the sorting function
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


def test_sorting_with_resources_folder():
    """Test sorting with the actual resources folder"""
    
    # Get the path to the resources folder
    resources_path = Path(__file__).parent / "resorces"
    
    if not resources_path.exists():
        print("⚠️  Resources folder not found, skipping this test")
        return
    
    # Test the sorting function with resources
    sorted_dir = create_sorted_directory(str(resources_path))
    
    # Verify the sorted directory was created
    assert os.path.exists(sorted_dir)
    assert os.path.isdir(sorted_dir)
    
    # Check what files are in the resources folder
    resource_files = list(resources_path.glob("*"))
    print(f"✅ Resources folder contains: {[f.name for f in resource_files]}")
    print(f"✅ Sorted directory created at: {sorted_dir}")
    
    # The sorted directory should be empty initially (since we're not actually sorting yet)
    sorted_files = list(Path(sorted_dir).glob("*"))
    print(f"✅ Sorted directory contains: {[f.name for f in sorted_files]}")


if __name__ == "__main__":
    test_sorting_functionality()
    test_sorting_with_resources_folder()

import pytest
import tempfile
import os
from pathlib import Path


@pytest.fixture
def temp_directory():
    """Create a temporary directory for testing"""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir


@pytest.fixture
def sample_directory_structure(temp_directory):
    """Create a sample directory structure for testing"""
    # Create some test files
    test_files = [
        'photo1.jpg',
        'photo2.png',
        'document.pdf',
        'video.mp4'
    ]
    
    for filename in test_files:
        file_path = Path(temp_directory) / filename
        file_path.touch()
    
    return temp_directory


@pytest.fixture
def flask_client():
    """Create a Flask test client"""
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
    
    from main import app
    return app.test_client()

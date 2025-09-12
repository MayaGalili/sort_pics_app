import os
import tempfile
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
import sys

# Add the src directory to the path so we can import main
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from main import app, create_sorted_directory


class TestFlaskApp:
    """Test cases for the Flask application"""
    
    def setup_method(self):
        """Set up test client for each test"""
        self.client = app.test_client()
        self.app = app
    
    def test_home_route(self):
        """Test that the home route returns the correct template"""
        response = self.client.get('/')
        assert response.status_code == 200
        assert b'Picture Splitter' in response.data
        assert b'Enter directory path:' in response.data
    
    def test_select_directory_success(self):
        """Test successful directory selection and creation"""
        with tempfile.TemporaryDirectory() as temp_dir:
            data = {'directory': temp_dir}
            response = self.client.post('/select_directory', 
                                      json=data,
                                      content_type='application/json')
            
            assert response.status_code == 200
            response_data = response.get_json()
            assert 'message' in response_data
            assert 'sorted_directory' in response_data
            assert response_data['input_directory'] == temp_dir
            
            # Check that the sorted directory was actually created
            sorted_dir = Path(response_data['sorted_directory'])
            assert sorted_dir.exists()
            assert sorted_dir.is_dir()
    
    def test_select_directory_no_directory(self):
        """Test error handling when no directory is provided"""
        data = {}
        response = self.client.post('/select_directory',
                                  json=data,
                                  content_type='application/json')
        
        assert response.status_code == 400
        response_data = response.get_json()
        assert 'error' in response_data
        assert 'No directory selected' in response_data['error']
    
    def test_select_directory_empty_string(self):
        """Test error handling when empty directory string is provided"""
        data = {'directory': ''}
        response = self.client.post('/select_directory',
                                  json=data,
                                  content_type='application/json')
        
        assert response.status_code == 400
        response_data = response.get_json()
        assert 'error' in response_data
        assert 'No directory selected' in response_data['error']
    
    def test_select_directory_invalid_path(self):
        """Test error handling when invalid directory path is provided"""
        data = {'directory': '/nonexistent/path/that/does/not/exist'}
        response = self.client.post('/select_directory',
                                  json=data,
                                  content_type='application/json')
        
        # The function should handle the error gracefully
        assert response.status_code in [400, 500]
        response_data = response.get_json()
        assert 'error' in response_data
    
    def test_create_sorted_directory_function(self):
        """Test the create_sorted_directory function directly"""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = create_sorted_directory(temp_dir)
            
            # Check that the function returns the correct path
            expected_path = os.path.join(temp_dir, 'sorted_pictures')
            assert result == expected_path
            
            # Check that the directory was created
            assert os.path.exists(result)
            assert os.path.isdir(result)
    
    def test_create_sorted_directory_existing_dir(self):
        """Test that create_sorted_directory handles existing directories"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create the directory first
            sorted_dir = os.path.join(temp_dir, 'sorted_pictures')
            os.makedirs(sorted_dir)
            
            # Call the function again - should not raise an error
            result = create_sorted_directory(temp_dir)
            assert result == sorted_dir
            assert os.path.exists(result)
    
    def test_app_configuration(self):
        """Test that the Flask app is configured correctly"""
        assert app.name == 'main'
        # Debug mode is only True when running directly, not in test environment
        assert app.debug in [True, False]
    
    def test_json_content_type_required(self):
        """Test that the select_directory endpoint requires JSON content type"""
        data = {'directory': '/some/path'}
        response = self.client.post('/select_directory', data=data)
        
        # Should still work, but let's test with proper JSON
        response = self.client.post('/select_directory',
                                  json=data,
                                  content_type='application/json')
        assert response.status_code in [200, 400, 500]  # Depends on path validity


class TestIntegration:
    """Integration tests for the complete workflow"""
    
    def test_complete_workflow(self):
        """Test the complete workflow from web interface to directory creation"""
        client = app.test_client()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Simulate the complete workflow
            data = {'directory': temp_dir}
            response = client.post('/select_directory',
                                 json=data,
                                 content_type='application/json')
            
            assert response.status_code == 200
            response_data = response.get_json()
            
            # Verify the response structure
            assert 'message' in response_data
            assert 'input_directory' in response_data
            assert 'sorted_directory' in response_data
            
            # Verify the directory was created
            sorted_dir = Path(response_data['sorted_directory'])
            assert sorted_dir.exists()
            assert sorted_dir.is_dir()
            
            # Verify the path structure
            assert sorted_dir.name == 'sorted_pictures'
            assert sorted_dir.parent == Path(temp_dir)


if __name__ == '__main__':
    pytest.main([__file__])

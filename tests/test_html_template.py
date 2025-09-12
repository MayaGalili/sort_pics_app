import os
import sys
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from main import app


class TestHTMLTemplate:
    """Test cases for the HTML template rendering"""
    
    def setup_method(self):
        """Set up test client for each test"""
        self.client = app.test_client()
    
    def test_template_rendering(self):
        """Test that the template renders correctly"""
        response = self.client.get('/')
        assert response.status_code == 200
        
        # Check for key HTML elements
        html_content = response.get_data(as_text=True)
        
        # Check for basic HTML structure
        assert '<!DOCTYPE html>' in html_content
        assert '<html lang="en">' in html_content
        assert '<head>' in html_content
        assert '<body>' in html_content
        
        # Check for title
        assert '<title>Picture Splitter</title>' in html_content
        
        # Check for main heading
        assert '<h1>Picture Splitter</h1>' in html_content
        
        # Check for form elements
        assert 'Enter directory path:' in html_content
        assert 'input type="text"' in html_content
        assert 'id="directory"' in html_content
        assert 'placeholder="Enter the full path to your pictures directory"' in html_content
        
        # Check for button
        assert 'Create Sorted Directory' in html_content
        assert 'onclick="selectDirectory()"' in html_content
        
        # Check for JavaScript
        assert 'function selectDirectory()' in html_content
        assert 'fetch(\'/select_directory\'' in html_content
        
        # Check for CSS classes
        assert 'class="container"' in html_content
        assert 'class="input-group"' in html_content
        # These classes are used in JavaScript, not in the initial HTML
        assert '.success' in html_content
        assert '.error' in html_content
    
    def test_css_styling(self):
        """Test that CSS styles are included"""
        response = self.client.get('/')
        html_content = response.get_data(as_text=True)
        
        # Check for key CSS styles
        assert 'font-family: Arial, sans-serif' in html_content
        assert 'background-color: #f5f5f5' in html_content
        assert 'background-color: #4CAF50' in html_content
        assert 'border-radius: 8px' in html_content
        assert 'box-shadow: 0 2px 4px rgba(0,0,0,0.1)' in html_content
    
    def test_javascript_functionality(self):
        """Test that JavaScript functions are present"""
        response = self.client.get('/')
        html_content = response.get_data(as_text=True)
        
        # Check for JavaScript functions
        assert 'async function selectDirectory()' in html_content
        assert 'document.getElementById(\'directory\')' in html_content
        assert 'response.ok' in html_content
        assert 'JSON.stringify' in html_content
        assert "'Content-Type': 'application/json'" in html_content


if __name__ == '__main__':
    pytest.main([__file__])

# Test Suite for Picture Sorting Application

This directory contains comprehensive tests for the Picture Sorting Application.

## Test Structure

- `test_app.py` - Main application tests (Flask routes, API endpoints, core functionality)
- `test_html_template.py` - Template rendering and HTML structure tests
- `conftest.py` - Pytest fixtures and configuration
- `__init__.py` - Package initialization

## Running Tests

### Run All Tests
```bash
# From project root
python run_tests.py

# Or directly with pytest
pytest tests/ -v --cov=src
```

### Run Specific Test Files
```bash
pytest tests/test_app.py -v
pytest tests/test_html_template.py -v
```

### Run with Coverage Report
```bash
pytest tests/ --cov=src --cov-report=html
```

## Test Coverage

The test suite covers:

### Flask Application (`test_app.py`)
- ✅ Home route rendering
- ✅ Directory selection API endpoint
- ✅ Successful directory creation
- ✅ Error handling for missing directories
- ✅ Error handling for invalid paths
- ✅ Directory creation function
- ✅ Integration tests for complete workflow

### HTML Template (`test_html_template.py`)
- ✅ Template rendering
- ✅ HTML structure validation
- ✅ CSS styling presence
- ✅ JavaScript functionality
- ✅ Form elements and user interface

### Error Scenarios
- ✅ Missing directory parameter
- ✅ Empty directory string
- ✅ Invalid directory paths
- ✅ Network/connection errors

## Test Data

Tests use temporary directories created with Python's `tempfile` module to ensure:
- No interference with actual file system
- Clean test environment for each test
- Automatic cleanup after tests complete

## Fixtures

- `temp_directory` - Creates temporary directory for testing
- `sample_directory_structure` - Creates test files in temporary directory
- `flask_client` - Provides Flask test client for API testing

## Continuous Integration

The test suite is designed to run in CI/CD environments and provides:
- Detailed test output with `-v` flag
- Coverage reporting
- HTML coverage reports for detailed analysis
- Exit codes for automated testing pipelines

import os
from pathlib import Path
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def categorize_image(image_file):
    """Categorize an image file based on its filename"""
    filename_lower = image_file.name.lower()
    
    if any(keyword in filename_lower for keyword in ['people', 'person', 'girl', 'woman', 'man', 'boy']):
        return "people"
    elif any(keyword in filename_lower for keyword in ['landscape', 'grassland', 'gym', 'building']):
        return "views"
    else:
        return "special"

def copy_to_category(image_file, sorted_dir, category):
    """Copy an image file to its appropriate category directory"""
    # Create category directory if it doesn't exist
    category_dir = sorted_dir / category
    category_dir.mkdir(exist_ok=True)
    
    # Copy file to the appropriate category
    destination = category_dir / image_file.name
    if not destination.exists():
        import shutil
        shutil.copy2(image_file, destination)

def create_sorted_directory(input_path, output_path=None):
    """Create a subdirectory for sorted pictures and actually sort files"""
    input_path = Path(input_path)
    
    # If no output path specified, create sorted_pictures in input folder
    if output_path is None:
        sorted_dir = input_path / "sorted_pictures"
    else:
        sorted_dir = Path(output_path)
    
    sorted_dir.mkdir(parents=True, exist_ok=True)
    
    # Find all image files in the input directory
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'}
    image_files = []
    
    for file_path in input_path.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in image_extensions:
            image_files.append(file_path)
    
    # Sort files into categories
    for image_file in image_files:
        category = categorize_image(image_file)
        copy_to_category(image_file, sorted_dir, category)
    
    return str(sorted_dir)

@app.route('/')
def home():
    """Render the home page"""
    return render_template('index.html')

@app.route('/select_directory', methods=['POST'])
def select_directory():
    """Handle directory selection and creation of sorted directory"""
    data = request.get_json()
    input_directory = data.get('input_directory')
    output_directory = data.get('output_directory')  # Optional output folder
    
    if not input_directory:
        return jsonify({'error': 'No input directory selected'}), 400
    
    try:
        sorted_directory = create_sorted_directory(input_directory, output_directory)
        return jsonify({
            'message': 'Pictures sorted successfully',
            'input_directory': input_directory,
            'output_directory': output_directory,
            'sorted_directory': sorted_directory
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)

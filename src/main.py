import os
from pathlib import Path
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def create_sorted_directory(input_path):
    """Create a subdirectory for sorted pictures"""
    sorted_dir = Path(input_path) / "sorted_pictures"
    sorted_dir.mkdir(exist_ok=True)
    return str(sorted_dir)

@app.route('/')
def home():
    """Render the home page"""
    return render_template('index.html')

@app.route('/select_directory', methods=['POST'])
def select_directory():
    """Handle directory selection and creation of sorted directory"""
    data = request.get_json()
    input_directory = data.get('directory')
    
    if not input_directory:
        return jsonify({'error': 'No directory selected'}), 400
    
    try:
        sorted_directory = create_sorted_directory(input_directory)
        return jsonify({
            'message': 'Directory created successfully',
            'input_directory': input_directory,
            'sorted_directory': sorted_directory
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

import os
from pathlib import Path
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

app = Flask(__name__)

# ++++++++++++++++++++ PYTORCH ++++++++++++++++++++

import torch
from torchvision import models, transforms
from PIL import Image

model = models.resnet18(pretrained=True)
model.eval()

transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

import urllib.request

url = "https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt"
imagenet_classes = urllib.request.urlopen(url).read().decode("utf-8").splitlines()

def map_to_custom(label: str) -> str:
    label = label.lower()
    if any(x in label for x in ["person", "man", "woman", "boy", "girl"]):
        return "people"
    elif any(x in label for x in ["food", "dish", "pizza", "cake", "sandwich", "fruit", "vegetable", "meat"]):
        return "food"
    elif any(x in label for x in ["mountain", "valley", "volcano", "cliff", "beach", "forest", "field", "lake"]):
        return "landscape"
    else:
        return "other"

def categorize_image(image_path: str) -> str:
    image = Image.open(image_path).convert("RGB")
    img_t = transform(image).unsqueeze(0)

    with torch.no_grad():
        outputs = model(img_t)
        _, predicted = outputs.max(1)

    label = imagenet_classes[predicted.item()]
    category = map_to_custom(label)
    return category, label

# ++++++++++++++++++++ OPENAI ++++++++++++++++++++

from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def categorize_image_by_openai(image_path):
    import base64

    with open(image_path, "rb") as f:
        image_data = f.read()
        base64_image = base64.b64encode(image_data).decode('utf-8')

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an image classifier. Return only one word: people, food, landscape, or other."},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Classify this image into one of: people, food, landscape, other."},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ],
                },
            ],
        )
    return response.choices[0].message.content.strip().lower()

# ++++++++++++++++++++ NAME ++++++++++++++++++++

def categorize_image_by_name(image_file):
    """Categorize an image file based on its filename"""
    filename_lower = image_file.name.lower()

    if any(keyword in filename_lower for keyword in ['people', 'person', 'girl', 'woman', 'man', 'boy']):
        return "people"
    elif any(keyword in filename_lower for keyword in ['landscape', 'grassland', 'gym', 'building']):
        return "views"
    else:
        return "special"

# ++++++++++++++++++++ wrapper ++++++++++++++++++++

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
        try:
            category = categorize_image(str(image_file))
            # Map OpenAI categories to our folder structure
            if category in ['people']:
                category = 'people'
            elif category in ['landscape']:
                category = 'views'
            else:  # food, other, etc.
                category = 'special'
        except Exception as e:
            print(f"Error categorizing {image_file.name}: {e}")
            # Fallback to filename-based categorization
            category = categorize_image_by_name(image_file)
        
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

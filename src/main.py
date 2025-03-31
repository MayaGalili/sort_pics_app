import os
import shutil
from datetime import datetime
from pathlib import Path
import cv2
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
from PIL import Image
from tqdm import tqdm
import logging

# Setup logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ImageSorter:
    def __init__(self):
        # Load MobileNetV2 model for image classification
        try:
            self.model = hub.load('https://tfhub.dev/google/imagenet/mobilenet_v2_100_224/classification/4')
            logger.info("Model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise
        
        # Define categories
        self.categories = {
            'people': ['person', 'people', 'human', 'face', 'portrait'],
            'views': ['building', 'architecture', 'landscape', 'nature', 'sky', 'mountain', 'beach'],
            'special': ['screen', 'receipt', 'document', 'text']
        }
        
    def get_image_date(self, image_path):
        """Returns the capture date of the image"""
        try:
            img = Image.open(image_path)
            exif = img._getexif()
            if exif and 36867 in exif:  # 36867 is DateTimeOriginal tag
                date_str = exif[36867]
                return datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S')
        except Exception as e:
            logger.warning(f"Could not read image date from {image_path}: {e}")
        
        # If we couldn't read the date, use file modification time
        return datetime.fromtimestamp(os.path.getmtime(image_path))
    
    def classify_image(self, image_path):
        """Classifies the image into appropriate category"""
        try:
            # Load image
            img = cv2.imread(str(image_path))
            if img is None:
                logger.error(f"Could not load image: {image_path}")
                return 'special'
                
            img = cv2.resize(img, (224, 224))
            img = img / 255.0
            img = np.expand_dims(img, axis=0)
            
            # Classify image
            predictions = self.model(img)
            predicted_class = tf.argmax(predictions[0]).numpy()
            
            # Check appropriate category
            for category, keywords in self.categories.items():
                if any(keyword in str(predicted_class).lower() for keyword in keywords):
                    return category
            
            return 'special'  # default category
            
        except Exception as e:
            logger.error(f"Error classifying image {image_path}: {e}")
            return 'special'
    
    def create_summary(self, date_folder):
        """Creates daily summary"""
        summary_path = date_folder / 'summary.txt'
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(f"Daily Summary - {date_folder.name}\n")
            f.write("=" * 50 + "\n\n")
            f.write("Brief description of the day...\n")  # We can add more advanced summary logic here
    
    def process_folder(self, source_folder, out_folder):
        """Processes source folder and sorts images"""
        source_path = Path(source_folder)
        
        # Collect all files
        image_files = []
        for ext in ['.jpg', '.jpeg', '.png', '.pdf']:
            image_files.extend(list(source_path.glob(f'**/*{ext}')))
        
        logger.info(f"Found {len(image_files)} files to process")
        
        # Process each file
        for image_path in tqdm(image_files, desc="Processing images"):
            try:
                # Get image date
                date = self.get_image_date(image_path)
                date_folder = source_path / date.strftime('%Y-%m-%d')
                
                # Classify image
                category = self.classify_image(image_path)
                
                # Move file to appropriate folder
                (out_folder / category).mkdir(parents=True, exist_ok=True)

                target_path = out_folder / category / image_path.name
                shutil.copy2(image_path, target_path)
                
                # Create daily summary
                self.create_summary(date_folder)
                
            except Exception as e:
                logger.error(f"Error processing file {image_path}: {e}")

def main():
    try:
        # Create sorter instance
        sorter = ImageSorter()
        
        # Get source folder from user
        source_folder = input("Enter the path to source folder: ")

        out_folder = input("Enter the path to output folder: ")
        
        if not os.path.exists(source_folder):
            logger.error("Folder does not exist!")
            return
        
        # Start the process
        logger.info("Starting sorting process...")
        sorter.process_folder(source_folder, out_folder)
        logger.info("Process completed successfully!")
        
    except Exception as e:
        logger.error(f"General error: {e}")

if __name__ == "__main__":
    main() 
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

# הגדרת לוגר
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ImageSorter:
    def __init__(self):
        # טעינת מודל MobileNetV2 לסיווג תמונות
        self.model = hub.load('https://tfhub.dev/google/imagenet/mobilenet_v2_100_224/classification/4')
        
        # הגדרת קטגוריות
        self.categories = {
            'people': ['person', 'people', 'human', 'face', 'portrait'],
            'views': ['building', 'architecture', 'landscape', 'nature', 'sky', 'mountain', 'beach'],
            'special': ['screen', 'receipt', 'document', 'text']
        }
        
    def get_image_date(self, image_path):
        """מחזיר את תאריך הצילום של התמונה"""
        try:
            img = Image.open(image_path)
            exif = img._getexif()
            if exif and 36867 in exif:  # 36867 הוא תגית DateTimeOriginal
                date_str = exif[36867]
                return datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S')
        except Exception as e:
            logger.warning(f"לא ניתן לקרוא את תאריך התמונה {image_path}: {e}")
        
        # אם לא הצלחנו לקרוא את התאריך, נשתמש בתאריך הקובץ
        return datetime.fromtimestamp(os.path.getmtime(image_path))
    
    def classify_image(self, image_path):
        """מסווג את התמונה לקטגוריה המתאימה"""
        try:
            # טעינת התמונה
            img = cv2.imread(str(image_path))
            img = cv2.resize(img, (224, 224))
            img = img / 255.0
            img = np.expand_dims(img, axis=0)
            
            # סיווג התמונה
            predictions = self.model(img)
            predicted_class = tf.argmax(predictions[0]).numpy()
            
            # בדיקת הקטגוריה המתאימה
            for category, keywords in self.categories.items():
                if any(keyword in str(predicted_class).lower() for keyword in keywords):
                    return category
            
            return 'special'  # ברירת מחדל
            
        except Exception as e:
            logger.error(f"שגיאה בסיווג התמונה {image_path}: {e}")
            return 'special'
    
    def create_summary(self, date_folder):
        """יוצר סיכום יומי"""
        summary_path = date_folder / 'summary.txt'
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(f"סיכום יומי - {date_folder.name}\n")
            f.write("=" * 50 + "\n\n")
            f.write("תיאור קצר של היום...\n")  # כאן נוכל להוסיף לוגיקה מתקדמת יותר ליצירת סיכום
    
    def process_folder(self, source_folder):
        """מעבד את תיקיית המקור וממיינת את התמונות"""
        source_path = Path(source_folder)
        
        # איסוף כל הקבצים
        image_files = []
        for ext in ['.jpg', '.jpeg', '.png', '.pdf']:
            image_files.extend(list(source_path.glob(f'**/*{ext}')))
        
        logger.info(f"נמצאו {len(image_files)} קבצים לעיבוד")
        
        # עיבוד כל קובץ
        for image_path in tqdm(image_files, desc="מעבד תמונות"):
            try:
                # קבלת תאריך התמונה
                date = self.get_image_date(image_path)
                date_folder = source_path / date.strftime('%Y-%m-%d')
                
                # יצירת תיקיות
                for category in ['people', 'views', 'special']:
                    (date_folder / category).mkdir(parents=True, exist_ok=True)
                
                # סיווג התמונה
                category = self.classify_image(image_path)
                
                # העברת הקובץ לתיקייה המתאימה
                target_path = date_folder / category / image_path.name
                shutil.copy2(image_path, target_path)
                
                # יצירת סיכום יומי
                self.create_summary(date_folder)
                
            except Exception as e:
                logger.error(f"שגיאה בעיבוד הקובץ {image_path}: {e}")

def main():
    # יצירת מופע של הממיין
    sorter = ImageSorter()
    
    # קבלת תיקיית המקור מהמשתמש
    source_folder = input("הכנס את הנתיב לתיקיית המקור: ")
    
    if not os.path.exists(source_folder):
        logger.error("התיקייה לא קיימת!")
        return
    
    # התחלת התהליך
    logger.info("מתחיל בתהליך המיון...")
    sorter.process_folder(source_folder)
    logger.info("התהליך הושלם בהצלחה!")

if __name__ == "__main__":
    main() 
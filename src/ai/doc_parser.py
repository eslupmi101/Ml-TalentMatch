from typing import List
import aspose.words as aw
from pathlib import Path
import cv2
import os


def detect_face(img_path):
    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_classifier = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = face_classifier.detectMultiScale(
        gray, scaleFactor=1.2, minNeighbors=5)
    return faces


def clear_imagies(imagies_path: str):
    img_count = 0
    for raw_image in os.listdir(imagies_path):
        raw_img = os.path.join(imagies_path, raw_image)
        if len(detect_face(raw_img)) != 1 or img_count > 1:
            os.remove(raw_img)
            continue
        img_count += 1


def make_md(raw_doc_path: str, image_path: str, md_save_path: str = "src/ai/md") -> List[str]:
    doc = aw.Document(raw_doc_path)

    saveOptions = aw.saving.MarkdownSaveOptions()
    saveOptions.images_folder = image_dir

    md_save_path = os.path.join(md_save_path, Path(raw_doc_path).stem)
    md_save_path = md_save_path + ".md"

    doc.save(md_save_path, saveOptions)
    clear_imagies(image_path)


image_dir = "src/ai/img"
md_dir = "src/ai/md"
raw_document_path = "src/ai/resume"

if not os.path.exists(image_dir):
    os.makedirs(image_dir)

if not os.path.exists(md_dir):
    os.makedirs(md_dir)

for raw_doc in os.listdir(raw_document_path):
    raw_document = os.path.join(raw_document_path, raw_doc)
    make_md(raw_document, image_dir)

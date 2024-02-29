from typing import List
import aspose.words as aw
from pathlib import Path
import cv2
import requests
import os
import uuid


def detect_face(img_path):
    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_classifier = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = face_classifier.detectMultiScale(
        gray, scaleFactor=1.2, minNeighbors=5)
    return faces


def clear_images(images_path: str):
    img_count = 0
    for raw_image in os.listdir(images_path):
        raw_img = os.path.join(images_path, raw_image)
        if len(detect_face(raw_img)) != 1 or img_count > 1:
            os.remove(raw_img)
            continue
        img_count += 1


def make_md(raw_doc_url: str) -> str:
    r = requests.get(raw_doc_url, allow_redirects=True)
    uid = str(uuid.uuid4())
    raw_doc_path = '{id}.{format}'.format(id=uid, format=raw_doc_url.split('.')[-1])
    open(raw_doc_path, 'wb').write(r.content)
    doc = aw.Document(raw_doc_path)
    md_path = '{old_id}_1.md'.format(old_id=uid)
    doc.save(md_path)
    clear_images('./images')
    with open(md_path, 'r') as f:
        md_str = f.read()
    os.remove(md_path)
    return md_str



if __name__ == '__main__':
    print(make_md('https://docs.yandex.ru/docs/view?url=ya-disk-public%3A%2F%2F5J2ooKnHXKhxP743mXfP60AKql%2Fxs12BclB66uJE5nKxBkowQ3pKfNqNltj%2FgoNiq%2FJ6bpmRyOJonT3VoXnDag%3D%3D%3A%2FAlexey%20Melnichnikov.pdf&name=Alexey%20Melnichnikov.pdf&nosw=1'))

import aspose.words as aw
import cv2
import requests
import os
import uuid


def detect_face(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_classifier = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = face_classifier.detectMultiScale(
        gray, scaleFactor=1.15, minNeighbors=5)
    return faces


def get_face(img_path: str, resize_factor=1.5):
    var_img = cv2.imread(img_path)
    faces = detect_face(var_img)
    crop_image = None
    for i, (ex, ey, ew, eh) in enumerate(faces):

        new_ex = max(0, ex - int(ew * resize_factor / 2))
        new_ey = max(0, ey - int(eh * resize_factor / 2))
        new_ew = min(var_img.shape[1] - new_ex, int(ew * (1 + resize_factor)))
        new_eh = min(var_img.shape[0] - new_ey, int(eh * (1 + resize_factor)))

        crop_image = var_img[new_ey:new_ey+new_eh, new_ex:new_ex+new_ew]

        # cv2.imwrite('src/face.jpeg', crop_image)  # delete it
    return crop_image


def clear_images(images_path: str):
    img_count = 0
    for raw_image in os.listdir(images_path):
        if raw_image.endswith('.png') or raw_image.endswith('.jpeg') and raw_image != "face.jpeg":
            raw_img = os.path.join(images_path, raw_image)
            os.remove(raw_img)


async def make_md_and_img(raw_doc: str, is_url: bool = True):
    if is_url:
        r = requests.get(raw_doc, allow_redirects=True)
        uid = str(uuid.uuid4())
        raw_doc_path = '{id}.{format}'.format(
            id=uid, format=raw_doc.split('.')[-1])
        open(raw_doc_path, 'wb').write(r.content)
    else:
        raw_doc_path = raw_doc

    doc = aw.Document(raw_doc_path)

    uid = 'resume'
    md_path = 'src/{old_id}.md'.format(old_id=uid)
    img_path = 'src/{old_id}_main.png'.format(old_id=uid)

    doc.save(md_path)
    doc.save(img_path)

    img = get_face(img_path)

    clear_images("src")
    with open(md_path, 'r') as f:
        md_str = f.read()
    os.remove(md_path)

    if is_url:
        os.remove(raw_doc_path)

    if img is not None:
        file_path = 'temp.jpeg'
        cv2.imwrite(file_path, img)
        with open(file_path, "rb") as file:
            img = file.read()
        os.remove("temp.jpeg")

    return (md_str, img)

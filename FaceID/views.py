import shutil
from django.shortcuts import render
import time
import pickle
import os
import cv2
from PIL import Image
import numpy as np
from django import forms


# Create your views here.
class nameForm(forms.Form):
    name = forms.CharField()


def addName(request):
    if request.method == 'POST':
        form = nameForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            print(name)

    form = nameForm()
    return render(request, 'addName.html', {'form': form})


def about(request):
    if request.method == 'POST':
        form = nameForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            image_dir = os.path.join(BASE_DIR, "images")
            os.chdir(image_dir)
            if os.path.exists(name):
                return render(request, 'blog/about.html', {'form': form, 'data': 'Name already exists'})
            os.makedirs(name)
            os.chdir(name)
            if cam():
                return render(request, 'blog/camera.html')
            else:
                return render(request, 'blog/about.html', {'form': form, 'data': 'Unable to detect face'})

    form = nameForm()
    return render(request, 'blog/about.html', {'form': form})


def cam():
    face_cascade = cv2.CascadeClassifier(
        '/usr/local/lib/python3.7/dist-packages/cv2/data/haarcascade_frontalface_alt2.xml')
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    current_id = 0
    label_ids = {}
    y_labels = []
    x_train = []

    count = 1
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    timeout = time.time() + 25  # 10 seconds from now
    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
        for (x, y, w, h) in faces:
            img_item = str(count) + ".JPG"
            count += 1
            cv2.imwrite(img_item, gray)
        # cv2.imshow('frame', frame)
        if count > 5:
            break
        if time.time() > timeout:
            #shutil.rmtree(os.getcwd(), ignore_errors=False, onerror=None)   THIS LINE CAN DELETED THE WHOLE PROJECT
            return False
    ###############################################################################################################
    # Once pictures are taken, go back to base directory and train the machine to recognize the images
    ###############################################################################################################
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    image_dir = os.path.join(BASE_DIR, "images")
    os.chdir(BASE_DIR)

    for root, dirs, files in os.walk(image_dir):
        for file in files:
            if file.endswith("png") or file.endswith("JPG"):
                path = os.path.join(root, file)
                label = os.path.basename(root)
                if label not in label_ids:
                    label_ids[label] = current_id
                    current_id += 1

                id_ = label_ids[label]

                pil_image = Image.open(path).convert("L")  # converts to grayscale
                image_array = np.array(pil_image, "uint8")
                faces = face_cascade.detectMultiScale(image_array, scaleFactor=1.5, minNeighbors=5)

                for (x, y, w, h) in faces:
                    roi = image_array[y:y + h, x:x + w]
                    img_item = "my-image.png"
                    x_train.append(roi)
                    y_labels.append(id_)

    ###############################################################################################################
    # The training data is saved in trainer.yml and labels.pickle is to label each person
    ###############################################################################################################
    with open("labels.pickle", 'wb') as f:
        pickle.dump(label_ids, f)

    recognizer.train(x_train, np.array(y_labels))
    recognizer.save("trainer.yml")
    return True


def recognize(request):
    face_cascade = cv2.CascadeClassifier(
        '/usr/local/lib/python3.7/dist-packages/cv2/data/haarcascade_frontalface_alt2.xml')
    if not os.path.exists("/home/pi/Desktop/django_project/blog/trainer.yml"):
        return render(request, 'blog/recognize.html', {'empty': 'No accounts created'})

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("/home/pi/Desktop/django_project/blog/trainer.yml")

    with open("/home/pi/Desktop/django_project/blog/labels.pickle", 'rb') as f:
        og_labels = pickle.load(f)
        labels = {v: k for k, v in og_labels.items()}

    cap = cv2.VideoCapture(0)

    def make_480p():
        cap.set(3, 640)
        cap.set(4, 480)

    make_480p()

    timeout = time.time() + 30  # 15 seconds from now
    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
        for (x, y, w, h) in faces:
            roi_gray = gray[y:y + h, x:x + w]
            id_, conf = recognizer.predict(roi_gray)
            if 45 <= conf <= 85:
                font = cv2.FONT_HERSHEY_SIMPLEX
                name = labels[id_]
                color = (255, 255, 255)
                stroke = 2
                cv2.putText(frame, name, (x, y), font, 1, color, stroke, cv2.LINE_AA)
                return render(request, 'blog/recognize.html', {'data': name})

            # color = (255, 0, 0)  # BGR
            # stroke = 2
            # cv2.rectangle(frame, (x, y), (w + x, h + y), color, stroke)

        # cv2.imshow('frame', frame)
        if time.time() > timeout:
            return render(request, 'blog/recognize.html', {'data': 'Timed out'})

    return render(request, 'blog/recognize.html', {'data': 'Unable to recognize'})

from django.shortcuts import render, redirect
import time
import pickle
import os
import cv2
from PIL import Image
import numpy as np
from my_project.settings import MEDIA_ROOT
from users import models
from users.models import Profile, FcPic


def setupFaceID(request):
    if request.method == 'POST':
        p = Profile.objects.get(user=request.user)
        id = str(request.user.id)
        image_dir = os.path.join(MEDIA_ROOT, "face_images")
        os.chdir(image_dir)
        if not os.path.exists(id):
            os.makedirs(id)
        os.chdir(id)
        p.fc = False
        p.save()
        count = 0
        if 'retake' in request.POST:
            count = cam(request, True)

        elif 'start' in request.POST:
            count = cam(request, False)

        elif 'finish' in request.POST:
            learn()
            return redirect('success')

        if count is None:
            return render(request, 'FaceID/setup.html', {'message': 'No camera detected'})
        elif count >= 10:  # timed out
            pictures = FcPic.objects.filter(profile=p)
            context = {
                'pics': pictures,
                'message': 'Progress: ' + str(
                    ((count - 11) / 5) * 100) + '%',
                'progress': ((count - 11) / 5) * 100,
                'timeout': 'Timed out, press continue to try again'
            }
            return render(request, 'FaceID/setup.html', context)
        elif count > 5:
            pictures = FcPic.objects.filter(profile=p)
            context = {
                'finished': True,
                'pics': pictures,
                'message': 'Progress: ' + str(
                    ((count - 1) / 5) * 100) + '%',
                'progress': ((count - 1) / 5) * 100
            }
            return render(request, 'FaceID/setup.html', context)
        elif count > 0:
            pictures = FcPic.objects.filter(profile=p)
            context = {
                'pics': pictures,
                'message': 'Progress: ' + str(
                    ((count - 1) / 5) * 100) + '%',
                'progress': ((count - 1) / 5) * 100
            }
            return render(request, 'FaceID/setup.html', context)
        else:
            return render(request, 'FaceID/setup.html', {'message': 'One face at a time please.'})
    return render(request, 'FaceID/setup.html')


def setupSuccess(request):
    p = Profile.objects.get(user=request.user)
    p.fc_setup = True
    p.fc = True
    p.save()
    pictures = FcPic.objects.filter(profile=p)
    context = {
        'pics': pictures
    }
    return render(request, 'users/FaceIDsetupSuccess.html', context)


def cam(request, retake):
    face_cascade = cv2.CascadeClassifier(
        '/Users/benjaminchen/Desktop/my_project/venv/lib/python3.8/site-packages/cv2/data/haarcascade_frontalface_alt2.xml'
        #'/usr/local/lib/python3.7/dist-packages/cv2/data/haarcascade_frontalface_alt2.xml'
    )
    count = 1
    for path in os.listdir('.'):
        count += 1
    if count > 5 and not retake:
        return count
    cap = cv2.VideoCapture(0)
    if cap is None or not cap.isOpened():
        return None
    cap.set(3, 640)
    cap.set(4, 480)
    timeout = time.time() + 15  # 10 seconds from now
    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=3)
        if len(faces) > 1:
            return -1
        for (x, y, w, h) in faces:
            img_item = 'face_images/' + str(request.user.id) + '/' + str(count) + ".JPG"
            if retake:
                count -= 1
            fileName = str(count) + ".JPG"
            count += 1
            cv2.imwrite(fileName, frame)
            if not retake:
                user = models.Profile.objects.get(user=request.user)
                obj = models.FcPic.objects.create(profile=user, pic=img_item)
                obj.save()
            return count
        # cv2.imshow('frame', frame)
        if time.time() > timeout:
            return count + 10


def learn():
    face_cascade = cv2.CascadeClassifier(
        '/Users/benjaminchen/Desktop/my_project/venv/lib/python3.8/site-packages/cv2/data/haarcascade_frontalface_alt2.xml'
        #'/usr/local/lib/python3.7/dist-packages/cv2/data/haarcascade_frontalface_alt2.xml'
    )
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    current_id = 0
    label_ids = {}
    y_labels = []
    x_train = []

    BASE_DIR = MEDIA_ROOT
    image_dir = os.path.join(BASE_DIR, "face_images")
    os.chdir(BASE_DIR)

    for root, dirs, files in os.walk(image_dir):
        for file in files:
            if file.endswith("png") or file.endswith("JPG"):
                path = os.path.join(root, file)
                label = os.path.basename(root)
                if label not in label_ids:
                    label_ids[label] = current_id
                    current_id += 1
                    print(current_id)

                id_ = label_ids[label]

                pil_image = Image.open(path).convert("L")  # converts to grayscale
                image_array = np.array(pil_image, "uint8")
                faces = face_cascade.detectMultiScale(image_array)

                for (x, y, w, h) in faces:
                    roi = image_array[y:y + h, x:x + w]
                    x_train.append(roi)
                    y_labels.append(id_)

    ###############################################################################################################
    # The training data is saved in trainer.yml and labels.pickle is to label each person
    ###############################################################################################################
    with open("labels.pickle", 'wb') as f:
        pickle.dump(label_ids, f)

    recognizer.train(x_train, np.array(y_labels))
    recognizer.save("trainer.yml")
    return

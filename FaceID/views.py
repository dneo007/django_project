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
    if request.method == 'POST' and 'start' in request.POST:
        p = Profile.objects.get(user=request.user)
        id = str(request.user.id)
        image_dir = os.path.join(MEDIA_ROOT, "face_images")
        os.chdir(image_dir)
        if not os.path.exists(id):
            os.makedirs(id)
        os.chdir(id)
        count = cam(request)
        p.fc = False
        p.save()
        if count is None:
            return render(request, 'FaceID/setup.html', {'message': 'No camera detected'})
        elif count >= 5:
            return redirect('success')
        elif count > 0:

            return render(request, 'FaceID/setup.html', {'message':'We are having difficulties detecting your face, press to continue. Progress: '+str(((count-1)/5)*100) + '%'})
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


def cam(request):
    face_cascade = cv2.CascadeClassifier(
        '/usr/local/lib/python3.7/dist-packages/cv2/data/haarcascade_frontalface_alt2.xml')
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    current_id = 0
    label_ids = {}
    y_labels = []
    x_train = []
    count = 1
    for path in os.listdir('.'):
        count += 1
    print(count)
    if count > 5:
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
            fileName = str(count) + ".JPG"
            count += 1
            cv2.imwrite(fileName, gray)
            user = models.Profile.objects.get(user=request.user)
            user.fc_pic = img_item
            user.save()

            obj = models.FcPic.objects.create(profile=user, pic=img_item)
            obj.save()
        # cv2.imshow('frame', frame)
        if count > 5:
            break
        if time.time() > timeout:
            return count
    ###############################################################################################################
    # Once pictures are taken, go back to base directory and train the machine to recognize the images
    ###############################################################################################################


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

                id_ = label_ids[label]

                pil_image = Image.open(path).convert("L")  # converts to grayscale
                image_array = np.array(pil_image, "uint8")
                faces = face_cascade.detectMultiScale(image_array, scaleFactor=1.5, minNeighbors=5)

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
    return 6

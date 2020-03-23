import os
import pickle
import time

import cv2
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, FacialRecForm
from .models import Profile


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(username=username, password=raw_password)
            login(request, account)
            if form.cleaned_data['fc']:
                return redirect('setup')

            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('profile')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    checked = Profile.objects.get(user=request.user).fc
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        f_form = FacialRecForm(request.POST, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            f_form.save()
            messages.success(request, f'Your account has been updated!')

            if Profile.objects.get(user=request.user).fc and not Profile.objects.get(user=request.user).fc_setup:
                return redirect('setup')

            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        f_form = FacialRecForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'f_form': f_form,
        'checked': checked,
    }

    return render(request, 'users/profile.html', context)


def setupSuccess(request):
    p = Profile.objects.get(user=request.user)
    p.fc_setup = True
    p.save()
    return render(request, 'users/FaceIDsetupSuccess.html')


def faceIDLogin(request):
    if request.method == 'POST' and 'start' in request.POST:
        user = recognize()
        if user is not None:
            return render(request, 'users/FaceIDLogin.html', {'message': 'welcome' + user})
        elif user == -1:
            return render(request, 'users/FaceIDLogin.html', {'message': 'Not receiving images, please ensure your '
                                                                         'camera is working.'})
        else:
            return render(request, 'users/FaceIDLogin.html', {'message': 'We are having difficulties detecting your '
                                                                         'face, press to try again.'})

    return render(request, 'users/FaceIDLogin.html')


def recognize():
    face_cascade = cv2.CascadeClassifier(
        '/usr/local/lib/python3.7/dist-packages/cv2/data/haarcascade_frontalface_alt2.xml')
    if not os.path.exists("/home/pi/Desktop/django_project/FaceID/trainer.yml"):
        return None

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("/home/pi/Desktop/django_project/FaceID/trainer.yml")

    with open("/home/pi/Desktop/django_project/FaceID/labels.pickle", 'rb') as f:
        og_labels = pickle.load(f)
        labels = {v: k for k, v in og_labels.items()}

    cap = cv2.VideoCapture(0)

    def make_480p():
        cap.set(3, 640)
        cap.set(4, 480)

    make_480p()

    timeout = time.time() + 20  # 20 seconds from now
    while True:
        ret, frame = cap.read()
        if frame is not None:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=3)
            for (x, y, w, h) in faces:
                roi_gray = gray[y:y + h, x:x + w]
                id_, conf = recognizer.predict(roi_gray)
                if 45 <= conf <= 85:
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    name = labels[id_]
                    color = (255, 255, 255)
                    stroke = 2
                    cv2.putText(frame, name, (x, y), font, 1, color, stroke, cv2.LINE_AA)
                    return name

                # color = (255, 0, 0)  # BGR
                # stroke = 2
                # cv2.rectangle(frame, (x, y), (w + x, h + y), color, stroke)

            # cv2.imshow('frame', frame)

        else:
            print("no")
            return -1

        if time.time() > timeout:
            return None
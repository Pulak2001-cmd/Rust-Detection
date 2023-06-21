from django.shortcuts import render, HttpResponse
from .models import Images
# Create your views here.
import tensorflow as tf
import numpy as np
import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
# from ultralytics import YOLO

def index(request):
    if request.method == 'POST':
        print(BASE_DIR)
        folder = str(BASE_DIR) + '/media'
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
        file2 = request.FILES["file"]
        print(file2)
        document = Images.objects.create(img=file2)
        document.save()
        print("File")
        print(request.FILES['file'])
        img_path = str(BASE_DIR) + "/media/" + str(file2)
        # img_path='split/validation/CORROSION/photo-1531431221349-4a0b92bb795b.jpg'
        img = tf.keras.utils.load_img(img_path, target_size = (128, 128))
        img = tf.keras.utils.img_to_array(img)
        img = np.expand_dims(img, axis = 0)
        model = tf.keras.models.load_model(str(BASE_DIR)+'/app/model.h5')
        print(model)
        pred_value = model.predict(img)[0][0]
        print("Prediction value")
        print(pred_value)
        if pred_value < 0.5:
            status = "Corrotion"
        else:
            status = "No corrotion"
        context = {
            'link': request.FILES['file'],
            'status': status
        }
        return render(request, 'result.html', context=context)
    return render(request, 'index.html')

def folder(request):
    if request.method == 'POST':
        files = request.FILES.getlist('multifile')
        print(files)
        model = tf.keras.models.load_model(str(BASE_DIR)+'/app/model.h5')
        rust = []
        values = []
        folder = str(BASE_DIR) + '/media'
        for file in files:
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                print(filename)
                print(values)
                if filename in values:
                    continue
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    print('Failed to delete %s. Reason: %s' % (file_path, e))
            document = Images.objects.create(img=file)
            document.save()
            img_path = str(BASE_DIR) + "/media/" + str(file)
            img = tf.keras.utils.load_img(img_path, target_size = (128, 128))
            img = tf.keras.utils.img_to_array(img)
            img = np.expand_dims(img, axis = 0)
            pred_value = model.predict(img)[0][0]
            if pred_value < 0.5:
                rust.append(file)
                values.append(str(file))
        context = {
            'rust': rust,
        }
        print(rust)
        return render(request, 'folder.html', context=context)

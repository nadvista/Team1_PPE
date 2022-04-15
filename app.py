from importlib.resources import path
import os
import shutil
from flask import Flask, flash, request, redirect, url_for, render_template, after_this_request
from werkzeug.utils import secure_filename
from yaml import load
import Yolov5_DeepSort_Pytorch.track
from threading import Thread 
import threading


app = Flask(__name__)

# папка для сохранения загруженных файлов
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# th = Thread(target=Yolov5_DeepSort_Pytorch.track.start, args=(filepath, )) # Запускаем разметку видео
# th.start()

@app.route('/', methods=['POST'])
def upload_file_POST():
    loading_flag = False
    ###########################################################################
    # Удаляет все папки чтобы запущенный ран сохранился 
    # в Yolov5_DeepSort_Pytorch\runs\track\weights\best_osnet_ibn_x1_0_MSMT17
    delete_folder = 'Yolov5_DeepSort_Pytorch/runs/track/weights/'
    delete_folders = os.listdir(delete_folder)
    for g in delete_folders:
        print("Delete: ", g)
        shutil.rmtree(delete_folder + g)
    ###########################################################################
    # Сохраняет файл
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    filename = secure_filename(file.filename)
    filepath = f"{app.config['UPLOAD_FOLDER']}/{filename}"
    file.save(filepath)
    ###########################################################################
    return redirect(url_for('loading', file = filename))


@app.route('/', methods=['GET'])
def upload_file_GET():
    return render_template('index.html')


@app.route('/load/<file>', methods=['GET', 'POST'])
def loading(file):
    # @after_this_request
    # def after_request(responce):
    #     # Запускает Треккинг видео
    #     # Переносим файл в static
    #     return responce
    return render_template('loading.html')


@app.route('/download/<file>', methods=['GET', 'POST'])
def download(file):
    ###########################################################################
    # Переносим размеченный файл 
    try:
        file_source = 'Yolov5_DeepSort_Pytorch/runs/track/weights/best_osnet_ibn_x1_0_MSMT17/'
        file_destination = 'static'
        get_files = os.listdir(file_source)    
        for g in get_files:
            shutil.move(file_source + g, file_destination)
    except:
        print("File already exists")
    ###########################################################################
    # И удаляем папку откуда взяли файл
    try:
        delete_folder = 'Yolov5_DeepSort_Pytorch/runs/track/weights/'
        delete_folders = os.listdir(delete_folder)
        for g in delete_folders:
            print("Delete: ", g)
            shutil.rmtree(delete_folder + g)
    except:
        print("Failed Delete")
    ###########################################################################
    return render_template('videoplayer.html', filename=file)


if __name__ == "__main__":
    app.run(debug=True)

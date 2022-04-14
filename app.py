from importlib.resources import path
import os
import shutil
from flask import Flask, flash, request, redirect, url_for, render_template, after_this_request         
# объясняется ниже
from werkzeug.utils import secure_filename
from yaml import load
import Yolov5_DeepSort_Pytorch.track
from threading import Thread 
import threading


# папка для сохранения загруженных файлов
UPLOAD_FOLDER = 'uploads/'
# расширения файлов, которые разрешено загружать
# создаем экземпляр приложения
app = Flask(__name__, static_folder='static')

# конфигурируем
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['POST'])
def upload_file_POST():
    # Удаляет папки чтобы все запущенный ран сохранился 
    # в Yolov5_DeepSort_Pytorch\runs\track\weights\best_osnet_ibn_x1_0_MSMT17
    delete_folder = 'Yolov5_DeepSort_Pytorch/runs/track/weights/'
    delete_folders = os.listdir(delete_folder)
    for g in delete_folders:
        print("Delete: ", g)
        shutil.rmtree(delete_folder + g)

    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)
    filename = secure_filename(file.filename)
    filepath = f"{app.config['UPLOAD_FOLDER']}/{filename}"
    file.save(filepath)
    return redirect(url_for('loading', file = filename))

@app.route('/', methods=['GET'])
def upload_file_GET():
    return render_template('index.html')


@app.route('/load?<file>', methods=['GET', 'POST'])
def loading(file):
    # @after_this_request
    # def after_request(responce):
    #     th.start()
    #     return responce
    
    filepath = f"{app.config['UPLOAD_FOLDER']}/{file}"
    th = Thread(target=Yolov5_DeepSort_Pytorch.track.start, args=(filepath, ))
    # Запускает Треккинг видео
    th.start()
    th.join()
    # Переносим файл в static
    file_source = 'Yolov5_DeepSort_Pytorch/runs/track/weights/best_osnet_ibn_x1_0_MSMT17/'
    file_destination = 'static'
    get_files = os.listdir(file_source)
    try:
        for g in get_files:
            shutil.move(file_source + g, file_destination)
    except:
        print("File already exists")
    # И удаляем папку откуда взяли файл
    delete_folder = 'Yolov5_DeepSort_Pytorch/runs/track/weights/'
    delete_folders = os.listdir(delete_folder)
    for g in delete_folders:
        print("Delete: ", g)
        shutil.rmtree(delete_folder + g)
        
    return redirect(url_for('download', file = file))

    # return render_template('loading.html')
    # print(threading.active_count())
    # print(th)
    # threading.active_count()
    # if th.is_alive():
    #     return render_template('loading.html')
    # else:
    #     print("Thread is dead")
    return redirect(url_for('download/<file>',file = file))

@app.route('/download?<file>', methods=['GET', 'POST'])
def download(file):
    return render_template('videoplayer.html', filename=file)


def conv():
    yield redirect('/loading')
    yield redirect('/download')

if __name__ == "__main__":
    app.run(debug=True)
    
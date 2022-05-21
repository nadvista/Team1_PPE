import os
import shutil
from flask import Flask, request, redirect, url_for, render_template, Response
from werkzeug.utils import secure_filename
from Yolov5_DeepSort_Pytorch.track import start
import Yolov5_DeepSort_Pytorch.track
from threading import Thread
import threading
import database
import time
# import sys
# _PATH = 'C:\msys64\mingw64\bin'
# sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + _PATH)

# import gi


app = Flask(__name__)

# папка для сохранения загруженных файлов
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

conn_data = (5432, 'localhost', 'ppe_db', 'SyW8ZzaNJiKMx2y', 'postgres')
db = database.Database(conn_data)


@app.route('/', methods=['POST'])
def upload_file_POST():
    loading_flag = False
    ###########################################################################
    # Удаляет все папки чтобы запущенный ран сохранился 
    # в Yolov5_DeepSort_Pytorch\runs\track\weights\best_osnet_ibn_x1_0_MSMT17
    try:
        delete_folder = 'Yolov5_DeepSort_Pytorch/runs/track/weights/'
        delete_folders = os.listdir(delete_folder)
        for g in delete_folders:
            print("Delete: ", g)
            shutil.rmtree(delete_folder + g)
    except:
        pass
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
    print('upl')
    return render_template('index.html')

"""
####################
# YIELDS
def step_loads(file):
    yield render_template('loading.html')
    filepath = f"{app.config['UPLOAD_FOLDER']}/{file}"
    th = Thread(target=Yolov5_DeepSort_Pytorch.track.start, args=(filepath, )) # Запускаем разметку видео
    th.start()
    th.join()
    yield redirect(url_for('download', file = file))
    
return Response(step_loads(file)) # Добавить в loading
"""
@app.route('/load/<file>', methods=['GET', 'POST'])
def loading(file):
    # @after_this_request
    # def after_request(responce):
    #     # Запускает Треккинг видео
    #     # Переносим файл в static
    #     return responce
    print('load')
    return redirect(url_for('download', file = file))
    # return render_template('loading.html')


@app.route('/download/<file>', methods=['GET', 'POST'])
def download(file):
    filepath = f"{app.config['UPLOAD_FOLDER']}/{file}"
    data = start(filepath)
    data = db._process_data(data)
    print(data)
    print(round(time.time()))
    db.push(data, str(round(time.time())))
    ###########################################################################
    # Переносим размеченный файл 
    try:
        file_source = 'Yolov5_DeepSort_Pytorch/runs/track/weights/best_osnet_ibn_x1_0_MSMT17/'
        file_destination = 'static'
        get_files = os.listdir(file_source)    
        for g in get_files:
            shutil.move(file_source + g, file_destination)
            print(g, "Transfered by", file_destination, "And rdy for using")
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
    # # Gstreamer here :))))))))    
    # # Это, если вы используете deepsort в файле object_tracker.py
    # # Советую изучить как строить пайплайны в gstreamer и впринципе все эти теги для пайплайна
    # # pipe_out как раз является пайплайном
    # pipe_out = 'appsrc ! videoconvert ! x264enc tune=zerolatency bitrate=700 speed-preset=superfast ! decodebin ! autovideoconvert ! theoraenc ! oggmux ! tcpserversink host=127.0.0.1 port=8080'


    # try:
    #     vid = cv2.VideoCapture("filesrc location=./data/video/hype.mp4 ! decodebin ! videoconvert ! appsink", cv2.CAP_GSTREAMER)
    # except Exception as e:
    #     print(e)

    # out = cv2.VideoWriter(pipe_out, 0, 30, (int(vid.get(cv2.CAP_PROP_FRAME_WIDTH)), int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))), True)

    # # Всё запускается из файла server.py:
    # # Но только фронт у нас в отдельном докер контейнере лежит
    # from absl import app
    # import object_tracker as object_tracker

    # object_tracker.set_flags()

    # app.run(object_tracker.main)
    ###########################################################################
    return render_template('videoplayer.html', filename=file)


if __name__ == "__main__":
    app.run(debug=True)

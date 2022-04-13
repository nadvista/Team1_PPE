import os
from flask import Flask, flash, request, redirect, url_for, render_template, after_this_request         
# объясняется ниже
from werkzeug.utils import secure_filename
from yaml import load
import Yolov5_DeepSort_Pytorch.track
from threading import Thread

# папка для сохранения загруженных файлов
UPLOAD_FOLDER = 'uploads/'
# расширения файлов, которые разрешено загружать
# создаем экземпляр приложения
app = Flask(__name__)
# конфигурируем
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['POST'])
def upload_file_POST():
        
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)
    filename = secure_filename(file.filename)
    filepath = f"{app.config['UPLOAD_FOLDER']}/{filename}"
    file.save(filepath)
    return redirect(url_for('loading',file = filename))

@app.route('/', methods=['GET'])
def upload_file_GET():
    return render_template('index.html')

@app.route('/load/<file>', methods=['GET', 'POST'])
def loading(file):
    @after_this_request
    def after_request(responce):
        filepath = f"{app.config['UPLOAD_FOLDER']}/{file}"
        th = Thread(target=Yolov5_DeepSort_Pytorch.track.start, args=(filepath, ))
        th.start()
        return responce
    return render_template('loading.html')

@app.route('/download', methods=['GET', 'POST'])
def download():
    return render_template('videoplayer.html')


def conv():
    yield redirect('/loading')
    yield redirect('/download')

if __name__ == "__main__":
    app.run()
    
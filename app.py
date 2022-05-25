from concurrent.futures import thread
import os
import shutil
from flask import Flask, flash, request, redirect, url_for, render_template, Response
from matplotlib.pyplot import get
from werkzeug.utils import secure_filename
from Yolov5_DeepSort_Pytorch.track import start
import Yolov5_DeepSort_Pytorch.track
from turbo_flask import Turbo
from threading import Thread
import time
import database



app = Flask(__name__)
turbo = Turbo(app)

# Папка для сохранения загруженных файлов
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# conn_data = (5432, 'localhost', 'ppe_db', 'SyW8ZzaNJiKMx2y', 'postgres')
# db = database.Database(conn_data)



@app.route('/', methods=['GET'])
def upload_file_GET():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def upload_file_POST():

    ###########################################################################
    # Удаляет все папки чтобы запущенный ран сохранился в 
    # Yolov5_DeepSort_Pytorch\runs\track\weights\best_osnet_ibn_x1_0_MSMT17
    delete_folder = './Yolov5_DeepSort_Pytorch/runs/track/weights/'
    delete_folders = os.listdir(delete_folder)
    for g in delete_folders:
        try:
            shutil.rmtree(delete_folder + g)
            print(f'[INFO] "{g}" from "{delete_folder}" was deleted!')
        except:
            pass

    ###########################################################################
    # Сохраняет файл в UPLOAD_FOLDER
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    filepath = f"{app.config['UPLOAD_FOLDER']}/tempfile.mp4"
    file.save(filepath)

    ###########################################################################
    return redirect(url_for('loading'))


@app.route('/load/', methods=['GET', 'POST'])
def loading():
    filepath = f"{app.config['UPLOAD_FOLDER']}/tempfile.mp4"
    with app.app_context():
        turbo.push(turbo.replace(render_template('loading.html'), 'content'))

    data = start(filepath)
    # data = db._process_data(data)
    # print(data)
    # print(round(time.time()))
    # db.push(data, str(round(time.time())))
    
    return redirect(url_for('download'))


@app.route('/download/', methods=['GET', 'POST'])
def download():
    filepath = f"{app.config['UPLOAD_FOLDER']}/tempfile.mp4"


    ###########################################################################
    # Данный кусок кода удаляет загруженный исходный файл из /uploads
    try:
        delete_files = os.listdir('./' + UPLOAD_FOLDER)
        for n in delete_files:
            os.remove('./' + UPLOAD_FOLDER + n)
            print(f'[INFO] Source file "{n}" from "{UPLOAD_FOLDER}" was deleted.')
    except:
        print("[O-ops!] Failed to delete source file.")

    ###########################################################################
    # Переносим размеченный файл в /static
    try:
        file_source = './Yolov5_DeepSort_Pytorch/runs/track/weights/best_osnet_ibn_x1_0_MSMT17/'
        file_destination = './static/'
        get_files = os.listdir(file_source)    
        for g in get_files:
            shutil.move(file_source + g, file_destination)
            print(f'[INFO] {g} from "{file_source}" transfered by "{file_destination}" and ready for using!')
    except:
        print("[O-ops!] Output file already exists.")

    ###########################################################################
    # И удаляем папку откуда взяли размеченный файл
    try:
        delete_folder = 'Yolov5_DeepSort_Pytorch/runs/track/weights/'
        delete_files = os.listdir(delete_folder)
        for n in delete_files:
            print(f'[INFO] Folder "{n}" was deleted from "{delete_folder}".')
            shutil.rmtree(delete_folder + n)
    except:
        print("[O-ops!] Failed delete.")

    ###########################################################################
    # FFmpeg here  

    DATA_FOLDER = './video_streaming'
    PATH_TO_INPUT_FILE = './static'

    command = (
    f'ffmpeg -re -i {PATH_TO_INPUT_FILE}/tempfile.mp4 -map 0 -map 0 -c:a \
        aac -c:v libx264 -b:v:0 800k -b:v:1 \
        300k -s:v:1 320x170 -profile:v:1 baseline \
        -profile:v:0 main -bf 1 -keyint_min 120 -g 120 \
        -sc_threshold 0 -b_strategy 0 -ar:a:1 22050 \
        -use_timeline 1 -use_template 1 -window_size 5 \
        -adaptation_sets "id=0,streams=v id=1,streams=a" \
        -f dash {DATA_FOLDER}/output_manifest.mpd'
    )

    os.system(command)

    ###########################################################################
    return render_template('videoplayer.html', filename='static/tempfile.mp4')


if __name__ == "__main__":
    app.run(debug=True,  port=5000)

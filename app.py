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

    TEMP_FOLDER = './metadata'
    PATH_TO_INPUT_FILE = './static'

    command = (
    f'ffmpeg -hide_banner -y -i {PATH_TO_INPUT_FILE}/tempfile.mp4 \
       -r 30 -c:v libx264 -pix_fmt yuv420p -preset veryfast -profile:v main \
       -keyint_min 250 -g 250 -sc_threshold 0 \
       -c:a aac -b:a 128k -ac 2 -ar 48000 \
       -map v:0 -filter:v:0 "scale=-2:360"  -b:v:0 800k  -maxrate:0 856k  -bufsize:0 1200k \
       -map v:0 -filter:v:1 "scale=-2:432"  -b:v:1 1400k -maxrate:1 1498k -bufsize:1 2100k \
       -map v:0 -filter:v:2 "scale=-2:540"  -b:v:2 2000k -maxrate:2 2140k -bufsize:2 3500k \
       -map v:0 -filter:v:3 "scale=-2:720"  -b:v:3 2800k -maxrate:3 2996k -bufsize:3 4200k \
       -map v:0 -filter:v:4 "scale=-2:1080" -b:v:4 5000k -maxrate:4 5350k -bufsize:4 7500k \
       -map 0:a? \
       -init_seg_name "{TEMP_FOLDER}/init-\$RepresentationID\$.\$ext\$" \
       -media_seg_name "{TEMP_FOLDER}/chunk-\$RepresentationID\$-\$Number%05d\$.\$ext\$" \
       -dash_segment_type mp4 \
       -use_template 1 \
       -use_timeline 0 \
       -seg_duration 10 \
       -adaptation_sets "id=0,streams=v id=1,streams=a" \
       -f dash \
       dash.mpd'
    )

    os.system(command)

    ###########################################################################
    return render_template('videoplayer.html', filename='static/tempfile.mp4')


if __name__ == "__main__":
    app.run(debug=True,  port=5000)

import os
import shutil
from time import sleep
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import Yolov5_DeepSort_Pytorch.track
from turbo_flask import Turbo
from threading import Thread
import gi
gi.require_version("Gst", "1.0")
from gi.repository import Gst, GLib

app = Flask(__name__)
turbo = Turbo(app)


# папка для сохранения загруженных файлов
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['POST'])
def upload_file_POST():
    print(gi.__version__)
    ###########################################################################
    # Очищаем папку с размеченными видео
    if os.path.isfile('/output/tempfile.mp4'): 
        os.remove('/output/tempfile.mp4') 
        print("success") 
    else: 
        print("File doesn't exists!")
    ###########################################################################
    # Сохраняет файл
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    filename = secure_filename(file.filename)
    filepath = f"{app.config['UPLOAD_FOLDER']}/tempfile.mp4"
    file.save(filepath)
    ###########################################################################
    return redirect(url_for('loading',file=filename))

@app.route('/', methods=['GET'])
def upload_file_GET():
    return render_template('index.html')

@app.route('/load/', methods=['GET', 'POST'])
def loading():
    filepath = f"{app.config['UPLOAD_FOLDER']}/tempfile.mp4"
    with app.app_context():
        turbo.push(turbo.replace(render_template('loading.html'), 'content'))
    print(filepath, " Now working################################################################")
    Yolov5_DeepSort_Pytorch.track.start(filepath)
    return redirect(url_for('download'))


@app.route('/download/', methods=['GET', 'POST'])
def download():
    filepath = f"{app.config['UPLOAD_FOLDER']}/tempfile.mp4"
    ###########################################################################
    # Переносим размеченный файл 
    try:
        file_source = 'Yolov5_DeepSort_Pytorch/runs/track/weights/best_osnet_ibn_x1_0_MSMT17/'
        file_destination = 'output'
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
    Gst.init()

    main_loop = GLib.MainLoop()
    thread = Thread(target=main_loop.run)
    thread.start()
    pipeline = Gst.parse_launch("filesrc location=./output/tempfile.mp4 ! decodebin ! autovideoconvert ! autovideosink")
    pipeline.set_state(Gst.State.PLAYING)
    # try:
    #     while True:
    #         sleep(0.1)
    # except KeyboardInterrupt:
    #     pass
    # pipeline.set_state(Gst.State.NULL)
    # main_loop.quit()
    # pipe_out = 'appsrc ! videoconvert ! x264enc tune=zerolatency bitrate=700 speed-preset=superfast ! decodebin ! autovideoconvert ! theoraenc ! oggmux ! tcpserversink host=127.0.0.1 port=8080'
    # pipe_out = 'filesrc location=static/tempfile.mp4 ! videoconvert ! x264enc tune=zerolatency bitrate=700 speed-preset=superfast ! decodebin ! autovideoconvert ! theoraenc ! oggmux ! tcpserversink host=127.0.0.1 port=5000'
    # pipeline = Gst.parse_launch("filesrc location=./static/tempfile.mp4 ! videoconvert ! x264enc tune=zerolatency bitrate=700 speed-preset=superfast ! decodebin ! autovideoconvert ! theoraenc ! oggmux ! filesink location=./output.mp4")
    # pipeline = Gst.parse_launch(pipe_out)
    # pipeline.set_state(Gst.State.PLAYING)
    ###########################################################################
    return render_template('videoplayer.html', filename='static/tempfile.mp4')


if __name__ == "__main__":
    app.run(debug=True)

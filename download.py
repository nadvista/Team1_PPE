import os
from threading import Thread
from flask import Blueprint, send_file, render_template, current_app
# Среда разаработки выделяет все связанное с gstreamer предупреждениями
# Однако все работает
import gi
gi.require_version("Gst", "1.0")
from gi.repository import Gst, GLib

download_bp = Blueprint('download', __name__,
                        template_folder='templates')

@download_bp.route('/downloadvideo/')
def download_video():
    path = os.path.join(current_app.root_path,
                        current_app.config['DOWNLOAD_FOLDER'], "tempfile.mp4")
    return send_file(path, as_attachment=True)


@download_bp.route('/downloaddb/')
def download_db():
    path = os.path.join(current_app.root_path,
                        current_app.config['DOWNLOAD_FOLDER'], os.curdir + '/static/data.txt')
    return send_file(path, as_attachment=True)

@download_bp.route('/download/')
def download_page():
    ###########################################################################
    # # Gstreamer here :))))))))
    Gst.init()
    main_loop = GLib.MainLoop()
    thread = Thread(target=main_loop.run)
    thread.start()
    pipeline = Gst.parse_launch("filesrc location=./static/tempfile.mp4 ! decodebin ! autovideoconvert ! autovideosink")
    pipeline.set_state(Gst.State.PLAYING)
    ###########################################################################
    return render_template('videoplayer.html', filename=f"{current_app.config['DOWNLOAD_FOLDER']}/tempfile.mp4")

from threading import Thread
from time import sleep

import gi

gi.require_version("Gst", "1.0")

from gi.repository import Gst, GLib


Gst.init()

main_loop = GLib.MainLoop()
thread = Thread(target=main_loop.run)
thread.start()
pipeline = Gst.parse_launch("filesrc location=./output/tempfile.mp4 ! decodebin ! autovideoconvert ! autovideosink")
pipeline.set_state(Gst.State.PLAYING)
try:
    while True:
        sleep(0.1)
except KeyboardInterrupt:
    pass

pipeline.set_state(Gst.State.NULL)
main_loop.quit()

# pipeline = Gst.parse_launch("filesrc location=./static/tempfile.mp4 ! videoconvert ! x264enc tune=zerolatency bitrate=700 speed-preset=superfast ! decodebin ! autovideoconvert ! theoraenc ! oggmux ! tcpserversink host=127.0.0.1 port=8080")
# pipe_out = 'appsrc ! videoconvert ! x264enc tune=zerolatency bitrate=700 speed-preset=superfast ! decodebin ! autovideoconvert ! theoraenc ! oggmux ! tcpserversink host=127.0.0.1 port=8080'
# pipeline = Gst.parse_launch("audiotestsrc wave=saw freq=205 volume=0.1 ! autoaudiosink")
# pipeline = Gst.parse_launch("filesrc location=./static/tempfile.mp4 ! videoconvert ! x264enc tune=zerolatency bitrate=700 speed-preset=superfast ! decodebin ! autovideoconvert ! theoraenc ! oggmux ! filesink location=./output.mp4")

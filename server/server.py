from pyimagesearch.motion_detection import SingleMotionDetector
from imutils.video import VideoStream
from flask import Response
from flask import Flask
from flask import render_template
import threading
import datetime
import imutils
import argparse
import time
import cv2
import imagezmq

# outputFrame = None
# lock = threading.Lock()


app = Flask(__name__)
image_hub = imagezmq.ImageHub()

time.sleep(2.0)

@app.route("/")
def index():
	return render_template("index.html")
		
def generate():

	while True:
		rpi_name, frame = image_hub.recv_image()
		# imageHub.send_reply(b'OK')
		# frame = imutils.resize(frame, width=400)
		
		(flag, encodedImage) = cv2.imencode(".jpg", frame)
		# if not flag:
		# 	continue

		yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
			bytearray(encodedImage) + b'\r\n')

@app.route("/video_feed")
def video_feed():
	return Response(generate(), mimetype = "multipart/x-mixed-replace; boundary=frame")


if __name__ == '__main__':
	ap = argparse.ArgumentParser()
	ap.add_argument("-i", "--ip", type=str, required=True,
		help="ip address of the device")
	ap.add_argument("-o", "--port", type=int, required=True,
		help="ephemeral port number of the server (1024 to 65535)")
	ap.add_argument("-f", "--frame-count", type=int, default=32,
		help="# of frames used to construct the background model")
	args = vars(ap.parse_args())

	# start a thread that will perform motion detection
	# t = threading.Thread(target=detect_motion, args=(
	# 	args["frame_count"],))
	# t.daemon = True
	# t.start()

	# start the flask app
	app.run(host=args["ip"], port=args["port"], debug=True,
		 use_reloader=False)
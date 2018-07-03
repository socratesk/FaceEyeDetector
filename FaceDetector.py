
from flask import Flask, render_template, Response
from camera import VideoCamera
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')

# Included these lines just to try that it works on Heroku server.
# Comment these lines if you are running in local machine
port = int(os.environ.get("PORT", 5000))
app.run(host='0.0.0.0', port=port)		# For Heroku server

# Commented the below code just to try that it works on Heroku server.
# But, if you run it in local machine, Keep this main method
#if __name__ == "__main_":
#    port = int(os.environ.get("PORT", 5000)) # For Heroku server
#    app.run(host='0.0.0.0', port=port)		# For Heroku server


    #app.run(debug=False)		# For local machine

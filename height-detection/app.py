from flask import Flask, Response, render_template
from lib import *
import pyttsx3
from playsound import playsound

app = Flask(__name__)

@app.route('/')
def index():
    speak("I am about to measure your height now sir")
    speak("Although I reach a precision upto ninety eight percent")

    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)


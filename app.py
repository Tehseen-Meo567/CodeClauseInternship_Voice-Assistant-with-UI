import requests
from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
import pyttsx3

app = Flask(__name__)

# Initialize the speech recognition and text-to-speech engines
recognizer = sr.Recognizer()
tts = pyttsx3.init()

def recognize_speech_from_microphone():
    with sr.Microphone() as source:
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            return command
        except sr.UnknownValueError:
            return "Sorry, I did not understand that."
        except sr.RequestError:
            return "Sorry, my speech service is down."

def process_command(command):
    # Add your own command processing logic here
    if "hello" in command.lower():
        response = "Hello! How can I help you today?"
    elif "your name" in command.lower():
        response = "I am your friendly voice assistant."
    elif "weather" in command.lower():
        response = "Sorry, I can't fetch the weather right now."
    else:
        response = "I'm not sure how to respond to that."
    return response

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/listen', methods=['POST'])
def listen():
    command = recognize_speech_from_microphone()
    response = process_command(command)
    tts.say(response)
    tts.runAndWait()
    return jsonify({'command': command, 'response': response})

if __name__ == '__main__':
    app.run(debug=True)

